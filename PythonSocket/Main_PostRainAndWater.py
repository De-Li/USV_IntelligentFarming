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
global StartTime
global WaterData
global WeatherData
#delay time in second
SampleInterval = 10
SocketTimeOut = 1
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
	global WaterData
	WaterData = "[0, 0, 0, 0, 0, 0, 0]"
	'''
	WaterWaitingCount=0
	while(1):
		CurrentWaterData = GetWaterData()
		WaterWaitingCount = WaterWaitingCount + 1
		if CurrentWaterData is not None:
			break
		elif WaterWaitingCount == WaitingLimit:
			CurrentWaterData = "[0, 0, 0, 0, 0, 0, 0]"
			break
	return CurrentWaterData	
	#encoding the receive data and sending to the server by UDP.
	#MainSocket.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	'''
def PostWeatherData():
	global WeatherData
	WeatherData = "[0, 0, 0, 0, 0, 0, 0]"
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
	WeatherData = CurrentWeatherData + CurrentRainData
	print(WeatherData)
	#encoding the receive data and sending to the server by UDP.
	#MainSocket.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
        
def DataSampling():
	print('DataSampling')
	WaterThread = threading.Thread(target = PostWaterData())
	WeatherThread = threading.Thread(target = PostWeatherData())
	#Engage thread objects
	WaterThread.start()
	WeatherThread.start()
	WaterData = WaterThread.join()
	WeatherData = WeatherThread.join()
	return WaterData, WeatherData
		
def CommunicationToMainServer(content):
	#UDP socket to the "Main Server", DGRAM means UDP protocal.
	MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	MainSocket.settimeout(SocketTimeOut)
	MainSocket.sendto(content.encode('utf-8'), (HOST, PORT))
	print('ListeningToMainServer')
	try:
		command, addr = MainSocket.recvfrom(20)
		command = command.decode()
		print("command")
		print(command)
		if(command == '200'):
			return True
		elif(command== '404'):
			return True
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		if(StatusOfWaterChamber == "DoNothing"):
			return True
		print("StatusOfWaterChamber")
		print(StatusOfWaterChamber)
		MainSocket.sendto(StatusOfWaterChamber.encode(), addr)
			return True
	except:
		pass

if __name__ == '__main__':
	global StartTime
	StartTime = time.time()
	print('Start')
	while(True):
		CurrentTime = time.time()
		#Check the time interval
		if(CurrentTime - StartTime > SampleInterval):
			CheckIfInternetIsConnected()
			WaterSamplingThread = threading.Thread(target = PostWaterData())
			WeatherSamplingThread = threading.Thread(target = PostWeatherData())
			WaterSamplingThread.start()
			WeatherSamplingThread.start()
			WaterSamplingThread.join()
			WeatherSamplingThread.join()
			print("Sampling is Done")
			CommunicationThread_Water = threading.Thread(target = CommunicationToMainServer(WaterData))
			CommunicationThread_Water.start()
			time.sleep(0.1)
			CommunicationThread_Weather = threading.Thread(target = CommunicationToMainServer(WeatherData))
			CommunicationThread_Weather.start()
			print("Sending is Done")
			StartTime = time.time()
		elif(CurrentTime - StartTime > MinTransmitTimeInterval):
			CheckIfInternetIsConnected()
			CommunicationThread = threading.Thread(target = CommunicationToMainServer("HeartBeat Message"))
			CommunicationThread.start()
			CommunicationThread.join()
		else:
			print("------------Pass------------")
		time.sleep(DelayTime)
	MainSocket.close()
