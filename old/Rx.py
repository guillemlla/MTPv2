import FancyDataSender as FancyDataSender
import PacketManager as pm
import Constants as CTE
import USBManager


class Rx:

    def __init__(self):
        self.dataSender = FancyDataSender.UnicastDataSender(CTE.LOCAL_ADDRESS)

    def receivePacket(self):
        packet = self.dataSender.receiveMessage()
        payload, sequenceNumber, isACK, isEnd = pm.readUnicastPacket(packet)
        if not isACK and sequenceNumber == self.dataSender.getSequenceNumber():
            self.dataSender.sendACK()
            return payload, isEnd
        else:
            print("[*] ACK not valid")
            return None

    def receiveData(self):
        end = False
        filePointer = USBManager.openWriteFile()

        while not end:
            data, isEnd = self.receivePacket()
            if data is not None:
                USBManager.writeBytes(data, filePointer)
            end = isEnd

        print("[*] File received")
        USBManager.putOnUSB()





