import FancyDataSender as FancyDataSender
import Constants as CTE
import PacketManager as pm
import USBManager


class Tx:

    def __init__(self):
        self.dataSender = FancyDataSender.UnicastDataSender(CTE.LOCAL_ADDRESS)
        self.sequenceNumber = 0

    def sendPacket(self, data, isEnd):
        packet = pm.createUnicastPacket(data, self.dataSender.getSequenceNumber(), False, isEnd)
        packetSend = False
        while not packetSend:
            packetSend = self.dataSender.sendData(packet)

    def sendData(self):
        USBManager.getFromUSB()
        isEnd = False
        filePointer = USBManager.openReadFile()
        while not isEnd:
            data = USBManager.getBytes(CTE.PAYLOAD_SIZE_UNICAST, filePointer)
            if data == '':
                isEnd = True
                self.sendEndPacket()
            else:
                self.sendPacket(data, isEnd)

    def sendEndPacket(self):
        packet = pm.createUnicastPacket(" ", self.dataSender.getSequenceNumber(), False, True)
        packetSend = False
        while not packetSend:
            packetSend = self.dataSender.sendData(packet)
