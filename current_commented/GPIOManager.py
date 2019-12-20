#This file is in charge of the managin of the gpios, there are functions for
#initializing the gpios, for setting parametes of determined gpios and change
#the mode in function of determined gpios

import Constants as CTE
import RPi.GPIO as GPIO

#Detects the position of the switches and change the mode base on the position
def getMode():
    sw_1 = GPIO.input(CTE.SW_1)
    sw_2 = GPIO.input(CTE.SW_2)
    if not sw_1 and not sw_2:
        return CTE.TX_MODE
    elif not sw_1 and sw_2:
        return CTE.RX_MODE
    else:
        return CTE.NETWORK_MODE

#If the antenna is ready, returns true
def isAntennaReady():
    if GPIO.input(CTE.SW_7) == 1:
        return True

#Changes the leds based on the mode selected, transmitter have the first led open
# and the receiver have the second led open, otherwise all leds are off
def setLEDsMode(mode):
    if mode == CTE.TX_MODE:
        setLeds(True, False, False)
    elif mode == CTE.RX_MODE:
        setLeds(False, True, False)
    else:
        setLeds(False, False, True)

#if the button is pressed, it returns true
def buttonPressed(buttonGPIO):
    while True:
        if GPIO.input(buttonGPIO):
            return True

#Sets on/off a specified led
def setLed(led, isOn):
    boolTranslation = {
        True: GPIO.HIGH,
        False: GPIO.LOW
    }
    GPIO.output(led, boolTranslation[isOn])

#Set all the three leds on/off based on the booleans that we put on the parameter
def setLeds(led1,led2,led3):
    setLed(CTE.LED_1,led1)
    setLed(CTE.LED_2,led2)
    setLed(CTE.LED_3,led3)

#Change to on or off the send led
def changeSendLed(state):
    setLed(CTE.LED_4,state)

#Change to on or off the connected led
def setLedConected():
    setLed(CTE.LED_5,True)

#This function setup all the gpios needed for the device, selects which one are the inputs and
# outputs and initializes all of them
def gpioSetup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    gpioOut = {CTE.LED_1, CTE.LED_2, CTE.LED_3, CTE.LED_4, CTE.LED_5}
    gpioIn = {CTE.SW_1, CTE.SW_2, CTE.SW_3, CTE.SW_4, CTE.SW_5, CTE.SW_6, CTE.SW_7, CTE.BTN_1, CTE.BTN_2, CTE.BTN_3}

    for gpio in gpioOut:
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, GPIO.LOW)

    for gpio in gpioIn:
        GPIO.setup(gpio, GPIO.IN)

    mode = getMode()
    setLEDsMode(mode)
    print("[*] We are in mode ", mode)
