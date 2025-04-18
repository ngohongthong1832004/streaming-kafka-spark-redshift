from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, TimestampType

schema = StructType([
    StructField("post_id", StringType()),
    StructField("user_id", LongType()),
    StructField("social_id", IntegerType()),
    StructField("keyword_id", IntegerType()),
    StructField("date", TimestampType()),
    StructField("title", StringType()),
    StructField("content", StringType()),
    StructField("sentiment_score", IntegerType()),
    StructField("count_like", IntegerType()),
    StructField("count_dislike", IntegerType()),
    StructField("count_view", IntegerType()),
    StructField("author", StringType()),
    StructField("url", StringType())
])

spark = SparkSession.builder \
    .appName("KafkaToRedshift") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "social_posts") \
    .option("startingOffsets", "latest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)")
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

def write_to_redshift(batch_df, batch_id):
    try:
        print(f"🔥 Writing batch {batch_id} with {batch_df.count()} rows...")
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:redshift://lab1.913524914199.us-east-1.redshift-serverless.amazonaws.com:5439/dev") \
            .option("user", "admin") \
            .option("password", "VDBIKyqbnp682.&") \
            .option("dbtable", "dev") \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"❌ Failed batch {batch_id}: {e}")

query = parsed_df.writeStream \
    .foreachBatch(write_to_redshift) \
    .option("checkpointLocation", "/tmp/kafka-checkpoint") \
    .start()

query.awaitTermination()
