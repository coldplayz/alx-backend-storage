-- create procedure

DELIMITER //

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser//

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
	BEGIN
		-- declare local variable
		DECLARE avrg FLOAT;
		-- calculate average score
		SELECT AVG(score) INTO avrg
			FROM corrections
			WHERE corrections.user_id=user_id;
		-- update users table with average score
		UPDATE users
			SET average_score = avrg
			WHERE id=user_id;
	END; //

DELIMITER ;
