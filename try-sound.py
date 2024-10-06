#from playsound import playsound

#song = AudioSegment.from_wav("BSB-counter-bell.wav")
#song = AudioSegment.from_wav("small-bell.wav")

#play_sounds("BSB-small-bell.wav")  # louder
#playsound("BSB-counter-bell.wav")

import time

def n_bells(n_rings):
    for n in range(n_rings):
        print(n)
        print("\a",end='')  # BEL
        time.sleep(0.2)

n_bells(3)
