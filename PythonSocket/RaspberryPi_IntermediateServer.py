"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:RaspberryPi_IntermediateServer.py
related file:
function:Let the raspberry pi become the intermediate role to convey the message between main server and endpoint.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
	In 5910 Lab
	RaspberryPi-burned
	Server IP = "192.168.1.56" 
	Serve PORT = 7777
	RaspberryPi-new
	Server IP = "192.168.1.108" 
	Serve PORT = 7777
	ESP8266
	Client IP = "192.168.1.145"
	Client PORT = 5555
	ESP8266-float chamber
	Client IP = "192.168.1.29"
	Client PORT = 5555
---------------------------------------------------------------
Log:
2021/12/29
add SendingMessageToFloatChamber() function to control the electrical power on the float chamber.
add GetCommandFromMainServer() function to receive the command from the main server.
---------------------------------------------------------------
"""
import socket, time, select

def GetWeatherDataFromGroundStation():
	#Get weather data from ESP8266 on the ground station
	Server_UDP_IP = "192.168.1.108"
	Server_UDP_PORT_ForESP8266 = 7777
	Receive_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Receive_Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	Receive_Sock.bind((Server_UDP_IP, Server_UDP_PORT_ForESP8266))
	data, addr = Receive_Sock.recvfrom(100) # buffer size is 100 bytes
	if(Receive_Sock.recvfrom(100)):
		print("received message: ")
		print(data)
	Receive_Sock.close()
	return data.decode("utf-8")

def GetCommandFromMainServer():
	#Get command from main server(Website)
	Server_UDP_IP = "192.168.1.108"
	Server_UDP_PORT_ForMainServer = 6666
	Receive_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Receive_Sock.bind((Server_UDP_IP, Server_UDP_PORT_ForMainServer))
	command, addr = Receive_Sock.recvfrom(100) # buffer size is 1024 bytes
	if(Receive_Sock.recvfrom(100)):
		print("received message: ")
		print(command)
		SendingMessageToFloatChamber(command)

	Receive_Sock.close()
	return data.decode("utf-8")

def SendingMessageToFloatChamber(command):
	#Raspberry Pi send message to ESP8266 on the Float chamber
	Client_TCP_IP = "192.168.1.29"
	Client_TCP_PORT = 5555
	#MESSAGE = "Hello this is raspberry pi!"
	#Create TCP socket
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet, # TCP
	Send_Sock.settimeout(20)
	Send_Sock.connect((Client_TCP_IP,Client_TCP_PORT))
	#Check the command
	if command=='ShowVoltage':
		Send_Sock.send('1'.encode('utf-8'))
	elif command=='PowerUp':
		Send_Sock.send('2'.encode('utf-8'))
	elif command=='ShutDown':
		Send_Sock.send('3'.encode('utf-8'))
	else :
		return "DoNothing"
	print(Send_Sock.recv(200))
	return Send_Sock.recv(200)
	#close the socket
	Send_Sock.close()
	
if __name__ == '__main__':
	i=1
	while(1):
		GetWeatherDataFromGroundStation()	
		'''
		if i%3==0:
			command = 'ShutDown'
			print(command)
		elif i%2==0:
			command = 'PowerUp'
			print(command)
		elif i%1==0:
			command = 'ShowVoltage'
			print(command)
		elif i==20:
			i=1
		else :
			command = "ShowVoltage"
			print(command)
		SendingMessageToFloatChamber(command)
		i=i+1
		'''
		time.sleep(1)
	
	
