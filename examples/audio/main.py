from time import sleep
from androidaudio import AndroidMicrophone

if __name__ == "__main__":

    microphone = AndroidMicrophone()
    microphone.start()
    print 'Status', microphone.status
    sleep(5)
    microphone.stop()
    print 'Status', microphone.status
    sleep(1)
    microphone.start()
    print 'Status', microphone.status
    sleep(10)
    microphone.stop()
