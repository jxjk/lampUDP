# -*- coding: utf-8 -*-
import socket
import socketserver
import time
from threading import Thread
"""
from neopixel import *
import RPi.GPIO as GPIO
from configparser import ConfigParser 


GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
"""


# LED strip configuration:
LED_COUNT      = 256 # Number of LED pixels.
"""
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
"""

def showLed():
    print('showLed')
    global s,e,r,g,b,flg
    while flg:
        print(s,e,r,g,b)
        time.sleep(2)
        """
        for i in range(int(e)):
            strip.setPixelColor(int(s)+i, Color(int(r),int(g),int(b)))
        strip.show()
        GPIO.output(10,True)
        time.sleep(0.5)
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        GPIO.output(10,False)
        """


serverPort = 50007
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive.')
while 1 :
    try:
        connectionSocket,addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        sent = sentence.decode("utf-8")

        # 通讯确认
        if sent== '?':
            capitalizedSentence = b'!'
        elif (sent== 'C') or (sent== 'c'):
            s,e,r,g,b,flg = 0,LED_COUNT,0,0,0,False
            capitalizedSentence = b'C'
            t = Thread(target=showLed)
            t.start()
        else:
            try:
                s,e,r,g,b = sent.split(',')
                flg = True
                capitalizedSentence = sentence 
                t = Thread(target=showLed)
                t.start()
            except:
                capitalizedSentence = b'-1'

        connectionSocket.send(capitalizedSentence)
        connectionSocket.close()
    except:
        flg = False
