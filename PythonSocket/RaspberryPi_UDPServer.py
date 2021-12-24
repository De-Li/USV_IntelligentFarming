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
	Server_UDP_IP = "192.168.1.56"
	Server_UDP_PORT = 7777
	Client_UDP_IP = "192.168.1.145"
	Client_UDP_PORT = 5555

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	sock.bind((Server_UDP_IP, Server_UDP_PORT))
	MESSAGE = "Hello this is server!"
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print("received message: %s" % data)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
		sock.sendto(MESSAGE, (Client_UDP_IP, Client_UDP_PORT))
	
if __name__ == '__main__':
	while(1):
		GetWeatherDataFromESP8266()
		time.sleep(1)
	
	
