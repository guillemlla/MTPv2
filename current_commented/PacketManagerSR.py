import Exceptions
import Constants as CTE
import array


#Creates the unicast packet with the header, converts the data to binary and
#returns all the packet, if the Payload is greater than the spected packet size
#it raises an error
def createUnicastPacket(payload, sequenceNumber, isACK, isEnd):
    #If the payload is type int it changes to string
    if type(payload) == int:
        payload = str(payload)

    #Create and add the header to the data packet
    header = createUnicastHeader(sequenceNumber, isACK, isEnd)
    data = [header]

    #Converts the payload to binary and adds the payload to the data packet
    payloadBinary = array.array('B', payload).tolist()
    data.extend(payloadBinary)
    #If the data packet is longer thant the packet sizes it raises an exeception
    #otherwise it returns the data
    if len(data) <= CTE.PACKET_SIZE:
        return data
    else:
        raise Exceptions.WrongPayloadSize()


# HEADER
# 00:0-> packet 0 01:1->ACK packet 0
# 10:2-> packet 1 11:3 -> ACK packet 1
def createUnicastHeader(sequenceNumber, isACK, isEnd):
    header = boolToNum(isACK) + (sequenceNumber << 1) + (boolToNum(isEnd) << 2)
    return header

#Reads the unicast packet, first read the header and extract the sequenceNumber,
#isACK and isEnd parameters from there, extracts the payload and it converts to
# string and return the payload, the sequenceNumber, and the booleans isACK and isEnd
def readUnicastPacket(packet):
    sequenceNumber, isACK, isEnd = readUnicastHeader(packet[0])
    payload = packet[1:len(packet)]
    payload = arrayToString(payload)
    return payload, sequenceNumber, isACK, isEnd

#From an array of bytes it converts to a string
def arrayToString(arrayBytes):
    new = ""
    for x in arrayBytes:
        new += chr(x)
    return new

#Extract sequenceNumber, isEnd and isACK from the headers
def readUnicastHeader(header):
    isEnd = header >> 2
    sequenceNumber = header >> 1 & 0x1
    isACK = header & 0x1
    return sequenceNumber, bool(isACK), bool(isEnd)

#Creates a network packet based on the source, the destinations, if it is ACK,
#the sequenceNumber and the packetType. Converts the playload to binary
def createNetworkPacket(payload, source, dest1, dest2, isACK, sequenceNumber, packetType):
    data = createNetworkHeader(source, dest1, dest2, isACK, sequenceNumber, packetType)
    payloadBinary = array.array('B', payload).tolist()
    data.extend(payloadBinary)
    if len(data <= CTE.PACKET_SIZE):
        return data
    else:
        raise Exceptions.WrongPayloadSize()

#Extract the parameters from the header and the payload from the packet
def readNetworkPacket(packet):
    source, dest1, dest2, isACK, sequenceNumber, packetType = readNetworkHeader(packet[0:2])
    payload = packet[2:len(packet)]
    return payload, source, dest1, dest2, isACK, sequenceNumber, packetType

#Based on the specified parameters it creates the network header
def createNetworkHeader(source, dest1, dest2, isACK, sequenceNumber, packetType):
    first = source << 4 | dest1
    second = (boolToNum(isACK) << 7) | (sequenceNumber << 6) | (dest2 << 2) | packetType
    return [first, second]

#Id reads the network header and extract the parameters
def readNetworkHeader(header):
    source = header[0] >> 4
    dest1 = header[0] & 15
    isACK = header[1] >> 7
    sequenceNumber = (header[1] >> 6) & 1
    dest2 = (header[1] >> 2) & 15
    packetType = header[1] & 3
    return source, dest1, dest2, bool(isACK), sequenceNumber, packetType

#Maps a boolean to a int
def boolToNum(boolVar):
    mapper = {
        False: 0,
        True: 1
    }
    return mapper[boolVar]

#Maps a int to a boolean 
def numToBool(num):
    mapper = {
        0: False,
        1: True
    }
    return mapper[num]
