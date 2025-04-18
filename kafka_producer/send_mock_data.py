
from kafka import KafkaProducer
import json
import time
import random
from faker import Faker

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],  # Thử 127.0.0.1 hoặc host.docker.internal
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'social_posts'

social_ids = [1, 2, 3, 4]  # facebook, youtube, tiktok, website
keyword_ids = [1, 2, 3, 4]

while True:
    message = {
        'post_id': fake.uuid4(),
        'user_id': random.randint(1, 1000),
        'social_id': random.choice(social_ids),
        'keyword_id': random.choice(keyword_ids),
        'date': fake.date_time().isoformat(),
        'title': fake.sentence(),
        'content': fake.text(),
        'sentiment_score': random.randint(-1, 1),
        'count_like': random.randint(0, 1000),
        'count_dislike': random.randint(0, 500),
        'count_view': random.randint(0, 10000),
        'author': fake.name(),
        'url': fake.url()
    }
    producer.send(topic, value=message)
    print("Sent:", message["post_id"])
    time.sleep(1)