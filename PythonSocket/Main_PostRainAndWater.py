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
6.The voltage of battery is too low 2^5
7.CPU's Temperature is too high 2^6

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
from gpiozero import CPUTemperature

#IP and port of main server
HOST = '140.116.202.132'
PORT = 3038

#IP and port of Raspberry pi
#LAB5910_IP = '192.168.1.108'
#ListeningPort = 5910
TPLink_IP = '192.168.1.102'
ListeningPort = 6060
global StartTime
global WaterData
global WeatherData
global RainData
global FlagOfException
global StatusOfWaterChamber

#WaterData = "[1, 1, 0, 0, 0, 0, 0]"
RainData = ", 0, 0, 0, 0, 0]"
#-----Parameter-----
#VoltageLimit = 10.8
#Time(second)
UploadInterval = 100
WaterSampleInterval = UploadInterval*0.7
WaterPowercontrolTryingLimit = 10
SampleInterval = UploadInterval/3
MinTransmitTimeInterval = 5
SocketTimeOut = 1
WaitingLimit = 20
DelayTime = 0.5
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
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=10)
			FlagOfException = FlagOfException & 0b1111110
			return True
		except urllib.error.URLError as err:
			if(FlagOfException & 0b0000001 == 0b0000001):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000001
			pass
		except socket.timeout as e:
			print('socket timeout')

def PostWaterData():
	global WaterData
	global FlagOfException
	WaterWaitingCount=0
	try:
		CurrentWaterData = GetWaterData()
		print("CurrentWaterData: ", CurrentWaterData)
	except:
		CurrentWaterData = "Lose connection to <UnderWaterSensor!>"
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
	try:
		CurrentRainData = GetRainData(WaitingLimit)
	except:
		CurrentRainData = "Communication Error"
		print("RaindataAquicitionError")
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
	
	#Get weather data from esp8266 in shutter box
	try:
		CurrentWeatherData = GetWeatherDataFromGroundStation()
	except:
		CurrentWeatherData = "Lose connection to <weather ESP8266!>"
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
		#encoding the receive data and sending to the server by UDP.
		#MainSocket.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
	print(WeatherData)
def CheckCPUTemperature():
	global FlagOfException
	Cpu = CPUTemperature()
	if(Cpu.temperature < 60):
		if(FlagOfException & 0b1000000 == 0b1000000):
			FlagOfException = FlagOfException & 0b0111111
		pass
	elif(Cpu.temperature > 60 and FlagOfException & 0b1000000 == 0b1000000):
		pass	
	else:	
		FlagOfException = FlagOfException | 0b1000000
	return Cpu.temperature

def CommunicationToMainServer(content):
	global StatusOfWaterChamber
	global FlagOfException
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
	except:
		print("Lose connection to Main Server!")
		pass
	try:
		CommandESP8266Inchamber(command)
		print("StatusOfWaterChamber")
		print(StatusOfWaterChamber)
		CPUTemperature = str(CheckCPUTemperature())
		if(StatusOfWaterChamber[1] == "DoNothing"):
			return True
		if(StatusOfWaterChamber[1] == "Lose connection to the ESP8266 on the Float chamber"):
			print("Lose connection to the ESP8266 on the Float chamber")
			StatusOfWaterChamber[0] = "[1.1, 1"
			if(FlagOfException & 0b0000010 == 0b0000010):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000010
		elif(StatusOfWaterChamber[1] is not "Lose connection to the ESP8266 on the Float chamber"):
			FlagOfException = FlagOfException & 0b1111101
		if(StatusOfWaterChamber[1] == "The voltage of battery is too low, SHUTDOWN!"):
			print("The voltage of battery is too low, SHUTDOWN!")
			if(FlagOfException & 0b0100000 == 0b0100000):
				pass
			else:
				FlagOfException = FlagOfException | 0b0100000
			StatusOfWaterChamber = "[0.0, 0"
		elif(StatusOfWaterChamber[1] is not "The voltage of battery is too low, SHUTDOWN!"):
			FlagOfException = FlagOfException & 0b1011111
		StatusParameter = StatusOfWaterChamber[0] + ', ' + CPUTemperature + ', ' + str(FlagOfException) + ']'
		print("StatusParameter")
		print(StatusParameter)
		MainSocket.sendto(StatusParameter.encode(), addr)
		return True
	except:
		print("Data formal problem or Lose connection to ESP8266")
		pass
def CommandESP8266Inchamber(command):
	global StatusOfWaterChamber
	TryingTime = time.time()
	while(True):
		time.sleep(0.2)
		CurrentTime = time.time()
		if(CurrentTime - TryingTime > WaterPowercontrolTryingLimit):
			return False
		try:
			StatusOfWaterChamber = SendingMessageToFloatChamber(command)
			if(command == 'PowerUp' and StatusOfWaterChamber[2] == True):
				return True
			elif(command == 'ShutDown' and StatusOfWaterChamber[2] == False):
				return True
			elif(command == 'ShowVoltage'):
				return StatusOfWaterChamber[1]
		except:
			print("Fail to connect ESP8266 in the chamber!")
if __name__ == '__main__':
	global StartTime
	global WeatherData
	global WaterData
	global FlagOfException
	BatteryStatus = True
	WaterData = "[1, 1, 0, 0, 0, 0, 0]"
	FlagOfException = 0b0000000
	Uploading_LastTime = time.time()
	Sampling_LastTime = time.time()
	Listening_LastTime = time.time()
	WaterSampling_LastTime = time.time()
	print('Start')
	while(True):
		CurrentTime = time.time()
		#Check the time interval
		if(CurrentTime - Uploading_LastTime > UploadInterval):
			CheckIfInternetIsConnected()
			'''
			CommunicationThread_Water = threading.Thread(target = CommunicationToMainServer(WaterData))
			CommunicationThread_Water.start()
			time.sleep(0.1)
			CommunicationThread_Weather = threading.Thread(target = CommunicationToMainServer(WeatherData))
			CommunicationThread_Weather.start()
			stop_threads = True
			CommunicationThread_Water.join()
			CommunicationThread_Weather.join()
			'''
			CommunicationToMainServer(WaterData)
			time.sleep(0.1)
			CommunicationToMainServer(WeatherData)
			#Status Check
			#Check the Voltage of float chamber, if voltage is below 10.8, Pi will shutdown the float chamber
			if(CommandESP8266Inchamber('ShowVoltage') == "The voltage of battery is too low, SHUTDOWN!"):
				CommandESP8266Inchamber('ShutDown')
				BatteryStatus = False
			elif(CommandESP8266Inchamber('ShowVoltage') == "Normal"):
				BatteryStatus = True
				pass
			print("Uploading is Done")
			Uploading_LastTime = time.time()
		#Read Water data
		elif(CurrentTime - WaterSampling_LastTime > WaterSampleInterval):
			CheckIfInternetIsConnected()
			if(BatteryStatus == True and CommandESP8266Inchamber("PowerUp") == True):
				#time.sleep(10)
				print("Waterdata saampling")
				i=0
				while(i<12):
					time.sleep(5)
					PostWaterData()
					i = i + 1
				i=0
				while(True):
					if(i>20):
						print("Can't shut the power down!!")
						break
					if(CommandESP8266Inchamber("ShutDown") == True):
						break
					else:
						print("Can't shut the power down!!")
					time.sleep(0.1)
					i = i + 1
			else:
				print("Can't connect to ESP8266 in 10 seconds, try next time!!")
			if(BatteryStatus == False):
				print("Battery is too low, wait for charge!")
				pass
			WaterSampling_LastTime =  time.time()
		elif(CurrentTime - Sampling_LastTime > SampleInterval):
			print("DataSampling")
			CheckIfInternetIsConnected()
			PostWeatherData()
			#WaterSamplingThread = threading.Thread(target = PostWaterData())
			WeatherSamplingThread = threading.Thread(target = PostWeatherData())
			WeatherSamplingThread.start()
			#WaterSamplingThread.start()
			#WaterSamplingThread.join()
			WeatherSamplingThread.join()
			Sampling_LastTime = time.time()
			print("Sampling is Done")
		elif(CurrentTime - Listening_LastTime > MinTransmitTimeInterval):
			CheckIfInternetIsConnected()
			CommunicationToMainServer("HeartBeat Message")
			Listening_LastTime = time.time()
			print(bin(FlagOfException))
			print("Upload time in: (Second)")
			print(Uploading_LastTime + UploadInterval - CurrentTime)
		else:
			#print("------------Pass------------")
			pass
		#elif(FlagOfException is not 0b0000000):
			#CommunicationThread = threading.Thread(target = CommunicationToMainServer(FlagOfException))
		time.sleep(DelayTime)
	MainSocket.close()
