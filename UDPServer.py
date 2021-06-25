# -*- coding: utf-8 -*-
import socket
# import socketserver
import time
from threading import Thread
from neopixel import *
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.OUT)


# LED strip configuration:
LED_COUNT      = 1024 # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library 1must be called once before other functions).
strip.begin()
# strip.setPixelColor(1, Color(0,0,0))
# strip.show()


def showLed():
    global s,e,r,g,b,flg
    print('flg',flg)
    if flg:
        GPIO.output(11,True)
    else:
        GPIO.output(11,False)
    for i in range(int(e)):
        strip.setPixelColor(int(s)+i,Color(int(r),int(g),int(b)))
    strip.show()
    """
    while flg:
        for i in range(int(e)):
            strip.setPixelColor(int(s)+i,Color(int(r),int(g),int(b)))
        strip.show()
        time.sleep(0.5)
        for i in range(LED_COUNT):
            strip.setPixelColor(i,Color(0,0,0))
        strip.show()
        time.sleep(0.5)
    """


serverPort = 50007
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('The server is ready to receive.')
while 1 :
    print("waiting...")
    sentence,addr = serverSocket.recvfrom(1024)
    sent = sentence.decode("utf-8")

    """
    ## 通讯确认 [?] => [!]
    ## LED灭所有的灯 [C] => [C]
    ## LED点灯 点灯起始位置，红，绿，蓝，点灯数量 
    ##       送信命令 = 返回值 
    ##       例如：[1,255,255,255,5] => [1,255,255,255,5]
    """

    
    print(sent)
    try:
        # 通讯确认
        if sent== '?':
            print('?')
            capitalizedSentence = b'!'
        elif (sent== 'C') or (sent== 'c'):
            print('c')
            s,e,r,g,b,flg  = 0,LED_COUNT,0,0,0,False
            capitalizedSentence = b'C'
            t = Thread(target=showLed)
            t.start()
        else:
            print('s,e,rgb')
            s,e,r,g,b = sent.split(',')
            flg = True
            capitalizedSentence = sentence 
            t = Thread(target=showLed)
            t.start()
        serverSocket.sendto(capitalizedSentence,addr)
    except:
        flg=False
serverSocket.close()
