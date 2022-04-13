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
	In Tp-link A/P
	ESP8266-float chamber
	IP = "192.168.1.100"
	PORT = "5555"
	ESP8266-Ground Station
	IP = "192.168.1.103"
	--------------------
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
	2022/2/11
	ESP8266,No3
	Client IP = "192.168.1.38"
	Client PORT = 5555
---------------------------------------------------------------
Log:
2021/12/29
add SendingMessageToFloatChamber() function to control the electrical power on the float chamber.
add GetCommandFromMainServer() function to receive the command from the main server.
---------------------------------------------------------------
"""
import socket, time, select, re
global VoltageRecord
BatteryTooLowFlag = False
def GetWeatherDataFromGroundStation():
	#Get weather data from ESP8266 on the ground station
	Server_UDP_IP = "192.168.1.101"
	Server_UDP_PORT_ForESP8266 = 6060
	Receive_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, # UDP
	Receive_Sock.settimeout(10)
	Receive_Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#try:
	Receive_Sock.bind((Server_UDP_IP, Server_UDP_PORT_ForESP8266))
	data, addr = Receive_Sock.recvfrom(40) # buffer size is 40 bytes
	DecodedData = data.decode("utf-8")
	#print(DecodedData)
	DecodedData = DecodedData.split(", ")
	print(DecodedData)
	#print(DecodedData)
	DecodedData[2] = re.sub("[^\d\.]", '',DecodedData[2])
	DecodedData[2] = str(float(DecodedData[2]))
	DecodedData = '['+', '.join(str(e) for e in DecodedData)
	Receive_Sock.close()
	return DecodedData
	'''
	if(DecodedData[2] == '    0.'): #4
		DecodedData[2] = '0'
	elif(DecodedData[2] == '     0.'):#5
		DecodedData[2] = '0'
	elif(DecodedData[2] == '      0.'):#6
		DecodedData[2] = '0'
	elif((float(DecodedData[2])).is_integer()):
		DecodedData[2] = str(float(DecodedData[2]) + 0.1)
		
	except:
		print("Lose connection to <weather ESP8266!>")
		return "Lose connection to <weather ESP8266!>"
		pass
	'''
'''
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
'''
def SendingMessageToFloatChamber(command):
	#Raspberry Pi send message to ESP8266 on the Float chamber
	#Client_TCP_IP = "192.168.1.38"
	Client_TCP_IP = "192.168.1.38"
	Client_TCP_PORT = 100
	ReturnList = []
	#MESSAGE = "Hello this is raspberry pi!"
	#Create TCP socket
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet, # TCP
	#data, addr = Send_Sock.recvfrom(40) # buffer size is 40 bytes
	try:
		Send_Sock.connect((Client_TCP_IP, Client_TCP_PORT))
	except:
		ReturnList.append("Can't connect to ESP32 in the water chamber!")
		return ReturnList
	
	#Check the command
	if command=='ShowStatus':
		Send_Sock.send(command.encode('utf-8'))
		time.sleep(0.5)
		Send_Sock.send(command.encode('utf-8'))
		Reply = Send_Sock.recv(50)
	else :
		Send_Sock.send(command.encode('utf-8'))
		time.sleep(0.5)
		Send_Sock.send(command.encode('utf-8'))
		Reply = Send_Sock.recv(60)
	Reply = Reply.decode('utf-8')
	print(Reply)
	Send_Sock.close()
	return Reply
	
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
	
	
