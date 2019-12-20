#This files have the classes BaseDataSender, NetworkDataSender and UnicastDataSender
# with all the functions and constructors needed for sending the data, with ACK
# and TIMEOUT implemented


import Constants as CTE
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import signal, spidev, time
import PacketManagerSR as pm
import Exceptions
import time


class BaseDataSender:

    #The constructor fo this class and calls the initializator of the radio
    def __init__(self, address):
        self.sequenceNumber = 0
        self.numPackets = 0
        self.address = address
        self.radio = self.initRadio()
        self.startTime = 0

    #With the data that we pass for parameter, stops the listening of the radio
    #writes the data in the radio, prints the number of paquets sent and starts
    #listening until it receives an ACK or TIMEOUT
    def sendData(self, data):
        self.radio.stopListening()
        self.radio.write(data)
        print("[*] Packet ", self.numPackets, " Send")
        self.radio.startListening()
        return self.waitForACK()


    #Starts a counter an waits until it receives a valid ACK and returns TRUE
    #if not, returns FALSE
    def waitForACK(self):
        self.startTime = time.time()
        try:
            file = self.receiveMessageWithTimeout()
            while not self.isCorrectACK(file):
                file = self.receiveMessageWithTimeout()
            self.changeSequenceNumber()
            return True
        except Exceptions.TimeoutError:
            return False

    #Check what time is now and it compares with the start time of the class,
    #if it is bigger than what we declared as a TIMEOUT in the constants, it raise
    #an error.
    def checkTime(self):
        now = time.time()
        if now - self.startTime > CTE.TIMEOUT:
            raise Exceptions.TimeoutError


    #Wait some time and checks if there is payload at the pipe, if not, waits more
    #until it reach the TIMEOUT time
    def receiveMessageWithTimeout(self):
        pipe = [0]
        while not self.radio.available(pipe):
            time.sleep(5/10000)
            self.checkTime()
        file = []
        self.radio.read(file, self.radio.getPayloadSize())
        return file

    #Wait some time and checks if there is payload at the pipe, if not, waits more
    #but this time does not check the TIMEOUT time
    def receiveMessage(self):
        pipe = [0]
        while not self.radio.available(pipe):
            time.sleep(5/10000)
        file = []
        self.radio.read(file, self.radio.getPayloadSize())
        return file

    #Prints which packet is have TIMEOUT and raise a TimeoutError Exception
    def timeoutHandler(self, signum, frame):
        print("[*] Packet ", self.numPackets, " Timeout")
        raise Exceptions.TimeoutError

    #If the sequenceNumber is 0 it changes to 1, otherwise it changes to 0
    def changeSequenceNumber(self):
        if self.sequenceNumber == 0:
            self.sequenceNumber = 1
        else:
            self.sequenceNumber = 0

    #If the ACK is correct, raises a NotImplementedError
    def isCorrectACK(self, data):
        raise NotImplementedError

    #send ack manually
    def sendACK(self,sequenceNumber):
        packet = pm.createUnicastPacket("", sequenceNumber, True, False)
        self.radio.stopListening()
        self.radio.write(packet)
        self.radio.startListening()
        self.changeSequenceNumber()

    #initialize radio
    @staticmethod
    def initRadio():
        radio = NRF24(GPIO, spidev.SpiDev())
        print("[*] Starting Radio Interface...")
        radio.begin(CTE.BEGIN[0], CTE.BEGIN[1])
        radio.setRetries(CTE.RETRY[0], CTE.RETRY[1])
        radio.setPayloadSize(CTE.PACKET_SIZE)
        radio.setChannel(CTE.CHANNEL)
        radio.setDataRate(CTE.DATARATE)
        radio.setPALevel(CTE.PA_LEVEL)
        radio.setAutoAck(CTE.AUTO_TRACK)
        radio.enableDynamicPayloads()
        radio.enableAckPayload()
        radio.openWritingPipe(CTE.PIPES[0])
        radio.openReadingPipe(1, CTE.PIPES[1])
        radio.startListening()
        radio.stopListening()
        radio.startListening()
        radio.printDetails()
        return radio

    def getSequenceNumber(self):
        return self.sequenceNumber

#Class not used in the final mode
class NetworkDataSender(BaseDataSender):
    def isCorrectACK(self, data):
        source, dest1, dest2, isACK, sequenceNumber, packetType = pm.readNetworkHeader(data)
        if isACK and dest2 == self.address:
            return True

#Class not used in the final Mode
class UnicastDataSender(BaseDataSender):
    def isCorrectACK(self, data):
        sequenceNumber, isACK, isEnd = pm.readUnicastHeader(data[0])
        if isACK and sequenceNumber == self.sequenceNumber:
            print("[*] ACK Recived with sequence Number:",sequenceNumber)
            self.numPackets = self.numPackets + 1
            return True
        else:
            print("[*] Erronious ACK")
            return False
