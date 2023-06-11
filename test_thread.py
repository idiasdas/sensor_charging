import time
import threading

startTime = time.time()
my_lock = threading.Lock()
def foo(i, my_lock):
    time.sleep(1)
    my_lock.acquire()

    test_file = open("test_file.txt","a")
    test_file.write(str(i) + '\n')
    my_lock.release()

threads = []
for i in range(10):
    thread = threading.Thread(target = foo, args=[i,my_lock])
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

endTime = time.time()
elapsedTime = endTime - startTime
print("Elapsed Time = " + str(elapsedTime))