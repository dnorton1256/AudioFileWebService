DEMLIMITER //
DROP PROCEDURE IF EXISTS getFile //
CREATE PROCEDURE getUser
(
   IN fileId_in INT
)
BEGIN
	SELECT * FROM files WHERE file_id = fileId_in;
END //
DELIMITER ;