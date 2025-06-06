# 🚀 Streaming Kafka → Spark → Amazon Redshift

A complete real-time data pipeline that streams data from Apache Kafka, processes it with PySpark, and stores it in Amazon Redshift.

---

## 📦 Tech Stack

- **Apache Kafka**: Real-time message broker
- **Apache Spark (PySpark Structured Streaming)**: Real-time data processing
- **Amazon Redshift**: Cloud data warehouse (for storing processed data)
- **Docker Compose**: Service orchestration
- **Kafka UI (Kafdrop)**: Web interface to inspect Kafka topics
- **Faker + Kafka Producer (Python)**: For generating mock data

---

## 🏗️ Architecture

```text
[ Kafka Producer (Python) ] --> [ Kafka Topic: social_posts ] --> [ Spark Structured Streaming ] --> [ Amazon Redshift ]
