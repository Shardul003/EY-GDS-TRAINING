import pika
import json
import csv
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - CONSUMER - %(levelname)s - %(message)s')

processed_count = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='enrollment_queue')

def callback(ch, method, properties, body):
    global processed_count
    start_time = time.time()
    try:
        record = json.loads(body)
        logging.info(f"Received record: {record}")

        # Error handling for missing fields
        if not record.get("name") or not record.get("course"):
            raise ValueError(f"Missing required fields in record: {record}")

        # ETL: Transform
        record["name"] = record["name"].title()

        # Load: Write to CSV
        with open("processed_enrollments.csv", mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "course"])
            if processed_count == 0:
                writer.writeheader()
            writer.writerow(record)

        processed_count += 1
        elapsed = time.time() - start_time
        logging.info(f"Processed record in {elapsed:.2f}s: {record}")

    except Exception as e:
        logging.error(f"Error processing record: {e}")

channel.basic_consume(queue='enrollment_queue', on_message_callback=callback, auto_ack=True)

logging.info('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()