@echo off
SETLOCAL

echo 🚀 Starting Docker Compose stack...
docker compose up -d

echo ⏳ Waiting 15 seconds for Kafka and ZooKeeper to initialize...
timeout /t 15 >nul

echo 📦 Creating Kafka topic 'social_posts' (if not exists)...
docker exec kafka kafka-topics \
  --create \
  --if-not-exists \
  --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic social_posts

echo ⚡ Starting Spark streaming job...
docker compose restart spark

echo ✅ All services running. Open:
echo     ▶ Kafka UI: http://localhost:9000
echo     ▶ Spark UI: http://localhost:4040

ENDLOCAL
