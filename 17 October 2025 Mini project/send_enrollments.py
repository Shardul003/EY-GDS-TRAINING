import pika
import json

enrollments = [
    {"id": 1, "name": "Alice", "course": "Python"},
    {"id": 2, "name": "Bob", "course": "Data Science"},
    {"id": 3, "name": "Charlie", "course": "AI"},
]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='enrollment_queue')

for record in enrollments:
    message = json.dumps(record)
    channel.basic_publish(exchange='', routing_key='enrollment_queue', body=message)
    print(f"Sent: {record}")

connection.close()