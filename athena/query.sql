

--- get all sold property order by city

SELECT * FROM 
"property-database"."property_raw_zone" 
where 
status='Sold' ORDER BY city;


--- get all property
SELECT * FROM "property-database"."property_raw_zone";

--- get properties in cities
SELECT * FROM "property-database"."property_raw_zone" where city in ('North Anthony','Phillipsberg') 