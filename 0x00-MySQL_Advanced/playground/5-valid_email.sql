-- create a trigger

DELIMITER //

CREATE TRIGGER reset_email_validity
	BEFORE UPDATE
	ON users
	FOR EACH ROW
		BEGIN
			IF OLD.email <> NEW.email
				THEN
				SET NEW.valid_email = FALSE;
			END IF;
		END; //

DELIMITER ;
