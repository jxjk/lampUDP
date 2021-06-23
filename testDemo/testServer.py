# -*- coding: utf-8 -*-
import socketserver
import time
# from neopixel import *
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(10,GPIO.OUT)
from threading import Thread 

LED_COUNT      = 256 # Number of LED pixels.
"""
# LED strip configuration:
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
# strip.setPixelColor(1, Color(0,0,0))
# strip.show()

"""
class MySockServer(socketserver.BaseRequestHandler):

    def __init__(self,*args):
        self.s = 0
        self.e = LED_COUNT
        self.r = 0
        self.g = 0 
        self.b = 0
        self.led = False
        self.t = Thread(target = self.showLed)
        self.t.setDaemon(True)
        self.t.start()
        super().__init__(*args)
        
        
    def handle(self):
        print('Got a new connection from ',self.client_address)
        while True:
            try:
                sent = self.request.recv(1024).decode()
            except:
                print('exit')
                self.led = False
                break
            if not sent:break
            print('recv:',sent)
        
            # 通讯确认
            if sent== '?':
                data = b'!'
            elif (sent== 'C') or (sent== 'c'):
                data = b'C'
                self.s = 0
                self.e = LED_COUNT
                self.r = 0
                self.g = 0
                self.b = 0
                self.led = False
            else:
                try:
                    s,e,r,g,b = sent.split(',')
                    data = sent.encode() 
                    self.s = s
                    self.e = e
                    self.r = r
                    self.g = g
                    self.b = b
                    self.led = True
                    self.t = Thread(target = self.showLed)
                    self.t.setDaemon(True)
                    self.t.start()
                except:
                    data = b'-1'

            self.request.send(data)
 
   
    def showLed(self):
        while self.led:
            print('LED ON',self.s,self.e,self.r,self.g,self.b,self.led)
            time.sleep(0.5)
            print('LED OFF')
            time.sleep(0.5)
            """
            for i in range(int(e)):
                strip.setPixelColor(int(s)+i, Color(int(r),int(g),int(b)))
            strip.show()
            GPIO.output(10,True)
            time.sleep(0.5)
            for i in range(LED_COUNT):
                strip.setPixelColor(i, Color(0,0,0))
            GPIO.output(10,False)
            time.sleep(0.5)
            """


if __name__ == '__main__':
    serverHost = ''
    serverPort = 50007
    s = socketserver.ThreadingTCPServer((serverHost,serverPort),MySockServer)
    s.serve_forever()

