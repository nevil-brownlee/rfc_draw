import threading, time
from playsound import playsound

start = time.time()

def ring_bell(n):
    playsound("BSB-counter-bell.wav")
    #print("%d x %d = %d" % (n, n, n*n))
#calc_square(3)

def calc_cube(n):
    print("%d x %d x %d = %d" % (n, n, n, n*n*n))
#calc_cube(2)

bell_thread = threading.Thread(target=ring_bell, args=((),))
#cube_thread = threading.Thread(target=calc_cube, args=((2),))

bell_thread.start()
#cube_thread.start()

#square_thread.join()
#print("finished square_thread")
#cube_thread.join()
print("finished cube_thread")
             
##calc_cube(3)
end = time.time()

print('Execution Time: {}'.format(end-start))
n = 21
for j in range(n):
    print("j = %d" % j)

