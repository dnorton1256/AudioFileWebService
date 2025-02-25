from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session
from helpers import check_if_admin
import json
import pymysql.cursors
import settings # Our server and db settings, stored in settings.py
import ssl #include ssl libraries
import sys
#/users/<string:email>
#curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
class User(Resource):
    def get(self, email):
        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'getUser'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [session['email']]) # stored procedure, arguments
            row = cursor.fetchone()
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()
        return make_response(jsonify({'user': row}), 200) # turn set into json and return it

    # curl -i -H "Content-Type: application/json" -X PATCH -d '{"email":"dum@poopie"}' -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
    def patch(self, email):

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        if not request.json or not 'email' in request.json:
            return make_response(jsonify({'status': 'no request'}), 400)

        new_email = request.json['email']
        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'setUser'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [email, new_email, session['admin_status']])
            dbConnection.commit() #NEEDED for updates and inserts
        except pymysql.err.InternalError as e:
            if email != new_email:
                # print(e)
                return make_response(jsonify({'status':new_email+' in use'}), 409)
            return make_response(jsonify({'status':'no change to '+email}), 200)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()

        if email == session['email']:
            session['email'] = new_email
        return make_response(jsonify({'status':'changed '+email+' to '+new_email}), 200)
    # curl -i -H "Content-Type: application/json" -X DELETE -c cookie-jar -b cookie-jar -k https://cs3103.cs.unb.ca:5045/users/tshutty@unb.ca
    def delete(self, email):

        if 'email' not in session:
            return make_response(jsonify({'status': 'not logged in'}), 403)
            
        check_if_admin()
        if session['email'] != email and session['admin_status'] == 0:
            return make_response(jsonify({'status': 'not logged in as '+email+' and not admin'}), 403)

        dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)

        sql = 'deleteUser'
        try:
            cursor = dbConnection.cursor()
            cursor.callproc(sql, [email])
            dbConnection.commit() #NEEDED for updates and inserts
        except pymysql.err.InternalError as e:
            return make_response(jsonify({'status':email+' not found'}), 200)
        except:
            abort(500) # Nondescript server error
        finally:
            cursor.close()
            dbConnection.close()

        if email == session['email']:
            session.pop('email',None)
            session.pop('admin_status',None)

        return make_response(jsonify({'status':'deleted '+email}), 200)
