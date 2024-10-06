from threading import Thread
from playsound import playsound


def ring_bell(n):
    print("ring_bell, n %d" % n)
    playsound("BSB-counter-bell.wav")

name = "Tutorialspoint..."

# Create and start threads
thread1 = Thread(target=ring_bell, args=(1))
#thread2 = threading.Thread(target=print_name, args=(name, 1, 2))

thread1.start()
#thread2.start()

# Wait for threads to complete
thread1.join()
#thread2.join()

print("Threads are finished...exiting")
