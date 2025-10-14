import time
import random

def producer(q, num_items=5):
    """Produces items and puts them in the queue."""
    for i in range(num_items):
        item = f"item-{i}"
        print(f"[Producer] Producing {item}")
        q.put(item)
        time.sleep(random.uniform(0.5, 1.5))
    q.put(None)  # Sentinel value to stop consumer
    print("[Producer] Finished producing.")
