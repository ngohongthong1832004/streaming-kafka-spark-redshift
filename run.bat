@echo off
SETLOCAL

echo Starting Docker Compose stack (build + detach mode)...
docker compose up --build -d

echo Waiting 15 seconds for Kafka and ZooKeeper to initialize...
timeout /t 15 >nul

echo Creating Kafka topic 'social_posts' (if not exists)...
docker exec kafka kafka-topics ^
  --create ^
  --if-not-exists ^
  --bootstrap-server kafka:9092 ^
  --replication-factor 1 ^
  --partitions 1 ^
  --topic social_posts

echo Sending mock data to topic 'social_posts' using KafkaProducer...
python .\kafka_producer\send_mock_data.py

echo Restarting Spark streaming job to pick up everything fresh...
docker compose restart spark

echo All services running. Open:
echo - Kafka UI:  http://localhost:9000
echo - Spark UI:  http://localhost:4040

ENDLOCAL
