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
	In 5910 Lab
	RaspberryPi
	Server_UDP_IP = "192.168.1.56" 
	Server_UDP_PORT = 7777
	Arduino
	Client_UDP_IP = "192.168.1.145"
	Client_UDP_PORT = 5555
---------------------------------------------------------------
Log:

---------------------------------------------------------------
"""
import socket, time

def GetWeatherDataFromESP8266():
	Server_UDP_IP = "192.168.1.56"
	Server_UDP_PORT = 7777
	Receive_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Receive_Sock.bind((Server_UDP_IP, Server_UDP_PORT))
	data, addr = Receive_Sock.recvfrom(1024) # buffer size is 1024 bytes
	if(Receive_Sock.recvfrom(1024)):
		print("received message: ")
		print(data)
	'''
	#No need to talk to the client.
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Send_Sock.sendto(MESSAGE.encode('utf-8'), (Client_UDP_IP, Client_UDP_PORT))
	Send_Sock.close()
	'''
	Receive_Sock.close()
	return data.decode("utf-8")
def SendingMessageToESP8266():
	Client_UDP_IP = "192.168.1.145"
	Client_UDP_PORT = 5555
	MESSAGE = "Hello this is raspberry pi!"
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet, # UDP
	Send_Sock.connect(Client_UDP_IP,Client_UDP_PORT)
	Send_Sock.send("Hello!".encode('utf-8'))
	#Send_Sock.sendto(MESSAGE.encode('utf-8'), (Client_UDP_IP, Client_UDP_PORT))
	print("The message is Sent")
	Send_Sock.close()
if __name__ == '__main__':
	while(1):
		#GetWeatherDataFromESP8266()
		SendingMessageToESP8266()
		time.sleep(1)
	
	
