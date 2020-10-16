import sys
import os
import time
import threading
import serial
import string
import tkinter as tk

thread_flag = None

root = tk.Tk()
root.title("Zigbee CLI")
root.geometry("400x240")

def getTextInput():
    result=textExample.get("1.0","end")
    print(result)
    ser.write(result.encode())



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
            #print(row)
            d=row.decode("utf-8")
            if d.strip():Report(d)
            #if d.strip():print(d)
            time.sleep(0.01)

        if thread_flag == 'stop': break
        else: thread_flag = 'paused'   # signals that the inner loop is done


    
ser = serial.Serial('COM7', 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)  
t1 = threading.Thread(target = Task1, args=[ser])
Report("Starting Thread 1")
t1.start()
textExample=tk.Text(root, height=10)
textExample.pack()
btnRead=tk.Button(root, height=1, width=10, text="Send", command=getTextInput)
btnRead.pack()

#ser = serial.Serial(7, 11520)





#time.sleep(3)

ser.write(b'info\r\n')     # write a string
time.sleep(1)
ser.write(b'network leave\r\n')     # write a string
time.sleep(1)
ser.write(b'plugin network-steering start 0\r\n')     # write a string
root.mainloop()