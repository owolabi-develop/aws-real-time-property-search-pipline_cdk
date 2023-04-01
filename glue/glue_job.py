import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1711980189310 = glueContext.create_dynamic_frame.from_catalog(
    database="property-database",
    table_name="property_raw_zone",
    transformation_ctx="AWSGlueDataCatalog_node1711980189310",
)

# Script generated for node Change Schema
ChangeSchema_node1711980219070 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1711980189310,
    mappings=[
        ("property_url", "string", "property_url", "string"),
        ("mls", "string", "mls", "string"),
        ("mls_id", "int", "mls_id", "int"),
        ("status", "string", "status", "string"),
        ("style.name", "string", "style.name", "string"),
        ("style.value", "string", "style.value", "string"),
        ("street", "string", "street", "string"),
        ("unit", "int", "unit", "int"),
        ("city", "string", "city", "string"),
        ("state", "string", "state", "string"),
        ("zip_code", "string", "zip_code", "string"),
        ("beds", "int", "beds", "int"),
        ("full_baths", "int", "full_baths", "int"),
        ("half_baths", "int", "half_baths", "int"),
        ("sqft", "int", "sqft", "int"),
        ("year_built", "int", "year_built", "int"),
        ("days_on_mls", "int", "days_on_mls", "int"),
        ("list_price", "int", "list_price", "int"),
        ("list_date", "string", "list_date", "string"),
        ("sold_price", "int", "sold_price", "int"),
        ("last_sold_date", "string", "last_sold_date", "string"),
        ("lot_sqft", "int", "lot_sqft", "int"),
        ("price_per_sqft", "int", "price_per_sqft", "int"),
        ("latitude", "double", "latitude", "double"),
        ("longitude", "double", "longitude", "double"),
        ("stories", "int", "stories", "int"),
        ("hoa_fee", "int", "hoa_fee", "int"),
        ("parking_garage", "int", "parking_garage", "int"),
        ("primary_photo", "string", "primary_photo", "string"),
        ("alt_photos", "string", "alt_photos", "string"),
        ("partition_0", "string", "partition_0", "string"),
        ("partition_1", "string", "partition_1", "string"),
        ("partition_2", "string", "partition_2", "string"),
        ("partition_3", "string", "partition_3", "string"),
    ],
    transformation_ctx="ChangeSchema_node1711980219070",
)

# Script generated for node Amazon S3
AmazonS3_node1711980294963 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1711980219070,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://property-consumption-zone",
        "partitionKeys": ["state", "street", "status"],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1711980294963",
)

job.commit()
