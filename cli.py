import sys
import os
import time
import threading
import serial
import string

thread_flag = None


def Report(s):
    print (s)
    sys.stdout.flush() # helps to ensure messages from different threads appear in the right order

def Stop():
    global thread_flag
    thread_flag = 'stop'

def Task1(ser):

    Report("Inside Thread 1")
    global thread_flag
    thread_flag = 'go'

    while True:

        Report("Thread 1 waiting for permission to read")
        while thread_flag != 'go': time.sleep( 0.0001 )

        while thread_flag == 'go':
            #Report("Thread 1 is reading")
            #ser.write('\x5A\x03\x02\x02\x02\x09') # Byte ArrayTo Control a MicroProcessing Unit
            #b = ser.read(1000)
            row=ser.readline()
            d=row.decode("utf-8")
            if d.strip():print(d)
            time.sleep(0.1)

        if thread_flag == 'stop': break
        else: thread_flag = 'paused'   # signals that the inner loop is done

    #Report("Thread 1 complete")


def Task2(ser):

    Report("Inside Thread 2")

    global thread_flag
    thread_flag = 'pause' # signals Task1 to pause
    while thread_flag != 'paused': time.sleep(0.001) # waits for Task1 inner loop to exit
    Report("I stopped Task 1 to start and execute Thread 2")

    ser.write(b'info\r\n')     # write a string
    
    #c = ser.read(7)
    #Report(c.encode('hex'))

    thread_flag = 'go' # signals Thread 1 to resume
    Report("Thread 2 complete")


def Main():
    #ser = serial.Serial(7, 11520)
    ser = serial.Serial('COM7', 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)
    t1 = threading.Thread(target = Task1, args=[ser])
    t2 = threading.Thread(target = Task2, args=[ser])
    Report("Starting Thread 1")
    t1.start()

    time.sleep(3)
    Report("Starting Thread 2")
    t2.start()


if __name__ == '__main__':

    Main()