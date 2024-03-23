import threading
import random
import time

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Shared variables
buffer = []
mutex = threading.Lock()
producer_done = False
even_done = False
odd_done = False

def producer():
    global buffer, producer_done
    with open('all.txt', 'w') as f_all:
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            f_all.write(str(num) + '\n')
            with mutex:
                buffer.append(num)
    producer_done = True

def even():
    global buffer, even_done
    with open('even.txt', 'w') as f_even:
        while not producer_done or buffer:
            with mutex:
                if buffer and buffer[-1] % 2 == 0:
                    num = buffer.pop()
                    f_even.write(str(num) + '\n')
    even_done = True

def odd():
    global buffer, odd_done
    with open('odd.txt', 'w') as f_odd:
        while not producer_done or buffer:
            with mutex:
                if buffer and buffer[-1] % 2 != 0:
                    num = buffer.pop()
                    f_odd.write(str(num) + '\n')
    odd_done = True

if __name__ == "__main__":
    start_time = time.time()
    producer_thread = threading.Thread(target=producer)
    even_thread = threading.Thread(target=even)
    odd_thread = threading.Thread(target=odd)

    producer_thread.start()
    even_thread.start()
    odd_thread.start()

    producer_thread.join()
    even_thread.join()
    odd_thread.join()

    end_time = time.time()
    print("Program execution complete.")
    print(f"Execution time: {end_time - start_time:.2f} seconds.")
