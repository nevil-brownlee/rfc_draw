
from playsound import playsound
import threading
import time

def print_name(name, *arg):
    playsound("BSB-counter-bell.wav")
    return

name="Tutorialspoint..."

thread1 = threading.Thread(target=print_name, args=(name, 1))

thread1.start()

thread1.join()

print("Threads are finished...exiting")
