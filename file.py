from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session

import json
import pymysql.cursors
import settings
import ssl
import sys

class File(resource):
	def get():
	
		dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor
		)
		
		sql = 'getFile'
		try:
			cursor = dbConnection.cursor()
			cursor.callproc(sql, [session['fileID']])
			row = cursor.fetchone()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_reponse(jsonify({'file': row}), 200)
	
	def patch
		# to do #
		 dbConnection = pymysql.connect(
            settings.MYSQL_HOST,
            settings.MYSQL_USER,
            settings.MYSQL_PASSWD,
            settings.MYSQL_DB,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
			
	def delete
		# to do #