import pika
import json
import csv

processed_count = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='enrollment_queue')

def callback(ch, method, properties, body):
    global processed_count
    record = json.loads(body)
    record["name"] = record["name"].title()  # Simple ETL
    with open("processed_enrollments.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "course"])
        if processed_count == 0:
            writer.writeheader()
        writer.writerow(record)
    processed_count += 1
    print(f"Processed: {record}")

channel.basic_consume(queue='enrollment_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()