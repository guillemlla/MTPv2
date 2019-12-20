#Initialization file where we setup all the gpios and calls one class or another
#based on the selected mode by the means of the switches


import GPIOManager as gpio
import Exceptions
import Constants as CTE
import Tx as Tx
import Rx as Rx
import main as main
import USBManager as USBManager


#Initialization function
def begin():
    #Setup the gpios, gets the mode and changes the leds based on the mode
    gpio.gpioSetup()
    mode = gpio.getMode()
    gpio.setLEDsMode(mode)

    #Waits until the button is pressed and afterwards set all the leds on
    gpio.buttonPressed(CTE.BTN_1)
    gpio.setLeds(True, True, True)

    #Based on the selected mode initialize one class or another, if it enters a
    #mode not declared it raises a ModeError Exception
    if mode == CTE.TX_MODE:
        tx = Tx.Tx()
        tx.sendData()
    elif mode == CTE.RX_MODE:
        rx = Rx.Rx()
        rx.receiveData()
    elif mode == CTE.NETWORK_MODE:
        main.startNetworkMode(USBManager.is_usb_connected())
    else:
        raise Exceptions.ModeError()

    #When finish set on the second led and all the others off
    gpio.setLeds(False, True, False)

try:
    begin()
except Exceptions.ModeError():
    print("Error in the mode")
