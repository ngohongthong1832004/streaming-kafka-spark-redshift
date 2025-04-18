from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, TimestampType

# Khai báo schema dữ liệu từ Kafka
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

# Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("KafkaToRedshift") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "social_posts") \
    .load()

# Parse JSON từ Kafka message
json_df = df.selectExpr("CAST(value AS STRING)")
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Ghi batch vào Redshift
def write_to_redshift(batch_df, batch_id):
    row_count = batch_df.count()
    print(f"🚀 Batch {batch_id} - Rows: {row_count}")
    if row_count > 0:
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:redshift://lab1.913524914199.us-east-1.redshift-serverless.amazonaws.com:5439/dev") \
            .option("dbtable", "dev") \
            .option("user", "admin") \
            .option("password", "VDBIKyqbnp682.&") \
            .option("driver", "com.amazon.redshift.jdbc42.Driver") \
            .mode("append") \
            .save()
    else:
        print("⚠️ Empty batch — nothing to write.")

# Khởi động streaming query
query = parsed_df.writeStream \
    .foreachBatch(write_to_redshift) \
    .option("checkpointLocation", "/tmp/checkpoint_kafka_to_redshift") \
    .start()

query.awaitTermination()
