-- calculate weighted average

/**
* Explanation:
* - Consider a quantity that represents a range; a sort of weight space.
* In this case, it's the weight of the Python
* ...project (2) plus that of the C project (1),
* ...giving a total weight of 3.
*
* - Weighted average is given as:
* 	sum(project_score * weight) divided by the total weight.
*/

DELIMITER //

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser//

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
  BEGIN
    DECLARE w_sum, t_weight INT;
    DECLARE w_avg FLOAT;
    /*
    -- create a view of the data we need, merging corrections and projects
    CREATE OR REPLACE VIEW v1 AS
      SELECT *
        FROM corrections AS c
          LEFT JOIN projects AS p
            ON c.project_id=p.id
        WHERE c.user_id=user_id;
    */
    -- get the weighted sum, and total weight from subquery
    SELECT SUM(score * weight) INTO w_sum FROM
      (SELECT *
        FROM corrections AS c
          LEFT JOIN projects AS p
            ON c.project_id=p.id
        WHERE c.user_id=user_id) AS sq;
    SELECT SUM(weight) INTO t_weight FROM
      (SELECT *
        FROM corrections AS c2
          LEFT JOIN projects AS p2
            ON c2.project_id=p2.id
        WHERE c2.user_id=user_id) AS sq;
    -- compute weighted average
    SET w_avg = w_sum / t_weight;
    -- update the users table with this average
    UPDATE users
      SET average_score = w_avg
      WHERE users.id=user_id;
    /*
    -- drop created view to clean namespace
    DROP VIEW v1;
    */
  END; //

DELIMITER ;
