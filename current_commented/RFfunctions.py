import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import time
from NetworkModeCTE import *

#configure radio with constants imported from NetworkModeCTE
def config_radio(channel, power, rate, autoAck=False, ce=25, csn=8):
    GPIO.setmode(GPIO.BOARD)
    radio = NRF24(GPIO, spidev.SpiDev())
    print("[*] Starting Radio Interface...")
    radio.begin(BEGIN[0], BEGIN[1])
    radio.setRetries(RETRY[0], RETRY[1])
    radio.setPayloadSize(PACKET_LENGTH)
    radio.setChannel(channel)
    radio.setDataRate(rate)
    radio.setPALevel(power)
    radio.setAutoAck(autoAck)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.stopListening()
    radio.printDetails()
    return radio

#send data through antenna previously configured
def send_radio_packet(data, radio,pipe_tx):
    radio.stopListening()
    #radio.openWritingPipe(pipe_tx)
    time.sleep(0.01)
    radio.write(data)


#change array of bytes to string
def arrayToString(arrayBytes):
    new = ""
    for x in arrayBytes:
        new += chr(x)
    return new

#wait radio packet, Rx will wait till one arrives
def wait_radio_packet(radio,pipe_rx):
    #radio.openReadingPipe(1,pipe_rx)
    radio.startListening()
    while not radio.available():
        time.sleep(0.001) #0.0001
    packet=[]
    radio.read(packet,radio.getPayloadSize())
    radio.stopListening()
    #radio.closeReadingPipe(1)
    return packet

#Wait till a timeout is reached
def wait_radio_packet_timeout(radio,pipe_rx, timeout):
    #radio.openReadingPipe(1,pipe_rx)
    radio.startListening()
    time_first = time.time()
    packet = None
    timeout_reached = False
    while not radio.available():
        time.sleep(0.001)  #0.0001
        time_actual = time.time()
        if time_actual >= time_first + timeout:
            timeout_reached = True
            break

    if not timeout_reached:
	packet=[]
        radio.read(packet,radio.getPayloadSize())

    radio.stopListening()
    #radio.closeReadingPipe(1)
    return packet, timeout_reached

def close_radio(radio):
    radio.stopListening()
