-- SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

-- Column names must be: band_name and lifespan (in years)
SELECT band_name, (split - formed) AS lifespan
	FROM metal_bands
	WHERE style LIKE '%Glam rock%'
	ORDER BY lifespan DESC;