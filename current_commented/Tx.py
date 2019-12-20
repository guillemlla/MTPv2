import FancyDataSender as FancyDataSender
import Constants as CTE
import PacketManagerSR as pm
import USBManagerSR as USBManager
import GPIOManager as gpio

class Tx:

    #Initiliaze the class and obtain the dataSender with the local address
    def __init__(self):
        self.dataSender = FancyDataSender.UnicastDataSender(CTE.LOCAL_ADDRESS)
        self.sequenceNumber = 0
	    self.sendLedState = False

    #Creates an unicastpacket and send the packet, change the states of the leds
    def sendPacket(self, data, isEnd):
        #Create the packet
        packet = pm.createUnicastPacket(data, self.dataSender.getSequenceNumber(), False, isEnd)
        #Waits until the packet is sent
        packetSend = False
        while not packetSend:
            packetSend = self.dataSender.sendData(packet)
        #Change the led states
	    self.changeSendLedState()
        gpio.setLedConected()

    #Gets the file from the usb, starts reading the file and sends a payload of data
    def sendData(self):
        #Read the file from the usb
        USBManager.getFromUSB()

        #Creates a pointer to the file and reads a payload size of bytes from the file
        # and sends the packet, if the payload of bytes is empty, it send an EndPacket
        isEnd = False
        filePointer = USBManager.openReadFile()
        while not isEnd:
            data = USBManager.getBytes(CTE.PAYLOAD_SIZE_UNICAST, filePointer)
            if data == '':
                isEnd = True
                self.sendEndPacket()
            else:
                self.sendPacket(data, isEnd)

    #Creates end type packet and waits until it sends it
    def sendEndPacket(self):
        packet = pm.createUnicastPacket(" ", self.dataSender.getSequenceNumber(), False, True)
        packetSend = False
        while not packetSend:
            packetSend = self.dataSender.sendData(packet)

    #If the led was off it turns on and viceversa        
    def changeSendLedState(self):
    	if self.sendLedState == True:
    		self.sendLedState = False
    	else:
    		self.sendLedState = True
    	gpio.changeSendLed(self.sendLedState)
