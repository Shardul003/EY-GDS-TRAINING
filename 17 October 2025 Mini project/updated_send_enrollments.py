import pika
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PRODUCER - %(levelname)s - %(message)s')

enrollments = [
    {"id": 1, "name": "Alice", "course": "Python"},
    {"id": 2, "name": "", "course": "Data Science"},  # Missing student name
    {"id": 3, "name": "Charlie", "course": ""},       # Missing course
]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='enrollment_queue')

for record in enrollments:
    logging.info(f"New enrollment: {record}")
    message = json.dumps(record)
    channel.basic_publish(exchange='', routing_key='enrollment_queue', body=message)

connection.close()