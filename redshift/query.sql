
---- create external schema for glue catalog
create EXTERNAL SCHEMA property_schema
FROM DATA CATALOG
database 'enhance_property'
IAM_ROLE 'arn:aws:iam::52142885190825:role/RedshiftproperyRole'
create EXTERNAL DATABASE if not exists;

-------------------

--- select all property limit 10

select * from property_schema.property_consumption_zone limit 10;


---- select specific column

select property_url,city,state,unit,beds,list_price,style,street,status
from property_schema.property_consumption_zone order by year_built limit 10;