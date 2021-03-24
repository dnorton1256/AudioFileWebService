DELIMITER //
DROP PROCEDURE IF EXISTS setFile //
CREATE PROCEDURE setFile
(
	IN fileId_in INT,
	IN name_in VARCHAR(600),
	IN date_in DATETIME
)
BEGIN
	UPDATE files
	SET file_name = name_in,
			upload_date = date_in
	WHERE file_id = fileId_in;
	
	IF(ROW_COUNT() == 0) THEN
		SIGNAL SQLSTATE '52711'
		SET MSG_TEXT = 'Unable to update the file.';
	END IF;
END //
DELIMITER;