"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:RaspberryPi_UDPServer.py
related file:
function:Get weather data from ESP8266 client to RaspberryPi UDP server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:

---------------------------------------------------------------
Log:

---------------------------------------------------------------
"""
import socket, time

def GetWeatherDataFromESP8266():
	UDP_IP = ""
	UDP_PORT = 7777

	sock = socket.socket(socket.AF_INET, # Internet
						 socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
 
while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print("received message: %s" % data)
	
if __name__ == '__main__':
	while(1):
		GetWeatherDataFromESP8266()
		time.sleep(1)
	
	
