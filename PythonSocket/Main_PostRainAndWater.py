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
#import daemon # keep listening in daemon mode

#IP and port of main server
HOST = '140.116.202.132'
PORT = 3038	

#IP and port of Raspberry pi
LAB5910_IP = '192.168.1.108'
ListeningPort = 5910
global FlagOfListening
global StartTime
#delay time in second
SampleInterval = 5
MinTransmitTimeInterval = 1
WaitingLimit = 5
DelayTime = 0.3

def CheckIfInternetIsConnected():
	while(1):
		try:
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=2)
			return True
		except urllib.error.URLError as err:
			pass	

def PostWaterData(MainSocket):
	WaterWaitingCount=0
	while(1):
		CurrentWaterData = GetWaterData()
		WaterWaitingCount = WaterWaitingCount + 1
		if CurrentWaterData is not None:
			break
		elif WaterWaitingCount == WaitingLimit:
			CurrentWaterData = [0, 0, 0, 0, 0, 0, 0]
			break
	#encoding the receive data and sending to the server by UDP.
	MainSocket.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	
def PostWeatherData(MainSocket):
	RainSerialCount = 0
	while(1):
		CurrentRainData = GetRainData(WaitingLimit)
		# WaitingLimit*0.2 second for per waiting time.
		RainSerialCount = RainSerialCount + 1
		if CurrentRainData is not None:
			break
		#less half of update time.
		elif RainSerialCount > WaitingLimit:
			CurrentRainData = ", 0, 0, 0, 0, 0]"
			print("Rain receive waiting limit!")
			break
	while(1):
		CurrentWeatherData = GetWeatherDataFromGroundStation()
		if CurrentWeatherData is not None:
			break
	#Create a socket, DGRAM means UDP protocal
	MeldedWeatherData = CurrentWeatherData + CurrentRainData
	print(MeldedWeatherData)
	#encoding the receive data and sending to the server by UDP.
	MainSocket.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
        
	#sleep 1 seconds
	#time.sleep(1)

def DataSampling(MainSocket):
	print('DataSampling')
	#WaterThread = threading.Thread(target = PostWaterData(MainSocket))
	WeatherThread = threading.Thread(target = PostWeatherData(MainSocket))
	#Engage thread objects
	#WaterThread.start()
	WeatherThread.start()
	#WaterThread.join()
	WeatherThread.join()
		
def ListeningToMainServer(MainSocket):
	global FlagOfListening
	while(True):
		print('ListeningToMainServer')
		command, addr = MainSocket.recvfrom(20)
		command = command.decode()
		print(command)
		if(command == '200'):
			pass
			#FlagOfListening = True
			return False
		elif(command== '404'):
			pass
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		print("StatusOfWaterChamber")
		print(StatusOfWaterChamber)
		MainSocket.sendto(StatusOfWaterChamber.encode(), addr)
		#FlagOfListening = True
		return True

if __name__ == '__main__':
	#UDP socket to the "Main Server", DGRAM means UDP protocal.
	MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	MainSocket.settimeout(20)
	global FlagOfListening
	global StartTime
	FlagOfSample = False
	FlagOfListening = False
	FlagOfListeningInitialization = False
	StartTime = time.time()
	#ListeningThreading = threading.Thread(target = ListeningToMainServer(MainSocket))
	#ListeningThreading.setDaemon(True)
	#ListeningThreading.start()
	print('Start')
	while(True):
		CurrentTime = time.time()
		#Check the time interval
		if(CurrentTime - StartTime > SampleInterval):
			CheckIfInternetIsConnected()
			FlagOfListening = False
			DataSamplingThread = threading.Thread(target = DataSampling(MainSocket))
			ListeningThreading = threading.Thread(target = ListeningToMainServer(MainSocket))
			DataSamplingThread.start()
			ListeningThreading.start()
			print("Sampling is Done")
			StartTime = time.time()
			FlagOfSample = True
		elif(CurrentTime - StartTime > MinTransmitTimeInterval):
			CheckIfInternetIsConnected()
			MainSocket.sendto("HeartBeat Message".encode('utf-8'), (HOST, PORT))
			FlagOfListening = False
			ListeningThreading = threading.Thread(target = ListeningToMainServer(MainSocket))
			ListeningThreading.start()
		else:
			print("------------Pass------------")
		print("FlagOfSample")
		print(FlagOfSample)
		#print("FlagOfListening")
		#print(FlagOfListening)
		time.sleep(DelayTime)
	MainSocket.close()
