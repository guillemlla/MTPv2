import GPIOManager as gpio
import Exceptions
import Constants as CTE
import Tx as Tx
import Rx as Rx


def begin():
    gpio.gpioSetup()
    mode = gpio.getMode()
    gpio.setLEDsMode(mode)

    gpio.buttonPressed(CTE.BTN_1)
    gpio.setLeds(True, True, True)

    if mode == CTE.TX_MODE:
        tx = Tx.Tx()
        tx.sendData()
    elif mode == CTE.RX_MODE:
        rx = Rx.Rx()
        rx.receiveData()
    elif mode == CTE.NETWORK_MODE:
        i = 1
        #do whatever
    else:
        raise Exceptions.ModeError()

    gpio.setLeds(False, True, False)

try:
    begin()
except Exceptions.ModeError():
    print("Error in the mode")
