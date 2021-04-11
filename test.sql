SELECT 
	Year, 
	month, 
	count(clothing) AS ClothingSaleQTY, 
	count(bikes) AS BikesSaleQTY
FROM table_name
GROUP BY(month)
HAVING ClothingSaleQTY < BikesSaleQTY;