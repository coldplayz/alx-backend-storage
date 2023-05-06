-- create procedure

DELIMITER //

CREATE PROCEDURE AddBonus(
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
	)
	BEGIN
		-- declare local variable
		DECLARE proj_id INT;
		-- get the id related to project name
		SELECT id INTO proj_id FROM projects WHERE name=project_name;
		IF proj_id <=> NULL THEN
			-- create a new projects table record and retrieve ID
			INSERT INTO projects (name) VALUES (project_name);
			SET proj_id = LAST_INSERT_ID();
		END IF;
		-- update corrections table
		INSERT INTO corrections (user_id, project_id, score)
			VALUES (user_id, proj_id, score);
	END; //

DELIMITER ;
