DELIMITER //
CROP PROCEDURE IF EXISTS deleteFile //
CREATE PROCEDURE deleteFile(
	IN fileId_in INT
)
BEGIN
	DELETE FROM files WHERE file_id = fileID_in;
	
	IF(ROW_COUNT() = 0) THEN
		SIGNAL SQLSTATE '45000'
		SET msg_text = 'Unable to delete the file';
	END IF;
END //
DELIMITER;