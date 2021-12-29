"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:RaspberryPi_IntermediateServer.py
related file:
function:Get weather data from ESP8266 client to RaspberryPi UDP server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
	In 5910 Lab
	RaspberryPi
	Server IP = "192.168.1.56" 
	Serve PORT = 7777
	ESP8266
	Client IP = "192.168.1.145"
	Client PORT = 5555
---------------------------------------------------------------
Log:
add SendingMessageToFloatChamber() function to control the electrical power on the float chamber.
---------------------------------------------------------------
"""
import socket, time

def GetWeatherDataFromGroundStation():
	#Get Weather Data From ESP8266 on the ground station
	Server_UDP_IP = "192.168.1.56"
	Server_UDP_PORT = 7777
	Receive_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Receive_Sock.bind((Server_UDP_IP, Server_UDP_PORT))
	data, addr = Receive_Sock.recvfrom(1024) # buffer size is 1024 bytes
	if(Receive_Sock.recvfrom(1024)):
		print("received message: ")
		print(data)

	Receive_Sock.close()
	return data.decode("utf-8")

def SendingMessageToFloatChamber(command):
	#Send Message To ESP8266 on the Float chamber
	Client_TCP_IP = "192.168.1.145"
	Client_TCP_PORT = 5555
	#MESSAGE = "Hello this is raspberry pi!"
	#Create TCP socket
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet, # TCP
	Send_Sock.connect((Client_TCP_IP,Client_TCP_PORT))
	#Check the command
	if command==ShowVoltage:
		Send_Sock.send(command.encode('utf-8'))
	elif command==ShutDown:
		Send_Sock.send(command.encode('utf-8'))
	elif command==PowerUp:
		Send_Sock.send(command.encode('utf-8'))
	print(Send_Sock.recv(200))
	return Send_Sock.recv(200)
	#close the socket
	Send_Sock.close()
	
if __name__ == '__main__':
	while(1):
		#GetWeatherDataFromGroundStation()
		SendingMessageToFloatChamber()
		time.sleep(1)
	
	
