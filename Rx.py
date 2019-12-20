import FancyDataSender as FancyDataSender
import PacketManagerSR as pm
import Constants as CTE
import USBManagerSR as USBManager
import GPIOManager as gpio


class Rx:

    #Initiliaze the class and obtain the dataSender with the local address
    def __init__(self):
        self.dataSender = FancyDataSender.UnicastDataSender(CTE.LOCAL_ADDRESS)
 	    self.oldPayload = None

    #Receive packets and extract all the information
    def receivePacket(self):
        #Receive a packet and extract the payload and all the parameters from it
        packet = self.dataSender.receiveMessage()
        payload, sequenceNumber, isACK, isEnd = pm.readUnicastPacket(packet)

        #Turn the conected led on
        gpio.setLedConected()

        #If is not an ACK, the sequenceNumber does not match with the old one
        # and the payload is not the same as the old one, it sends and ACK with
        #the sequenceNumber and updates the variables
        if not isACK and sequenceNumber == self.dataSender.getSequenceNumber() and not payload == self.oldPayload:
            self.dataSender.sendACK(sequenceNumber)
            print("[*] Packet Recived and ACK Send SequenceNumber: ",sequenceNumber," isAck:",isACK)
	        self.oldPayload = payload
            return payload, isEnd
        #If the transmitter fails to receive the ACK and resends again the same
        #packet after a timeout, it resends the ACK
        elif not isACK and not sequenceNumber == self.dataSender.getSequenceNumber() and payload == self.oldPayload:
            self.dataSender.changeSequenceNumber()
            self.dataSender.sendACK(sequenceNumber)
            print("Re-SendACK SequenceNumber: ", sequenceNumber, " isAck: ",isACK)
            return None,isEnd
        #If it receives an ACK that is not valid
        else:
            print("[*] ACK not valid")
            return None,isEnd

    #Open the file that we want to write, and writes the packets until the packet
    #is isEnd
    def receiveData(self):
        end = False
        #Pointer to the file that we want to write
        filePointer = USBManager.openWriteFile()

        #Writing the bytes until the it receceives a isEnd packet
        while not end:
            data, isEnd = self.receivePacket()
            if data is not None:
                USBManager.writeBytes(data, filePointer)
            end = isEnd

        print("[*] File received")
#        USBManager.putOnUSB()
