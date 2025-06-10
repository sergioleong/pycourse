import threading
import time
import random

# --- SCRIPT INTENTION: Multithreading - Producer-Consumer Pattern ---
# This script illustrates basic multithreading using a simple producer-consumer pattern.
# A 'Producer' thread generates random numbers and adds them to a shared list,
# while a 'Consumer' thread waits for numbers to appear and processes them.

# A list to simulate a shared data queue between threads
shared_data_queue = []

# Event to signal when the producer should stop
stop_event = threading.Event()

def producer_thread(thread_id):
    """Generates random integers and adds them to the shared queue."""
    print(f"Producer Thread {thread_id}: Starting...")
    count = 0
    while not stop_event.is_set() and count < 5: # Produce 5 items then stop or if stop_event is set
        random_int = random.randint(1, 100)
        shared_data_queue.append(random_int)
        print(f"Producer Thread {thread_id}: Produced {random_int}. Queue size: {len(shared_data_queue)}")
        count += 1
        time.sleep(random.uniform(0.5, 1.5)) # Simulate work taking variable time

    print(f"Producer Thread {thread_id}: Finished producing.")

def consumer_thread(thread_id):
    """Consumes integers from the shared queue and prints them."""
    print(f"Consumer Thread {thread_id}: Starting...")
    processed_count = 0
    while not stop_event.is_set() or len(shared_data_queue) > 0:
        if shared_data_queue: # Check if there's data to consume
            item = shared_data_queue.pop(0) # Remove from the front of the list
            print(f"Consumer Thread {thread_id}: Consumed {item}. Queue size: {len(shared_data_queue)}")
            processed_count += 1
            time.sleep(random.uniform(0.3, 1.0)) # Simulate processing time
        else:
            # No items, wait a bit before checking again
            time.sleep(0.1) # Small sleep to avoid busy-waiting

    print(f"Consumer Thread {thread_id}: Finished consuming. Total processed: {processed_count}")

def producer_consumer_example():
    print("--- Producer-Consumer Multithreading Example ---")

    producers = []
    consumers = []
    # Create producer and consumer threads
    for i in range(10):
        producers.append(threading.Thread(target=producer_thread, args=(f"P{i}",)))
        consumers.append(threading.Thread(target=consumer_thread, args=(f"C{i}",)))

    # Start the threads
    for i in range(10):
        producers[i].start()
        consumers[i].start()

    # Allow threads to run for a bit
    print("\nMain thread: Running producer and consumer for a few seconds...")
    time.sleep(7) # Let them run for 7 seconds

    # Signal threads to stop
    print("\nMain thread: Signaling threads to stop...")
    stop_event.set()

    for i in range(10):
        producers[i].join()
        consumers[i].join()

    print("\nMain thread: All threads finished. Final queue size:", len(shared_data_queue))
    print("--- Producer-Consumer Multithreading Example Finished ---")

if __name__ == "__main__":
    producer_consumer_example()