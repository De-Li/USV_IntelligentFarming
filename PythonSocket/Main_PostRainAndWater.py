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
2022/1/14
FlagOfException
1.loss of Internet connection or A/P 2^0
2.loss of connection of ESP8266 on the floatchamber 2^1
3.loss of connection of ESP8266 in the shutter box 2^2
4.loss of connection of Underwater sensor system 2^3
5.loss of connection of RainSensor 2^4

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
2022/1/14
1.add automatic return voltage function
2.add Flag of exception
3.
2022/1/13
Split the communication part and data sampling
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
global FlagOfException

#WaterData = "[1, 1, 0, 0, 0, 0, 0]"
RainData = ", 0, 0, 0, 0, 0]"
#-----Parameter-----
VoltageLimit = 10
#Time(second)
UploadInterval =20
SampleInterval = UploadInterval/2
MinTransmitTimeInterval = 3
SocketTimeOut = 1
WaitingLimit = 20
DelayTime = 0.3
'''
def ExceptionHandler(Status, Error):
	global FlagOfException
	if(ErrorMessage == "Internet connection or A/P"):
		if(Status == True):
			FlagOfException = FlagOfException & 0b1111110
		else:
			if(FlagOfException & 0b0000001 == 0b0000001):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000001
	elif():
	elif():
	elif():
	elif():
'''
def CheckIfInternetIsConnected():
	global FlagOfException
	while(1):
		try:
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=2)
			return True
		except urllib.error.URLError as err:
			pass	

def PostWaterData():
	global WaterData
	global FlagOfException
	WaterWaitingCount=0
	CurrentWaterData = GetWaterData()
	if(CurrentWaterData == "Lose connection to <UnderWaterSensor!>"):
		if(FlagOfException & 0b0001000 == 0b0001000):
			pass
		else:
			FlagOfException = FlagOfException | 0b0001000
	else:
		if CurrentWaterData is not None:
			WaterData = CurrentWaterData
		elif CurrentWaterData is None:
			pass
		FlagOfException = FlagOfException & 0b1110111
	#encoding the receive data and sending to the server by UDP.
	#MainSocket.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT))
	print(WaterData)
def PostWeatherData():
	global WeatherData
	global RainData
	global FlagOfException
	CurrentRainData = GetRainData(WaitingLimit)
	if(CurrentRainData == "Communication Error"):
		if(FlagOfException & 0b0010000 == 0b0010000):
			pass
		else:
			FlagOfException = FlagOfException | 0b0010000
		CurrentRainData = ", 1, 1, 1, 1, 1]"
	else:
		if(CurrentRainData == None):
			CurrentRainData = RainData
		else:
			RainData = CurrentRainData
		FlagOfException = FlagOfException & 0b1101111
	# WaitingLimit*0.1 second is the time for trying.
	
	#Get weather data from esp8266 in shutter box
	CurrentWeatherData = GetWeatherDataFromGroundStation()
	if(CurrentWeatherData == "Lose connection to <weather ESP8266!>"):
		if(FlagOfException & 0b0000100 == 0b0000100):
			pass
		else:
			FlagOfException = FlagOfException | 0b0000100
		WeatherData = "[0, 0, 0" + CurrentRainData
	else:
		FlagOfException = FlagOfException & 0b1111011
		#Create a socket, DGRAM means UDP protocal
		WeatherData = CurrentWeatherData + CurrentRainData
		print(WeatherData)
		#encoding the receive data and sending to the server by UDP.
		#MainSocket.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
		
def CommunicationToMainServer(content):
	global FlagOfException
	print('ListeningToMainServer')
	#UDP socket to the "Main Server", DGRAM means UDP protocal.
	MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	MainSocket.settimeout(SocketTimeOut)
	'''
	if(content == "Return Status"):
		command = "ShowVoltage"
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		if(StatusOfWaterChamber == "DoNothing"):
			return True
		if(StatusOfWaterChamber == "Lose connection to the ESP8266 on the Float chamber"):
			if(FlagOfException & 0b0000010 == 0b0000010):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000010
		else:
			FlagOfException = FlagOfException & 0b1111101
		print("StatusOfWaterChamber")
		print(StatusOfWaterChamber)
		MainSocket.sendto(StatusOfWaterChamber.encode(), addr)
		return True
	'''
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
	global WeatherData
	global WaterData
	global FlagOfException
	WaterData = "[1, 1, 0, 0, 0, 0, 0]"
	FlagOfException = 0b0000000
	StartTime = time.time()
	print('Start')
	count=1
	while(True):
		CurrentTime = time.time()
		#Check the time interval
		if(CurrentTime - StartTime > UploadInterval):
			CommunicationThread_Water = threading.Thread(target = CommunicationToMainServer(WaterData))
			CommunicationThread_Water.start()
			time.sleep(0.1)
			CommunicationThread_Weather = threading.Thread(target = CommunicationToMainServer(WeatherData))
			CommunicationThread_Weather.start()
			StartTime = time.time()
			count=1
			print("Uploading is Done")
		elif(CurrentTime - StartTime > SampleInterval):
			print("DataSampling")
			CheckIfInternetIsConnected()
			CommunicationThread = threading.Thread(target = CommunicationToMainServer("Return Status"))
			WaterSamplingThread = threading.Thread(target = PostWaterData())
			WeatherSamplingThread = threading.Thread(target = PostWeatherData())
			CommunicationThread.start()
			WeatherSamplingThread.start()
			WaterSamplingThread.start()
			WaterSamplingThread.join()
			WeatherSamplingThread.join()
			print("Sampling is Done")
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
		'''
		elif(FlagOfException is not 0b0000000):
			CommunicationThread = threading.Thread(target = CommunicationToMainServer("HeartBeat Message"))
		'''	
		time.sleep(DelayTime)
	MainSocket.close()
