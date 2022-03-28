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
import socket, time, threading, time, logging, sys
import urllib.request #URL related liberary
from gpiozero import CPUTemperature

#IP and port of main server
HOST = '140.116.202.132'
PORT = 3038 #台南魚塭
#PORT = 3031 #高雄魚塭

#IP and port of Raspberry pi
#LAB5910_IP = '192.168.1.108'
#ListeningPort = 5910
TPLink_IP = '192.168.1.102'
ListeningPort = 6060
global DataList = ["0","0","0"] #WaterData #WeatherData #RainData
global RainData
global FlagOfException
global StatusOfWaterChamber
global StatusParameterList
global BatteryStatusList = [False,0,"[1.1, 1","0"""] #1.BatterySwitch, 2.BatteryStatus, 3.CurrentBatteryVoltage, 4.StatusOfWaterChamber.
global StatusParameterOfSystem


#WaterData = "[1, 1, 0, 0, 0, 0, 0]"
RainData = ", 0, 0, 0, 0, 0]"
#-----Parameter-----
#VoltageLimit = 10.8
#Time(second)
UploadInterval = 1200
WaterSampleInterval = UploadInterval*0.4
WaterPowercontrolTryingLimit = 1
WaterWaitingTime = 10
RainSampleInterval = UploadInterval/15
MinTCPConnectingTimeInterval = 10
SocketTimeOut = 1
WaitingLimit = 10
DelayTime = 0.5

#UDP socket to the "Main Server", DGRAM means UDP protocal.
MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MainSocket.settimeout(SocketTimeOut)

#Declare the logging level.
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a', format=FORMAT) 
#filemode=a means append new logging info behind old, filemode = w means erase old message and write new one.

#Due to the dirty water, the reading of data is unstable for water quality.
#So the function filters the extreme value of water quality.
#Temperary application,it still need to complete.
'''
def FilterReadingData(Input):
	#transferring the data array into string type in order to send data easily.
	DecipheredData = '['+', '.join(str(e) for e in DecipheredData)+']'
	return DecipheredData
'''
	
def CheckIfInternetIsConnected():
	global FlagOfException
	while(1):
		try:
			urllib.request.urlopen('https://tw.yahoo.com/', timeout=10)
			FlagOfException = FlagOfException & 0b1111110
			return True
		except urllib.error.URLError as err:
			logging.warning("Network unreachable", exc_info = True)
			if(FlagOfException & 0b0000001 == 0b0000001):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000001
			pass
		except socket.timeout as e:
			print('socket timeout')

def PostWaterData():
	global DataList
	global FlagOfException
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
			DataList[0] = CurrentWaterData
		elif CurrentWaterData is None:
			pass
		FlagOfException = FlagOfException & 0b1110111
	#print(DataList[0])
def PostWeatherData(FlagOfSampling):
	global DataList
	global RainData
	global FlagOfException
	CurrentWeatherData = "[0,0,0"
	if(FlagOfSampling == 'Rain' or FlagOfSampling == 'All'):
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
			logging.debug("Raindata is not complete", exc_info = True)
			if(CurrentRainData == None or CurrentRainData == "Rain data is not complete!"):
				CurrentRainData = RainData
			else:
				DataList[2] = CurrentRainData
			FlagOfException = FlagOfException & 0b1101111
	if(FlagOfSampling == 'All'):
		#Get weather data from esp8266 in shutter box
		try:
			CurrentWeatherData = GetWeatherDataFromGroundStation()
		except:
			logging.debug("didn't get weatherdata", exc_info = True)
			CurrentWeatherData = "Lose connection to <weather ESP8266!>"
		if(CurrentWeatherData == "Lose connection to <weather ESP8266!>"):
			if(FlagOfException & 0b0000100 == 0b0000100):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000100
			DataList[1] = "[0, 0, 0" + CurrentRainData
		else:
			FlagOfException = FlagOfException & 0b1111011
			DataList[1] = CurrentWeatherData + RainData
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
	global StatusParameterOfSystem
	MainSocket.sendto(content.encode('utf-8'), (HOST, PORT))
	'''
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
	'''
	try:
		#StatusOfWaterChamber = CommandESP8266Inchamber("ShowVoltage")
		#print("StatusOfWaterChamber")
		#print(StatusOfWaterChamber)
		CPUTemperature = str(CheckCPUTemperature())
		if(StatusOfWaterChamber[1] == "DoNothing"):
			pass
		if(StatusOfWaterChamber[1] == "Lose connection to the ESP8266 on the Float chamber"):
			print("Lose connection to the ESP8266 on the Float chamber")
			#StatusOfWaterChamber[0] = "[1.1, 1"
			if(FlagOfException & 0b0000010 == 0b0000010):
				pass
			else:
				FlagOfException = FlagOfException | 0b0000010
		elif(StatusOfWaterChamber[1] is not "Lose connection to the ESP8266 on the Float chamber"):
			FlagOfException = FlagOfException & 0b1111101
		if(StatusOfWaterChamber[1] == "The voltage of battery is too low, SHUTDOWN!"):
			StatusParameterList[1] = False
			print("The voltage of battery is too low, SHUTDOWN!")
			if(FlagOfException & 0b0100000 == 0b0100000):
				pass
			else:
				FlagOfException = FlagOfException | 0b0100000
		elif(StatusOfWaterChamber[1] is not "The voltage of battery is too low, SHUTDOWN!"):
			FlagOfException = FlagOfException & 0b1011111
		#CPUTemperature = str(CheckCPUTemperature())
		StatusParameterOfSystem = BatteryParameterList[2] + ', ' + CPUTemperature + ', ' + str(FlagOfException) + ']'
		print("StatusParameterOfSystem")
		print(StatusParameterOfSystem)
		MainSocket.sendto(StatusParameterOfSystem.encode(), addr)
		return True
	except:
		print("Data formal problem or Lose connection to ESP8266")
		pass
def CommandESP8266Inchamber(command):
	global StatusOfWaterChamber
	global StatusParameterList
	global FlagOfException
	global StatusParameterOfSystem
	try:
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		#print(StatusOfWaterChamber)
		if(StatusOfWaterChamber[1] == "Normal"):
			BatteryParameterList[2] = StatusOfWaterChamber[0]
			PostWaterData()
		if(StatusOfWaterChamber[1] == "The voltage of battery is too low, SHUTDOWN!"):
			SendingMessageToFloatChamber('ShutDown')
			print("The power is ShutDown! Due to low battery")
			BatteryParameterList[0] = False
			StatusParameterList[1] = False
			return False
		elif(StatusOfWaterChamber[1] == "Lose connection to the ESP8266 on the Float chamber"):
			#print("Fail to connect ESP8266 in the chamber!")
			return False
		elif(StatusOfWaterChamber[1] is not "Lose connection to the ESP8266 on the Float chamber"):
			CPUTemperature = str(CheckCPUTemperature())
			StatusParameterOfSystem = BatteryParameterList[2] + ', ' + CPUTemperature + ', ' + str(FlagOfException) + ']' 
			print(StatusParameterOfSystem)
			CommunicationToMainServer(StatusParameterOfSystem)
			return True
		elif(command == 'PowerUp'):
			print("PowerUp the sensor!")
			BatteryParameterList[0] = True
			return True
		elif(command == 'ShutDown'):
			print("The power is ShutDown!")
			BatteryParameterList[0] = False
			return True
		elif(command == 'ShowVoltage'):
			if(StatusOfWaterChamber[1] == "Normal"):
				StatusParameterList[1] = True
				return "Normal"
			elif(StatusOfWaterChamber[1] == "Donothing"):
				pass
			else:
				StatusParameterList[1] = False
			return False
		'''
			elif(command == 'Sleep'):
				BatteryParameterList[0] = False
				print("The ESP is sleeping now")
				return True
		'''
	except:
		print("Fail to connect ESP8266 in the chamber!")
if __name__ == '__main__':
	global DataList
	global FlagOfException
	global StatusParameterList
	global StatusOfWaterChamber
	BatteryParameterList[2] = "[1.1, 1"
	BatteryParameterList[1] = True
	BatteryParameterList[0] = False
	#DataList[0] = "[1, 1, 0, 0, 0, 0, 0]"
	FlagOfException = 0b0000000
	StartTime = time.time()
	Uploading_LastTime = time.time()
	Sampling_LastTime = time.time()
	Listening_LastTime = time.time()
	#WaterSampling_LastTime = time.time()
	WeatherSampling_LastTime = time.time()
	#CommandESP8266Inchamber('ShowVoltage')
	'''
	if(lat == "22.6163"):
		PORT = 3038 #台南魚塭
		print("In Tainan FishFarm")
	else:
		PORT = 3031 #高雄魚塭
		print("In Kaohsiung FishFarm")
	'''
	PORT = 3038 #台南魚塭
	print("In Tainan FishFarm")
	print('Start')
	while(True):
		CurrentTime = time.time()
		#Uploading data
		if(CurrentTime - Uploading_LastTime > UploadInterval):
			print("Uploading DATA to MainServer")
			CheckIfInternetIsConnected()
			if(StatusParameterList[1] == True):
				CommunicationToMainServer(DataList[0])
			time.sleep(0.1)
			CommunicationToMainServer(DataList[1])
			#Reset the basic time
			Uploading_LastTime = time.time()
			#WaterSampling_LastTime =  time.time()
			Sampling_LastTime = time.time()
			WeatherSampling_LastTime = time.time()
			#Status Check
			#Check the Voltage of float chamber, if voltage is below 10.8, Pi will shutdown the float chamber
			#CommandESP8266Inchamber('ShowVoltage')
			print("Uploading is Done")
		elif(CurrentTime - WeatherSampling_LastTime > UploadInterval/3):
			print("DataSampling")
			#CheckIfInternetIsConnected()
			#Get Weather once before uploading 40 seconds
			PostWeatherData('All')
			#WaterSamplingThread = threading.Thread(target = PostWaterData())
			#WeatherSamplingThread = threading.Thread(target = PostWeatherData())
			#WeatherSamplingThread.start()
			#WaterSamplingThread.start()
			#WaterSamplingThread.join()
			#WeatherSamplingThread.join()
			WeatherSampling_LastTime = time.time()
			print("Sampling is Done")
		elif(CurrentTime - Sampling_LastTime > RainSampleInterval):
			#CheckIfInternetIsConnected()
			PostWeatherData('Rain')
			Sampling_LastTime = time.time()
		elif(CurrentTime - Listening_LastTime > MinTCPConnectingTimeInterval):
			#CheckIfInternetIsConnected()
			PostWaterData()
			#municationToMainServer("HeartBeat Message")
			#If the ESP is on then sampling the waterdata.
			#CommandESP8266Inchamber("ShowVoltage")
			Listening_LastTime = time.time()
			print(bin(FlagOfException))
			print("Upload time in: (Second)")
			print(round(Uploading_LastTime + UploadInterval - CurrentTime, 1))
			'''
			print("---------------------------------------")
			print("StatusParameterList[1]")
			print(StatusParameterList[1])
			print("---------------------------------------")
			print("StatusParameterList[0]")
			print(StatusParameterList[0])
			'''
		else:
			#print("------------Pass------------")
			pass
		time.sleep(DelayTime)
	MainSocket.close()
