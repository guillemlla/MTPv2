#This file is for the declaration of the constatns tha we use in all the classes

from lib_nrf24 import NRF24

LOCAL_ADDRESS = 1


#File locations
FILE_DIR = "TXFILE-C-SRO.txt"
SR_FILE_NAME="TXFILE-C-SRI-1.txt"


#Modes that we can be at
TX_MODE = 1
RX_MODE = 2
NETWORK_MODE = 3

#Network mode Constants
NETWORK_PAQUET_TYPE_CONTROL = 0
NETWORK_PAQUET_TYPE_DATA = 1
NETWORK_PAQUET_TYPE_PASSTOKEN = 3

NETWORK_PAQUET_CONTROL_HELLO_PAYLOAD = 0
NETWORK_PAQUET_CONTROL_REPLY_YES_PAYLOAD = 1
NETWORK_PAQUET_CONTROL_REPLY_NO_PAYLOAD = 2

#Rx and Tx Constants
PACKET_SIZE = NRF24.MAX_PAYLOAD_SIZE
PAYLOAD_SIZE_UNICAST = PACKET_SIZE - 1
HEADER_SIZE_MULTICAST = 2
PAYLOAD_SIZE_MULTICAST = 30
CHANNEL = 0x60
RETRY = (5,0)
BEGIN = (0,22)
TIMEOUT = 0.0015 #In seconds
PIPES = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
DATARATE = NRF24.BR_250KBPS
PA_LEVEL = NRF24.PA_LOW
AUTO_TRACK = False

#GPIO
LED_1 = 18 #Is Tx
LED_2 = 16 #Is Rx
LED_3 = 7 #Sending /Recieving
LED_4 = 5 #Is network mode
LED_5 = 3 #Error

SW_1 = 31 #Network mode == 1
SW_2 = 33 # Tx == 0 or Rx == 1
SW_3 = 35
SW_4 = 37
SW_5 = 36
SW_6 = 38
SW_7 = 40 #On if Antena conected

BTN_1 = 8 #restart of the raspberry
BTN_2 = 10 #When the device is ready push to begin transmission
BTN_3 = 12
