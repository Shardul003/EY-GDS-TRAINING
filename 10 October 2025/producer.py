# consumer.py
import pika
import json
import time

# 1. Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# 2. Ensure the queue exists
channel.queue_declare(queue="student_tasks")

# 3. Define message handling function
task={
    "student_id":"101",
    "action":"generate_certificate",
    "email":"rahul@example.com"
}
channel.basic_publish(
    exchange='',
    routing_key='student_tasks',
    body=json.dumps(task),
)
print("Task sent to queue:", task)
connection.close()