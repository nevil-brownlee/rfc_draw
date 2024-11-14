import logging
import time

import threading
from playsound import playsound

def thread_function(n):
    logging.info("Thread %s: starting", n)
    playsound("BSB-counter-bell.wav")
    logging.info("Thread %s: finishing", n)
    return

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")

    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")

    x.start()
    #logging.info("Main    : wait for the thread to finish")

    #x.join()
    logging.info("Main    : all done")
    print("didn't wait for thread <<<")
