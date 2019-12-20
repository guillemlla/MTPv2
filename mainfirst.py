from NetworkModeFSM import NetworkModeFSM
from RFfunctions import config_radio
from NetworkModeCTE import *
radio = config_radio(channel=NETWORK_CHANNEL, power = NETWORK_PA_LEVEL, rate= NETWORK_DATARATE)
networkfsm = NetworkModeFSM(

    
    {"addr": NETWORK_SELF_ADDR, "first_tx": False, "token_pl": [], "reply_yes": [], "reply_no": [], "retransmission": 0, "data": [], "src_token": None, "polling_addr": None},
    NETWORK_FILENAME_OUTPUT,
    radio,
    useUSB=False, first=True
    )
