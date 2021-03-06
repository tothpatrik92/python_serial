import sys
import os
import time
import threading
import serial
import string
from tkinter import *
from time import sleep

thread_flag = None


SERIAL_PORT="COM6"


def cbc(id, tex):
    return lambda : callback(id, tex)

def callback(id, tex):
    s = 'At {} f is {}\n'.format(id, id**id/0.987)
    tex.insert(END, s)
    tex.see(END)             # Scroll if necessary
def printToBox(str,tex):
    #s = 'At {} f is {}\n'.format(id, id**id/0.987)
    #tex.insert(END, s)
    tex.insert(END, str)
    tex.see(END)   


root = Tk()
width_value=root.winfo_screenwidth()
height_value=(root.winfo_screenheight())-100
print(width_value)
print(height_value)
root.title("Zigbee CLI")
root.geometry("%dx%d+0+0" % ((width_value/2), height_value))
root.configure(bg='#c2d8e7')


tex = Text(master=root, width=70, height=60)
tex.place(relx=0.01, rely= 0, anchor=NW)


def SendText(event=None):
    getTextInput()

def getTextInput():
    result=textExample.get("1.0","end")
    print(result)
    ser.write(result.encode())



def Report(s):
    #print (s)
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
            if d.strip():
                Report(d)
                printToBox(d,tex)
                #
            time.sleep(0.01)
        if thread_flag == 'stop': break
        else: thread_flag = 'paused'   # signals that the inner loop is done

def nwk_creator0():
    
    ser.write(b'plugin network-creator start 0\r\n')     # write a string
    
def nwk_creator1():
    
    ser.write(b'plugin network-creator start 0\r\n')     # write a string
    
def nwk_open():
    
    ser.write(b'plugin network-creator-security open-network\r\n')     # write a string

def nwk_steering():
    
    ser.write(b'plugin network-steering start 0\r\n')     # write a string

def nwk_leave():
    ser.write(b'network leave\r\n')     # write a string   
    
def nwk_info():
    ser.write(b'info\r\n')     # write a string   
    
def ImageNotify():
    ser.write(b'raw 0x0019 {09 BD 00 02 64 02 10 00 00}\r\n')     # write a string
    ser.write(b'send 0x2707 1 1\r\n')     # write a string    
def QueryResponse():
    ser.write(b'raw 0x0019 {19 C2 02 00 02 10 00 00 03 00 00 00 A9 CF 02 00}\r\n')    # write a string
    ser.write(b'send 0x2707 1 1\r\n')     # write a string    
def BlockResponse():
    ser.write(b'raw 0x0019 { 19 C8 05 00 0B 10 1C 01 06 04 00 00 00 00 00 00 3F 1E F1 EE 0B 00 01 38 00 00 00 0B 10 1C 01 06 04 00 00 02 00 45 42 4C 20 70 72 6F 6A 65 63 74 5F 7A 6F 72 72 6F 27 00 00 00 00 00 00 00 00 00 00 00 00 00 00 A9 CF 02 00 00 00 6B CF 02 00 EB}\r\n')     # write a string
    ser.write(b'send 0x2707 1 1\r\n')     # write a string  


ser = serial.Serial(SERIAL_PORT, 112500, timeout=0, parity=serial.PARITY_EVEN, rtscts=0)  
t1 = threading.Thread(target = Task1, args=[ser])
Report("Starting Thread 1")
t1.start()
textExample=Text(root, height=15, width=40)
textExample.place(relx = 0.99, rely =0 , anchor=NE)
Button_Send=Button(root, height=1, width=10, text="Send", command=getTextInput)
Button_Send.pack()

Y=0.38
DIST=0.1
n=1

Button_NwkCreator0= Button(root, text="Nwk Creator Distr",command=nwk_creator0)
Button_NwkCreator0.place(relx = 0.7, rely = Y, anchor = CENTER)

Button_NwkLeave= Button(root, text="Nwk Leave",command=nwk_leave)
Button_NwkLeave.place(relx = 0.9, rely = Y, anchor = CENTER)

Button_NwkCreator1= Button(root, text="Nwk Creator Centr",command=nwk_creator1)
Button_NwkCreator1.place(relx = 0.7, rely = Y+(n*DIST), anchor = CENTER)


Button_NwkSteering= Button(root, text="Nwk Steering",command=nwk_steering)
Button_NwkSteering.place(relx = 0.9, rely = Y+(n*DIST), anchor = CENTER)
n+=1

Button_NwkOpen= Button(root, text="Nwk Open",command=nwk_open)
Button_NwkOpen.place(relx = 0.7, rely = Y+(n*DIST), anchor = CENTER)


Button_NwkInfo= Button(root, text="Info",command=nwk_info)
Button_NwkInfo.place(relx = 0.9, rely = Y+(n*DIST), anchor = CENTER)
n+=1

Button_ImageNotify= Button(root, text="ImageNotify",command=ImageNotify)
Button_ImageNotify.place(relx = 0.9, rely = Y+(n*DIST), anchor = CENTER)
n+=1

Button_QueryResponse= Button(root, text="QueryResponse",command=QueryResponse)
Button_QueryResponse.place(relx = 0.9, rely = Y+(n*DIST), anchor = CENTER)
n+=1

Button_BlockResponse= Button(root, text="BlockResponse",command=BlockResponse)
Button_BlockResponse.place(relx = 0.9, rely = Y+(n*DIST), anchor = CENTER)
n+=1
root.bind('<Return>', SendText)
root.mainloop()