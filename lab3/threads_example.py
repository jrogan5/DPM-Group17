# Example threadding. used to show how to use threads in python. 
# Source: https://www.youtube.com/watch?v=IEEhzQoKtQU
# Source: https://www.tutorialspoint.com/python/python_multithreading.htm

from asyncio import threads
import threading
import time

start = time.perf_counter() # gets the current time, ie. start time would be zero.


def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')

threads = []

for _ in range(10):
    t = threading.Thread(target=do_something) # creates a thread
    t.start() # starts the thread
    threads.append(t)

for thread in threads:
    thread.join() # waits for the thread to finish before moving on to the next thread

finish = time.perf_counter() # gets the current time

print(f'Finished in {round(finish-start,2)} second(s)')