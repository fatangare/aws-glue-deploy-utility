import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from utility.src.config.env import Env 
from ingestion.etl.src.bp_sample_pyspark import BpSamplePySpark

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'project','stage'])

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args['JOB_NAME'], args)

# Job input parameters
project = args['project']
stage = args['stage']
env = Env.get_config(project,stage)
incoming_path = "s3://{}/{}/food".format(env["s3_data_lake"], env["incoming_folder"])
primary_path = "s3://{}/{}/food".format(env["s3_data_lake"], env["primary_folder"])

# Read Data
datasource0 = glue_context.create_dynamic_frame_from_options(connection_type='s3', 
                                connection_options = {"paths": [incoming_path]}, format = "csv", \
                                format_options={"withHeader":True}, transformation_ctx = "readctx")

datasource0.printSchema()
datasource0.show(2)

# mask numbers in data with _number_
bpSamplePySpark = BpSamplePySpark(spark, env)
df = bpSamplePySpark.process_data(datasource0.toDF())
dyf = DynamicFrame.fromDF(df, glue_context, 'dyf')

# Write data
glue_context.write_dynamic_frame_from_options(frame = dyf, connection_type = "s3", \
                                connection_options = {"path": primary_path, \
                                }, format = "parquet", transformation_ctx = "writectx")
job.commit()
