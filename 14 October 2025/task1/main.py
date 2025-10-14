import threading
import queue
from producer import producer
from consumer import consumer

def main():
    q = queue.Queue()

    producer_thread = threading.Thread(target=producer, args=(q,))
    consumer_thread = threading.Thread(target=consumer, args=(q,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print("✅ All tasks completed.")

if __name__ == "__main__":
    main()
