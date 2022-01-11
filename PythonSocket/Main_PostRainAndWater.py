"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:PostRainData.py
related file: Main_RainWater, PostWaterData.py, PostRainData.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2022/1/06
The Ip and port of main server.
	HOST = '140.116.202.132'
	PORT = 3038
The external Ip of 5936 敬智's computer.	
	HOST = '140.116.201.71'
2021/12/02
The Ip and port of 5936 敬智's computer.
    HOST = '192.168.0.110'
    PORT = 6969
2021/11/30
The Ip and port of 5910 DeLi's computer.
    HOST = '192.168.0.228'
    PORT = 30000
---------------------------------------------------------------
Log:
---------------------------------------------------------------
"""

#from ReadRainSensor import GetRainData
from ReadUnderWaterSensors import GetWaterData
from RaspberryPi_IntermediateServer import GetWeatherDataFromGroundStation, SendingMessageToFloatChamber
from ReadRainSensor import GetRainData
import socket, time, threading, serial, time
import urllib.request #URL related liberary

#IP and port of main server
HOST = '140.116.202.132'
PORT = 3038	

#IP and port of Raspberry pi
RP_IP = '192.168.1.108'
RP_Port = 5910

#delay time in second
SampleInterval = 5
DelayTime = 0.3

def CheckIfInternetIsConnected():
	while(1):
		try:
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=2)
			return True
		except urllib.error.URLError as err:
			pass	
'''
def PostRainData():
	while(1):
		CurrentRainData = GetRainData()
		if CurrentRainData is not None:
			break			
	#print(CurrentRainData)
	#Create a socket
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             
        
	#encoding the receive data and sending to the server by UDP.
	client.sendto(CurrentRainData.encode('utf-8'), (HOST, PORT)) 
        
	#Waiting for the echo message from the server.
	serverMessage = str(client.recv(1024), encoding = 'utf-8')
	print('Server:', serverMessage)
        
	#sleep 1 second
	#time.sleep(1)
	#client.close()
'''
def PostWaterData():
	WaterWaitingCount=0
	while(1):
		CurrentWaterData = GetWaterData()
		WaterWaitingCount = WaterWaitingCount + 1
		if CurrentWaterData is not None:
			break
		elif WaterWaitingCount == 20:
			CurrentWaterData = [0, 0, 0, 0, 0, 0, 0]
			break
	#Create a socket, DGRAM means UDP protocal
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
	#encoding the receive data and sending to the server by UDP.
	client.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	#Waiting for the command from the server.
	ServerMessage = str(client.recv(15), encoding = 'utf-8')
	print(ServerMessage)
	Output = SendingMessageToFloatChamber(ServerMessage)
	if Output != "DoNothing":
		client.sendto(Output.encode('utf-8'), (HOST, PORT))
	client.close()

def ListeningToMainServer():
	#Create a socket, DGRAM means UDP protocal
	UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPServer.bind((RP_IP, RP_Port))
	command, addr = UDPServer.recvfrom(20)
	StatusOfWaterChamber = SendingMessageToFloatChamber(command)
	UDPServer.sendto(StatusOfWaterChamber.encode(), addr)
	return True
	
def PostWeatherData():
	RainSerialCount = 0
	while(1):
		CurrentRainData = GetRainData()
		# 10 second for per waiting time.
		RainSerialCount = RainSerialCount + 1
		if CurrentRainData is not None:
			break
		#less half of update time.
		elif RainSerialCount > SampleInterval/20:
			CurrentRainData = ", 0, 0, 0, 0, 0]"
			break
	while(1):
		CurrentWeatherData = GetWeatherDataFromGroundStation()
		if CurrentWeatherData is not None:
			break
	#Create a socket, DGRAM means UDP protocal
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	MeldedWeatherData = CurrentWeatherData + CurrentRainData
	print(MeldedWeatherData)
	#encoding the receive data and sending to the server by UDP.
	client.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
        
	#sleep 1 seconds
	#time.sleep(1)
	client.close()

def DataSampling():
	WaterThread = threading.Thread(target = PostWaterData)
	WeatherThread = threading.Thread(target = PostWeatherData)
	#Engage thread objects
	WaterThread.start()
	#WeatherThread.start()
	WaterThread.join()
	#WeatherThread.join()
	
if __name__ == '__main__':
	StartTime = time.time()
	FlagOfSample = False
	FlagOfListening = False
	ListeningThreading = threading.Thread(target = ListeningToMainServer())
	CheckIfInternetIsConnected()
	DataSamplingThread.start()
	DataSamplingThread = threading.Thread(target = DataSampling())
	while(1):
		CurrentTime = time.time()
		ListeningThread.start()
		
		#Check if the sampling is successful
		if(FlagOfSample == True):
			#Declare threading objects
			DataSamplingThread = threading.Thread(target = DataSampling())
			FlagOfSample = False
		#Check if Listening is successful
		if(FlagOfListening == True):
			ListeningThread = threading.Thread(target = ListeningToMainServer())
			FlagOfListening = False
		#Check the time interval
		if(CurrentTime - StartTime > SampleInterval && FlagOfSample == False):
			CheckIfInternetIsConnected()
			DataSamplingThread.start()
			print("Done")
			StartTime = CurrentTime
			FlagOfSample = True
		FlagOfListening = ListeningThreading.join()
		time.sleep(DelayTime)
