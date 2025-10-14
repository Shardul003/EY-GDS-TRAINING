import time
import random

def consumer(q):
    """Consumes items from the queue."""
    while True:
        item = q.get()
        if item is None:
            print("[Consumer] No more items. Exiting.")
            break
        print(f"[Consumer] Consuming {item}")
        time.sleep(random.uniform(1, 2))
    print("[Consumer] Finished consuming.")
