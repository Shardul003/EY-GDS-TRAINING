import time
import random

def producer(q, num_items=5):
    for i in range(num_items):
        item = f"item-{i}"
        print(f"[Producer] Producing {item}")
        q.put(item)
        time.sleep(random.uniform(0.5, 1.5))
    q.put(None)
    print("[Producer] Finished producing.")
