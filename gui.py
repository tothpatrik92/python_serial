import tkinter as tk
import serial
import io
import threading
import time
import sys
import os


        
        
#ser = serial.Serial("COM6")  # open serial port
ser = serial.Serial('COM7', 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)


def Task1(ser):

    while 1:
        print ("Inside Thread 1")
        print(ser.name)         # check which port was really used
        ser.write(b'info\r\n')     # write a string
        #b = ser.readline()
        #print (b)
        print ("Thread 1 still going on")
        time.sleep(1)

def Main():
    #ser = serial.Serial('COM7', 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)
    t1 = threading.Thread(target = Task1, args=[ser])
    print ("Starting Thread 1")
    t1.start()
    print ("=== exiting ===")

    #ser.close()

if __name__ == '__main__':

    Main()







sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

rec = ser.read(10)
print(rec)

ser.close()             # close port


window = tk.Tk()
window.title("Simple Text Editor")

greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()

window.mainloop()