import GPIOManager as gpio
import subprocess
import time
import os
import Constants as CTE
import Exceptions as exceptions
import shutil


def checkState():
    #Check if a new usb is connected and returns a boolean if it is or not
    rpistr = "ls /media/pi"
    USB_name = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
    line = USB_name.stdout.readline()
    if line:
        return True
    else:
        return False


def getFromUSB():
    #Waits until a usb is connected
    waitToUsbConnected()
    #When it is connected turns on a led
    gpio.setLeds(True,False,False)
    #Finds the path of the usb and opens on file that ends with a ".txt"
    usbPath = "/media/pi/"
    usb = os.listdir(os.path.dirname(usbPath))
    usb.sort()
    usb = usb[-1]
    fullPath = os.path.join(usbPath, usb)
    files = os.listdir(fullPath)
    for oneFile in files:
        if oneFile.endswith(".txt"):
            filename = oneFile
    #Turns on a led if find a file
    gpio.setLeds(False,True,False)
    #Waits some time
    time.sleep(1)
    #Copy the file to the local device for send it
    shutil.copy2(os.path.join(fullPath, filename),os.path.join(os.getcwd(),'text2send.txt'))
    #Turns on a all the leds if it make success in copy the file
    gpio.setLeds(True, True, True)
    #Waits some time
    time.sleep(1)
    #Turns off all the leds
    gpio.setLeds(False,False,False)

def putOnUSB():
    #Turns on one led and waits until a usb is connected
    gpio.setLeds(False, False, True)
    time.sleep(1)
    waitToUsbConnected()
    #When a usb is connected turns on the first and the last led and waits some time
    gpio.setLeds(True, False, True)
    time.sleep(1)

    #Finds the path of the usb, change the permissions of the folder and copy
    #the files to the usb
    usbPath = "/media/pi/"
    usb = os.listdir(os.path.dirname(usbPath))
    usb.sort()
    usb = usb[-1]
    fullPath=os.path.join(usbPath, usb)
    gpio.setLeds(True, True, False)
    os.chmod(os.path.join(os.getcwd(), CTE.FILE_DIR), 0o777)
    gpio.setLeds(True, False, False)
    shutil.copy2(os.path.join(os.getcwd(),CTE.FILE_DIR),os.path.join(fullPath,"TextGroupC.txt"))
    gpio.setLeds(True, True, True)

# Waits until the usb is connected, if not, waits some time and checks again
def waitToUsbConnected():
    while not checkState():
   	    time.sleep(0.1)


def openWriteFile():
    #Waits until the usb is connected
    waitToUsbConnected()
    #When the usb is connected turns on the first and the last led and waits some time
    gpio.setLeds(True, False, True)
    time.sleep(1)

    #Finds the path of the usb
    usbPath = "/media/pi/"
    usb = os.listdir(os.path.dirname(usbPath))
    usb.sort()
    usb = usb[-1]
    fullPath=os.path.join(usbPath, usb)

    #Opens the file from the usb for start writing it
    filePointer = open(os.path.join(fullPath,CTE.FILE_DIR), "w+b")
    return filePointer

#Writes the selected bytes from data to the file
def writeBytes(data, filePointer):
    return filePointer.write(data)


def openReadFile():
    #Search in all the files if anyone ends with "text2send.txt"
    for file in os.listdir(os.getcwd()):
        if file.endswith("text2send.txt"):
            #Opens the file
            filePath = os.path.join(os.getcwd(), file)
            filePointer = open(filePath, "r+b")
            #Turns on and off several times and waits
	        gpio.setLeds(True, True, True)
            time.sleep(0.2)
            gpio.setLeds(True,False,False)
            time.sleep(0.2)
            gpio.setLeds(False,True,False)
 	        time.sleep(0.2)
            gpio.setLeds(False,False,True)
            time.sleep(0.2)
            gpio.setLEDsMode(1)
            #Send the pointer from the opened file
            return filePointer

#From the selected file, read a spicified size of data bytes
def getBytes(size, filePointer):
    return filePointer.read(size)
