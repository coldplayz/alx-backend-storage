-- ranks bands by country

-- compute the country with the highest number of fans
SELECT origin, SUM(fans) AS nb_fans
	FROM metal_bands
	GROUP BY origin
	ORDER BY SUM(fans) DESC;
