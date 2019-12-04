import subprocess
import time
import os
import Constants as CTE
import Exceptions as exceptions
import shutil


def checkState():
    rpistr = "ls /media/pi"
    USB_name = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid,stdout=subprocess.PIPE)
    line = USB_name.stdout.readline()
    if line:
        return True
    else:
        return False


def getFromUSB():
    waitToUsbConnected()
    usbPath = "/media/pi/"
    usb = os.listdir(os.path.dirname(usbPath))[0]
    filename = os.listdir(os.path.join(usbPath, usb))[0]
    shutil.move(filename, os.getcwd())


def putOnUSB():
    waitToUsbConnected()
    usbPath = "/media/pi/"
    shutil.move(os.path.join(os.getcwd(), CTE.FILE_DIR), usbPath)


def waitToUsbConnected():
    while not checkState():
        time.sleep(0.1)


def openWriteFile():
    filePointer = open(CTE.FILE_DIR, "w+b")
    return filePointer


def writeBytes(data, filePointer):
    return filePointer.write(data)


def openReadFile():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            filePath = os.path.join(os.getcwd(), file)
            filePointer = open(filePath, "r+b")
            return filePointer
        else:
            print("[*] File not found")
            raise exceptions.NotFileFound()


def getBytes(size, filePointer):
    return filePointer.read(size)

