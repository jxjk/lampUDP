#!/bin/sh
cd ~/Documents/Adafruit/rpi_ws281x/python/examples
# chmod 777 ./TCPServer.py
chmod 777 ./UDPServer.py
# sudo python3 TCPServer.py -c
sudo python3 UDPServer.py -c
echo "TCPServere start ......"
