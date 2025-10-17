import csv
import threading
import queue
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Shared queue
enrollment_queue = queue.Queue()

# Sample data to simulate new enrollments
new_enrollments = [
    {"id": 1, "name": "Alice", "course": "Python"},
    {"id": 2, "name": "Bob", "course": "Data Science"},
    {"id": 3, "name": "Charlie", "course": "AI"},
]

# Producer function
def producer():
    for record in new_enrollments:
        logging.info(f"Producing record: {record}")
        enrollment_queue.put(record)
        time.sleep(1)  # Simulate delay

# Consumer function
def consumer():
    processed_count = 0
    with open('processed_enrollments.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "course"])
        writer.writeheader()
        while True:
            try:
                record = enrollment_queue.get(timeout=5)  # Wait for a record
                # Simulate ETL processing
                record["name"] = record["name"].title()
                writer.writerow(record)
                processed_count += 1
                logging.info(f"Processed record: {record}")
                enrollment_queue.task_done()
            except queue.Empty:
                break
    logging.info(f"Total records processed: {processed_count}")

# Start threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
