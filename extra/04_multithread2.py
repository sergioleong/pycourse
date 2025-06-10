import threading
import time
import random
import queue # Import the thread-safe Queue module

# --- SCRIPT INTENTION: Multithreading - Producer-Consumer with Synchronization ---
# This script demonstrates a more robust producer-consumer pattern using Python's
# thread-safe `queue.Queue` for safe data exchange between threads.
# It ensures synchronization and avoids race conditions and busy-waiting.

# A thread-safe queue to simulate a shared data buffer
# maxsize can be set to limit the queue size, causing producer to block if full.
shared_data_queue = queue.Queue(maxsize=5)

# Event to signal when the producer should stop
stop_producer_event = threading.Event()
# Event to signal when consumers should stop (after queue is empty)
stop_consumer_event = threading.Event()

def producer_thread_sync(thread_id):
    """Generates random integers and adds them to the thread-safe queue."""
    print(f"Producer Thread {thread_id}: Starting...")
    for i in range(10): # Produce 10 items
        if stop_producer_event.is_set():
            break
        item = random.randint(101, 200)
        try:
            # put() will block if the queue is full (because maxsize=5)
            shared_data_queue.put(item, timeout=1) # Timeout to prevent indefinite blocking if no consumer
            print(f"Producer Thread {thread_id}: Produced {item}. Queue size: {shared_data_queue.qsize()}")
        except queue.Full:
            print(f"Producer Thread {thread_id}: Queue full, waiting to put {item}...")
            if stop_producer_event.is_set(): # Check again in case signal arrived during wait
                break
        time.sleep(random.uniform(0.3, 0.8)) # Simulate variable production time

    print(f"Producer Thread {thread_id}: Finished producing.")

def consumer_thread_sync(thread_id):
    """Consumes integers from the thread-safe queue and prints them."""
    print(f"Consumer Thread {thread_id}: Starting...")
    processed_count = 0
    while not stop_consumer_event.is_set() or not shared_data_queue.empty():
        try:
            # get() will block until an item is available
            # We add a timeout to allow the loop to check stop_consumer_event
            item = shared_data_queue.get(timeout=0.5)
            print(f"Consumer Thread {thread_id}: Consumed {item}. Queue size: {shared_data_queue.qsize()}")
            processed_count += 1
            # Signal that this item has been processed (important for queue.join())
            shared_data_queue.task_done()
        except queue.Empty:
            # This happens if timeout expires and queue is empty.
            # Continue checking stop_consumer_event and queue.empty()
            pass

    print(f"Consumer Thread {thread_id}: Finished consuming. Total processed: {processed_count}")

def producer_consumer_sync_example():
    print("--- Producer-Consumer with Synchronization Example ---")

    producers = []
    consumers = []
    # Create producer and consumer threads
    for i in range(10):
        producers.append(threading.Thread(target=producer_thread_sync, args=(f"P{i}",)))
        consumers.append(threading.Thread(target=consumer_thread_sync, args=(f"C{i}",)))

    # Start the threads
    for i in range(10):
        producers[i].start()
        consumers[i].start()


    # Main thread: Wait 3s an signalize producers to stop producing new messages
    time.sleep(5) 
    stop_producer_event.set()

    # Main thread: Wait for the producers to finish putting all items
    for i in range(10):
        producers[i].join()
    print("\nMain thread: Producer has finished its work.")

    # Main thread: Wait for all items in the queue to be processed by consumers
    # This call blocks until all items ever put into the queue have been retrieved and `task_done()` called.
    shared_data_queue.join()
    print("Main thread: All items in queue have been processed.")

    # Now that the queue is empty and producer is done, signal consumers to stop their loop
    stop_consumer_event.set()

    # Wait for the consumers to finish its cleanup
    for i in range(10):
        consumers[i].join()

    print("\nMain thread: All threads finished. Final queue size:", shared_data_queue.qsize())
    print("--- Producer-Consumer with Synchronization Example Finished ---")

if __name__ == "__main__":
    producer_consumer_sync_example()