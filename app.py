import sys
import os
import time
import threading
import serial
import string
from tkinter import *


thread_flag = None

root = Tk()
root.title("Zigbee CLI")
root.geometry("400x500")

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

def nwk_steering():
    
    ser.write(b'plugin network-steering start 0\r\n')     # write a string

def nwk_leave():
    ser.write(b'network leave\r\n')     # write a string   
    
def nwk_info():
    ser.write(b'info\r\n')     # write a string      
    
ser = serial.Serial('COM7', 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)  
t1 = threading.Thread(target = Task1, args=[ser])
Report("Starting Thread 1")
t1.start()
textExample=Text(root, height=10)
textExample.pack()
Button_Send=Button(root, height=1, width=10, text="Send", command=getTextInput)
Button_Send.pack()
Y=0.38
DIST=0.1
Button_NwkLeave= Button(root, text="Nwk Leave",command=nwk_steering)
Button_NwkLeave.place(relx = 0.9, rely = Y, anchor = CENTER)
Button_NwkSteering= Button(root, text="Nwk Steering",command=nwk_leave)
Button_NwkSteering.place(relx = 0.9, rely = Y+DIST, anchor = CENTER)
Button_NwkInfo= Button(root, text="Info",command=nwk_info)
Button_NwkInfo.place(relx = 0.9, rely = Y+DIST+DIST, anchor = CENTER)


#time.sleep(3)

#ser.write(b'info\r\n')     # write a string


root.mainloop()