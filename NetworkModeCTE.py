from lib_nrf24 import NRF24

# Number of nodes to participate in the Network Mode
NETWORK_SIZE = 8

# Addres of the node (TO BE CHANGED UPON NODE)
NETWORK_SELF_ADDR = 3 
# Broadcast address
NETWORK_BROADCAST_ADDR = 0

MAX_RETRIES_POLL = 5
EOT_SEND_RETRIES = 20
# TIMEOUT VALUES
TIMEOUT_DATA = 15
TIMEOUT_DATA_ACK = 0.2 #0.06

TIMEOUT_TOKEN = 15 #2
TIMEOUT_TOKEN_ACK = 0.2 #0.06

TIMEOUT_HELLO = 2 #0.5
TIMEOUT_HELLO_REPLY = 0.2 #0.01

# The size of each packet will be 32 Bytes. The header length
# will be 2 Bytes
PACKET_LENGTH = 32
NETWORK_HEADER_SIZE = 2
SRI_HEADER_SIZE = 1
NETWORK_PAYLOAD_SIZE = PACKET_LENGTH - NETWORK_HEADER_SIZE
SRI_PAYLOAD_SIZE = PACKET_LENGTH - SRI_HEADER_SIZE

# ISACK field values
PACKET_FIELD_ISACK_NO_ACK = 0
PACKET_FIELD_ISACK_YES_ACK = 1

# Initial sequence number
PACKET_FIELD_SN_FIRST = 0

# Values for the different types of packets
NETWORK_PACKET_TYPE_CONTROL = 0
NETWORK_PACKET_TYPE_DATA = 1
NETWORK_PACKET_TYPE_EOF = 2
NETWORK_PACKET_TYPE_PASSTOKEN = 3

# Values for the payload of the different control packets
NETWORK_PACKET_CONTROL_HELLO_PAYLOAD = 0
NETWORK_PACKET_CONTROL_REPLY_YES_PAYLOAD = 1
NETWORK_PACKET_CONTROL_REPLY_NO_PAYLOAD = 2
NETWORK_PACKET_CONTROL_EOT_PAYLOAD = 3

# Input filenames (CHANGE THE NAME OF THE FILE UPON TEAM FOR THE SRI)
NETWORK_FILENAME_INPUT = "MTP-F19-NM-TX.txt"
SRI_FILENAME_INPUT = "MTP-F19-SRI-C-TX.txt"

# Output filenames (CHANGE THE NAMES OF THE FILES UPON THE TEAMS AND NODES)
NETWORK_FILENAME_OUTPUT = "MTP-F19-NM-C2-RX.txt"
SRI_FILENAME_OUTPUT = "MTP-F19-SRI-C-RX.txt"

# RF24 constants (NEED TO BE CHANGED UPON MODEL)
NETWORK_CHANNEL = 0x60
SRI_CHANNEL = 0x60
# TODO: WE SHOULD DEFINE THE TMEOUT (THIS IS GENERAL FOR ALL THE PACKETS AND MAY BE TOO MUCH)
#PIPES = [0xe7e7e7e7e7, 0xc2c2c2c2c2]
PIPES = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
NETWORK_DATARATE = NRF24.BR_250KBPS
NETWORK_PA_LEVEL = NRF24.PA_HIGH
SRI_DATARATE = NRF24.BR_2MBPS
SRI_PA_LEVEL = NRF24.PA_HIGH
BEGIN = (0,22)
RETRY = (5,0)

# GPIO related constants (THIS NEEDS TO BE CHANGED FOR EVERY TEAM, MODEL,...
# SOME OF THEM MAY NOT BE EVEN PRESENT, BECAUSE SOME CAN HAVE ONE-COLOUR
# ONLY LED, A BUTTON INSTEAD OF A SWITCH,...)
# Pins of the switches
SWITCH_PIN_ON_OFF = 26
SWITCH_PIN_TX_RX = 33
SWITCH_PIN_SRI_NW = 31

# Pins of the LEDs
COMMLED_PIN_0 = 21
COMMLED_PIN_1 = 16
COMMLED_PIN_2 = 20

BLINKLED_PIN = 12
