#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter.filedialog import askopenfilename

import os, threading, time, webbrowser

from ines import Ines

import pygame
# Table contains mappings for controller buttons to the NES buttons.
# The bit mappings for the NES buttons are:
# 0 = A, 1 = B, 2 = Select, 3 = Start, 4 = Up, 5 = Down, 6 = Left, 7 = Right.
# The button mappings are defined as "controller-button":"nes-button".
# Some controllers implement the D-pad as separate buttons others as a hat switch (x-axis, y-axis)
button_mappings = {
    # Controller name                       A,   B, Select, Start,   Up, Down, Left, Right
    'Nintendo Switch Pro Controller'   : {0:0, 1:1,    4:2,   6:3, 11:4, 12:5, 13:6, 14:7},
    'Controller (XBOX 360 For Windows)': {1:0, 0:1,    6:2,   7:3}, # D-pad as hat switch
    'Default'                          : {1:0, 0:1,    6:2,   7:3}, # D-pad as hat switch
}

# pyserial
import serial
import serial.tools.list_ports

from importlib import reload

ports = serial.tools.list_ports.comports()
devices=[]
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    devices.append(port)

if len(devices) == 0:
    msg="Cannot find any serial port. Connnect USB cable and try again?"
    print(msg)
    messagebox.showerror("Error", msg)
    exit(1)

top = Tk()
device=StringVar(top)
device.set(devices[0])
ser=None

def about():
    messagebox.showinfo("About",
    """
    NES260 - NES emulator for KV260 FPGA board
    
    Original version by:
    (c) Feng Zhou, 2022.7
    https://github.com/zf3/

    Updated by:
    RPKH, 2023
    https://github.com/rpkh/
    """)

def site():
    webbrowser.open("https://github.com/rpkh/nes260")

def initUi():
    top.title("NES260")
    top.geometry("480x250")

    title=Label(top, text='NES260', fg="#555")
    title.configure(font=("Arial", 22, "bold"))
    title.place(x=150, y=20)

    menu = Menu(top)
    top.config(menu=menu)
    helpMenu = Menu(menu)
    helpMenu.add_command(label="Project site", command=site)
    helpMenu.add_command(label="About", command=about)
    menu.add_cascade(label="Help", menu=helpMenu)

    btnLoad = Button(top, text = "Load .nes", command=chooseInes)
    btnLoad.place(x=50, y=90)

    global desc1, desc2, desc3, desc4
    desc1=Label(top, text='No nes file open')
    desc2=Label(top, text='Size: ')
    desc3=Label(top, text='Mapper: ')
    desc4=Label(top, text='PRG:, CHR:')

    desc1.place(x=160, y=70)
    desc2.place(x=160, y=90)
    desc3.place(x=160, y=110)
    desc4.place(x=160, y=130)

    # Serial port selection
    labelSerial=Label(top, text="Serial")
    labelSerial.place(x=50, y=170)
    global labelSerialStatus
    labelSerialStatus=Label(top, text="")
    labelSerialStatus.place(x=110, y=170)
    global device
    optionSerial=OptionMenu(top, device, *devices, command=serialSelected)
    optionSerial.place(x=50, y=190)

    # Controller group
    labelfrmCtr=LabelFrame(top, text="Controllers")
    labelfrmCtr.grid(column=2, row=1)
    labelfrmCtr.place(x=160, y=170)

    # Controller 1
    labelCtr1=Label(labelfrmCtr, text="1:")
    labelCtr1.grid(column=0, row=0)
    global labelCtr1Status
    labelCtr1Status=Label(labelfrmCtr, text="Disconnected", fg="#888")
    labelCtr1Status.grid(column=1, row=0)
    global labelCtr1Name
    labelCtr1Name=Label(labelfrmCtr, text="", justify='left', anchor='w')
    labelCtr1Name.grid(column=2, row=0,)

    # Controller 2
    labelCtr2=Label(labelfrmCtr, text="2:")
    labelCtr2.grid(column=0, row=1)
    global labelCtr2Status
    labelCtr2Status=Label(labelfrmCtr, text="Disconnected", fg="#888")
    labelCtr2Status.grid(column=1, row=1, sticky=W)
    global labelCtr2Name
    labelCtr2Name=Label(labelfrmCtr, text="")
    labelCtr2Name.grid(column=2, row=1, sticky=W)

def connectSerial():
    global ser
    if ser==None:
        ser=serial.Serial(device.get(), 230400, write_timeout=0)

def serialSelected(choice):
    print("Serial: {}".format(choice))
    global ser
    if ser != None:
        ser.close()
        ser=None
    connectSerial()

def showInesInfo(filename):
    size=os.stat(filename).st_size
    desc1.config(text=os.path.basename(filename))
    desc2.config(text="Size: {}".format(size))

    # parse file using kaitaistruct
    try:
        data=Ines.from_file(filename)
        header=data.header
        desc3.config(text="Mapper: {}".format(header.mapper))
        desc4.config(text="PRG: {}KB, CHR: {}KB".format(16*header.len_prg_rom, 8*header.len_chr_rom))
    except Exception:   # parse error, just ignore
        desc3.config(text="Mapper: ")
        desc4.config(text="PRG:, CHR:")

def chooseInes():
    filename=askopenfilename(title='Choose a .nes file', filetypes=(("nes files", "*.nes"),("all files","*.*")))
    showInesInfo(filename)
    sendInes(filename)

PROGRESS=['/','-','\\','|']

def sendInes(fname):
    if not os.path.isfile(fname):
        print("Cannot open file: {}".format(fname))
        exit(1)

    size=os.stat(fname).st_size
    f=open(fname, 'rb')
    data=bytearray(f.read())
    f.close()

    # send data over serial line
    # 115200,8,N,1
    header=bytearray([1])       # command: ines
    header += size.to_bytes(4, 'little')    # we send little-endian
    connectSerial()
    ser.write(header)
    CHUNK=1024
    for i in range(0,len(data),CHUNK):
        labelSerialStatus.config(text=PROGRESS[(i//CHUNK)%4], fg='#000')  # show an animation for progress
        top.update()
        ser.write(data[i:min(i+CHUNK,len(data))])

    print("Sent {} bytes over serial line.".format(len(data)))

line=''
def dumpSerial():
    global ser, line
    while True:
        try:
            if ser != None and ser.inWaiting():
                din = ser.read(1)
                s = din.decode("iso-8859-1")
                print(s, end='')
                if s == '\n':
                    line=''
                else:
                    line += s
                if 'FPGA' in line:  # PS returns this when ines is sent to PL
                    labelSerialStatus.config(text='OK', fg='#0c0')
            else:
                time.sleep(0.1)
        except Exception:
            time.sleep(0.1)
    
thread = threading.Thread(target=dumpSerial, daemon=True)
thread.start()

initUi()

# Names of first 2 gamepads we see so they do not get mixed up
pad_name=['','']
pad_id=['','']
pad_mapping=['','']
pad_connected=[False,False]

def showControllerInfo():
    if pad_connected[0]:
        labelCtr1Status.config(text='Connected', fg='#0c0')
        labelCtr1Name.config(text=f'{pad_name[0]}:{pad_id[0]}')
    else:
        labelCtr1Status.config(text='Disconnected', fg='#888')
        labelCtr1Name.config(text='')
    if pad_connected[1]:
        labelCtr2Status.config(text='Connected', fg='#0c0')
        labelCtr2Name.config(text=f'{pad_name[1]}:{pad_id[1]}')
    else:
        labelCtr2Status.config(text='Disconnected', fg='#888')
        labelCtr2Name.config(text='')

pygame.init()

# Implementation is based on example code for joystick module:
# https://www.pygame.org/docs/ref/joystick.html
def controllerThread():
    global pad_name, pad_id, pad_mapping, pad_connected

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    btns = [0,0]
    done = False
    while not done:
        btns_old = btns.copy()

        try:
            pygame_events = pygame.event.get()
        except:
            # Terminate this loop so that the thread can finish
            break

        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame_events:
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy

                # Look for an empty slot
                for i in range(2):
                    if pad_connected[i] == True:
                        continue

                    pad_id[i] = joy.get_instance_id()
                    pad_name[i] = f"{joy.get_name()}"

                    # Check if we have defined a button mapping for this controller
                    if joy.get_name() in button_mappings:
                        pad_mapping[i] = button_mappings[joy.get_name()]
                    else:
                        pad_mapping[i] = button_mappings['Default']

                    pad_connected[i] = True;
                    break

                showControllerInfo()
                print(f"Joystick {joy.get_instance_id()} connected [{joy.get_name()}:{joy.get_guid()}]")

            if event.type == pygame.JOYDEVICEREMOVED:
                # Unregister controller
                del joysticks[event.instance_id]

                # Look for slot
                for i in range(2):
                    if pad_id[i] == event.instance_id:
                        pad_name[i] = ""
                        pad_id[i] = ""
                        pad_mapping[i] = ""
                        pad_connected[i] = False
                        break
                showControllerInfo()
                print(f"Joystick {event.instance_id} disconnected")

            if event.type == pygame.JOYBUTTONDOWN:
                print(f'Joystick {event.instance_id} button pressed: {event.button}')
                # We only need to handle the button event if it's for a controller that is connected.
                for i in range(2):
                    if pad_id[i] == event.instance_id:
                        if event.button in pad_mapping[i]:
                            btns[i] |= 1 << pad_mapping[i][event.button]
                        break

            if event.type == pygame.JOYBUTTONUP:
                print(f'Joystick {event.instance_id} button released: {event.button}')
                # We only need to handle the button event if it's for a controller that is connected.
                for i in range(2):
                    if pad_id[i] == event.instance_id:
                        if event.button in pad_mapping[i]:
                            btns[i] &= ~(1 << pad_mapping[i][event.button])
                        break

            if event.type == pygame.JOYHATMOTION:
                print(f'Joystick {event.instance_id} hat motion: {event.value}')
                # We only need to handle the hatmotion event if it's for a controller that is connected.
                for i in range(2):
                    if pad_id[i] == event.instance_id:
                        # (x,y) 
                        # x -> -1 = Left, 1 = Right
                        # y -> -1 = Down, 1 = Up

                        # Clear buttons
                        btns[i] &= ~(1 << 4)
                        btns[i] &= ~(1 << 5)
                        btns[i] &= ~(1 << 6)
                        btns[i] &= ~(1 << 7)

                        # Check the X-axis
                        if event.value[0] == 1:
                            btns[i] |= 1 << 7
                        if event.value[0] == -1:
                            btns[i] |= 1 << 6

                        # Check the Y-axis
                        if event.value[1] == 1:
                            btns[i] |= 1 << 4
                        if event.value[1] == -1:
                            btns[i] |= 1 << 5
                        break

        if btns[0] != btns_old[0] or btns[1] != btns_old[1]:
            print("Buttons: {0:02x}, {1:02x}".format(btns[0], btns[1]))
            b=bytearray(b'\x02')
            b.append(btns[0])
            b.append(btns[1])
            # print(b)
            connectSerial()
            ser.write(b)
            ser.flush()

        # Limit to 30 frames per second.
        clock.tick(30)

thread2 = threading.Thread(target=controllerThread, daemon=True)
thread2.start()

# Show main GUI interface
top.mainloop()

pygame.quit()
