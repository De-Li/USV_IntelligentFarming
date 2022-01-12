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
LAB5910_IP = '192.168.1.108'
ListeningPort = 5910

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

def PostWaterData(MainSocket):
	WaterWaitingCount=0
	while(1):
		CurrentWaterData = GetWaterData()
		WaterWaitingCount = WaterWaitingCount + 1
		if CurrentWaterData is not None:
			break
		elif WaterWaitingCount == 20:
			CurrentWaterData = [0, 0, 0, 0, 0, 0, 0]
			break
	#encoding the receive data and sending to the server by UDP.
	MainSocket.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	
def PostWeatherData(MainSocket):
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
	while(True):
		print('ListeningToMainServer')
		command, addr = MainSocket.recvfrom(20)
		print(command)
		if(command.decode() == '200'):
			continue
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		print("StatusOfWaterChamber")
		print(StatusOfWaterChamber)
		MainSocket.sendto(StatusOfWaterChamber.encode(), addr)
		FlagOfListening = True
		return True

if __name__ == '__main__':
	print('Main')
	#UDP socket to the "Main Server", DGRAM means UDP protocal.
	MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	FlagOfSample = False
	global FlagOfListening
	FlagOfListening = False
	FlagOfListeningInitialization = False
	StartTime = time.time()
	while(1):
		print('Start')
		CurrentTime = time.time()
		#Check if the sampling is successful
		if(FlagOfSample == True):
			#Declare threading objects
			DataSamplingThread = threading.Thread(target = DataSampling(MainSocket))
			FlagOfSample = False
			if(FlagOfListening == False and FlagOfListeningInitialization == False):
				ListeningThreading = threading.Thread(target = ListeningToMainServer(MainSocket))
				ListeningThreading.setDaemon(True) #Set listening in Daemon mode.
				ListeningThreading.start()
				FlagOfListeningInitialization = True
		#Check if Listening is successful
		if(FlagOfListening == True):
			ListeningThreading = threading.Thread(target = ListeningToMainServer(MainSocket))
			ListeningThreading.setDaemon(True)
			ListeningThread.start()
			FlagOfListening = False
		#Check the time interval
		if(CurrentTime - StartTime > SampleInterval or FlagOfListeningInitialization == False):
			CheckIfInternetIsConnected()
			DataSamplingThread = threading.Thread(target = DataSampling(MainSocket))
			DataSamplingThread.start()
			print("Sampling is Done")
			StartTime = time.time()
			FlagOfSample = True
		print("FlagOfSample")
		print(FlagOfSample)
		print("FlagOfListening")
		print(FlagOfListening)
		time.sleep(DelayTime)
	MainSocket.close()
