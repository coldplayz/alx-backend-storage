-- calculate weighted average, no input.

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

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers//

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
  BEGIN
    DECLARE w_sum, u_id, offst, cnt, t_weight INT;
    DECLARE w_avg FLOAT;
    -- create view, grouped by user IDs
    CREATE OR REPLACE VIEW v1 AS
      SELECT c.user_id, SUM(c.score * p.weight) AS weighted_sum
        FROM corrections AS c
          LEFT JOIN projects AS p
            ON c.project_id=p.id
        GROUP BY c.user_id;
    -- get total weight
    SELECT SUM(weight) INTO t_weight FROM projects;
    -- get number of rows in view v1
    SELECT COUNT(*) INTO cnt FROM v1;
    SET offst = 0;
    -- use a loop to go throyght IDs in the view
    loop0:
    LOOP
      -- get ID and weighted_sum for each row
      SELECT user_id INTO u_id FROM v1 LIMIT 1 OFFSET offst;
      SELECT weighted_sum INTO w_sum FROM v1 LIMIT 1 OFFSET offst;
      -- compute weighted average for the user
      SET w_avg = w_sum / t_weight;
      -- update the users table with this average
      UPDATE users
        SET average_score = w_avg
        WHERE users.id=u_id;
      SET offst = offst + 1;
      IF offst = cnt THEN
        LEAVE loop0;
      END IF;
    END LOOP;
    -- cleanup
    DROP VIEW v1;
  END; //

DELIMITER ;
