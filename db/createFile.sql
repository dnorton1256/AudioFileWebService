DROP TABLE IF EXISTS files;
CREATE TABLE files(
	file_id INT NOT NULL AUTO_INCREMENT,
	file_name VARCHAR(600) NOT NULL,
	upload_date DATETIME NOT NULL,
	last_played DATETIME,
	times_played INT,
	saved_time DATETIME
)