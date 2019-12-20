# This class creates a buffer of size maxLength and declares de functions for get
# the atributes, all declares a function for filling this buffer with certain data
# and updates its own attibutes, if the buffer is full the function show an error

class Buffer:
    #class builder
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.sizeAvailable = self.maxLength
        self.bufferDataSize = 0
        self.bufferOffset = 0
        self.buffer = []
    #gets for all the atributes
    def getMaxLength(self):
        return self.maxLength

    def getSizeAvailable(self):
        return self.sizeAvailable

    def getBufferDataSize(self):
        return self.bufferDataSize

    def getBuffer(self):
        return self.buffer

    #This get returns the attribute as bytearray
    def getBufferString(self):
        return bytearray(self.buffer)

    def getBufferOffset(self):
        return self.bufferOffset

    #fills the buffer with certain data and updates its own attibutes,
    #if the buffer is full the function show an error
    def fillBuffer(self, data):
        L = len(data)

        if(L > self.sizeAvailable):
            print("Not available memory space!")
        else:
            self.buffer[self.bufferOffset:(self.bufferOffset + L)] = data
            self.bufferOffset = self.bufferOffset + L
            self.bufferDataSize = len(self.buffer)
            self.sizeAvailable = self.sizeAvailable - L
