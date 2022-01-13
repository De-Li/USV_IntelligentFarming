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
global RainData
WaterData"[1, 1, 0, 0, 0, 0, 0]"
RainData = ", 0, 0, 0, 0, 0]"
global FlagOfSampling
#delay time in second
SampleInterval = 10
SocketTimeOut = 1
MinTransmitTimeInterval = 3
WaitingLimit = 20
DelayTime = 0.3

def CheckIfInternetIsConnected():
	while(1):
		try:
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=2)
			return True
		except urllib.error.URLError as err:
			pass	

def PostWaterData():
	global WaterData
	WaterWaitingCount=0
	CurrentWaterData = GetWaterData()
	if CurrentWaterData is not None:
		WaterData = CurrentWaterData
	elif CurrentWaterData is None:
		pass
	#encoding the receive data and sending to the server by UDP.
	#MainSocket.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	print(WaterData)
def PostWeatherData():
	global WeatherData
	global RainData
	global FlagOfSampling
	#WeatherData = "[0, 0, 0, 0, 0, 0, 0]" 
	CurrentRainData = GetRainData(WaitingLimit)
	if(CurrentRainData == None):
		CurrentRainData = RainData
	else:
		RainData = CurrentRainData
	# WaitingLimit*0.1 second is the time for trying.
	CurrentWeatherData = GetWeatherDataFromGroundStation()
	#Create a socket, DGRAM means UDP protocal
	WeatherData = CurrentWeatherData + CurrentRainData
	print(WeatherData)
	FlagOfSampling = True
	#encoding the receive data and sending to the server by UDP.
	#MainSocket.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
		
def CommunicationToMainServer(content):
	print('ListeningToMainServer')
	#UDP socket to the "Main Server", DGRAM means UDP protocal.
	MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	MainSocket.settimeout(SocketTimeOut)
	MainSocket.sendto(content.encode('utf-8'), (HOST, PORT))
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
		print("Lose connection to Main Server!")
		pass

if __name__ == '__main__':
	global StartTime
	global WaterData
	global WeatherData
	global FlagOfSampling
	FlagOfSampling = False
	StartTime = time.time()
	print('Start')
	count=1
	while(True):
		CurrentTime = time.time()
		#Check the time interval
		if(CurrentTime - StartTime > SampleInterval):
			print("DataSampling")
			CheckIfInternetIsConnected()
			CommunicationThread = threading.Thread(target = CommunicationToMainServer("HeartBeat Message"))
			WaterSamplingThread = threading.Thread(target = PostWaterData())
			WeatherSamplingThread = threading.Thread(target = PostWeatherData())
			CommunicationThread.start()
			WeatherSamplingThread.start()
			WaterSamplingThread.start()
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
			count=1
		elif(CurrentTime - StartTime > MinTransmitTimeInterval*count):
			CheckIfInternetIsConnected()
			CommunicationThread = threading.Thread(target = CommunicationToMainServer("HeartBeat Message"))
			CommunicationThread.start()
			CommunicationThread.join()
			count = count + 1
			if(count%2==0):
				WeatherSamplingThread = threading.Thread(target = PostWeatherData())
				WeatherSamplingThread.start()
		else:
			print("------------Pass------------")
		time.sleep(DelayTime)
	MainSocket.close()
