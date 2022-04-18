"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:PostRainData.py
related file: Main_RainWater, PostWaterData.py, PostRainData.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
Git branch command: git clone --branch SYSArgument https://github.com/De-Li/USV_UnderWaterSensors_Socket.git
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
"""

#from ReadRainSensor import GetRainData
from ReadUnderWaterSensors import GetWaterData
from RaspberryPi_IntermediateServer import GetWeatherDataFromGroundStation, SendingMessageToFloatChamber
from ReadRainSensor import GetRainData
import socket, time, threading, time, logging, sys, schedule
import urllib.request #URL related liberary
from gpiozero import CPUTemperature
import RPi.GPIO as GPIO
from datetime import datetime, timezone, timedelta

#IP and port of main server
HOST = '140.116.202.132'
#PORT = 3038 #台南魚塭
#PORT = 3031 #高雄魚塭
PinWaterMotorControl = 21 #Control the AC relay by Raspberry pi pin 21.

global DataList #WaterData, WeatherData, RainData
global RainData
global FlagOfException
global StatusOfWaterChamber
global StatusParameterList
global BatteryStatusList #1.BatterySwitch, 2.BatteryStatus, 3.CurrentBatteryVoltage, 4.StatusOfWaterChamber.
global StatusParameterOfSystem
global ExecutiveSchedule
global PORT
global VoltageLevelOfBattery
global WaterMotorExecutiveTime

#-----Parameter-----
#Time(second)
WaterWaitingTime = 10
SocketTimeOut = 1
WaitingLimit = 10
DelayTime = 2

#UDP socket to the "Main Server", DGRAM means UDP protocal.
MainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MainSocket.settimeout(SocketTimeOut)

#Declare the logging level.
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a', format=FORMAT) 
#filemode=a means append new logging info behind old, filemode = w means erase old message and write new one.
	
def GetArgument():
	global ExecutiveSchedule
	global WaterMotorExecutiveTime
	
	ExecutiveSchedule = input("Please enter the schedule for esp32, default setting type 'd'!")
	if(ExecutiveSchedule is 'd'):
		ExecutiveSchedule = None
	
	WaterMotorExecutiveTime = input("Enter the Executive time for motor, default setting type 'd'(60sec)!")
	if(WaterMotorExecutiveTime is 'd'):
		WaterMotorExecutiveTime = 60
	else:
		WaterMotorExecutiveTime = int(WaterMotorExecutiveTime)
	location = input("Please enter the location, 't' or 'k'!")
	if(location is 't'):
		location = "Tainan Farm"
	elif(location is 'k'):
		location ="Kaohsiung Farm"
	else:
		print("wrong location format!")
	return location

def GPIOEngage():
	global WaterMotorExecutiveTime
	if(WaterMotorExecutiveTime is None):
		WaterMotorExecutiveTime = 20
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PinWaterMotorControl, GPIO.OUT)
	GPIO.output(PinWaterMotorControl, 1)# set port/pin value to 1/GPIO.HIGH/True
	time.sleep(WaterMotorExecutiveTime)	
	GPIO.cleanup()
def SetScheduler():
	global ExecutiveSchedule
	schedule.every(3).minutes.do(CommunicationToMainServer)
	schedule.every(0.7).minutes.do(PostWeatherData, FlagOfSampling = 'Rain')
	schedule.every(1).minutes.do(PostWeatherData, FlagOfSampling = 'All')
	schedule.every(0.5).minutes.do(PostWaterData)
	schedule.every(2).minutes.do(GPIOEngage)
	#schedule.every().hour.at("00:05").do(GPIOEngage)
	#schedule.every().hour.at("30:05").do(GPIOEngage)
	schedule.every().hour.at("04:00").do(PostWaterData)
	schedule.every().hour.at("04:30").do(PostWaterData)
	schedule.every().hour.at("34:00").do(PostWaterData)
	schedule.every().hour.at("34:30").do(PostWaterData)
	
	#Chech status of system
	schedule.every(0.5).minutes.do(CommandESP8266Inchamber, command= 'ShowStatus')
	schedule.every().hour.at("34:15").do(CommandESP8266Inchamber, command= 'ShowStatus')
	schedule.every(0.1).minutes.do(CommandESP8266Inchamber, command= ExecutiveSchedule)
	schedule.every().hour.at("31:00").do(CommandESP8266Inchamber, command= ExecutiveSchedule)
	'''
	schedule.every().hour.at("04:15").do(CommandESP8266Inchamber, command= 'ShowStatus')
	schedule.every().hour.at("34:15").do(CommandESP8266Inchamber, command= 'ShowStatus')
	schedule.every().hour.at("01:00").do(CommandESP8266Inchamber, command= ExecutiveSchedule)
	schedule.every().hour.at("31:00").do(CommandESP8266Inchamber, command= ExecutiveSchedule)
	schedule.every(5).minutes.do(CheckCPUTemperature)
	schedule.every(10).minutes.do(ShowPoccessingStatus)
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
	print(DataList[0])
	
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
			if(CurrentRainData == None or CurrentRainData == "Rain data is not complete!"):
				CurrentRainData = DataList[2]
				logging.debug("Raindata is not complete", exc_info = True)
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
			DataList[1] = CurrentWeatherData + DataList[2]
		print(DataList[1])
def ShowPoccessingStatus():
	global FlagOfException
	Cpu = CPUTemperature()
	print("CPU Temperature: ")
	print(Cpu)
	print("FlagOfException: ")
	print(FlagOfException)

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

def CommunicationToMainServer():
	global PORT
	global DataList
	#global StatusOfWaterChamber
	#global FlagOfException
	#global StatusParameterOfSystem
	CheckIfInternetIsConnected()
	print("send data to")
	print(HOST, PORT)
	MainSocket.sendto(DataList[0].encode('utf-8'), (HOST, PORT))
	time.sleep(0.1)
	MainSocket.sendto(DataList[1].encode('utf-8'), (HOST, PORT))
	print("The data is uploaded")

def CommandESP8266Inchamber(command):
	global StatusOfWaterChamber
	global StatusParameterList
	global FlagOfException
	global StatusParameterOfSystem
	global ExecutiveSchedule
	global VoltageLevelOfBattery
	if(command == 'ShowStatus'):
		print("Show the status of ESP32!")	
		pass
	else:
		if(ExecutiveSchedule is not None):
			temp = ExecutiveSchedule.split(',')
			if(len(temp) is not 5):
				print("ExecutiveSchedule format is invalid")
				return False
		else:
			return schedule.CancelJob
	try:
		while(command is not 'ShowStatus'):
			print("Send the Schedule to ESP32!")
			StatusOfWaterChamber = SendingMessageToFloatChamber(command)
			print(StatusOfWaterChamber)
			StatusOfWaterChamber = StatusOfWaterChamber.split(',')
			VoltageLevelOfBattery = StatusOfWaterChamber[0]
			print("Change schedule successfully!")
			return schedule.CancelJob
		StatusOfWaterChamber = SendingMessageToFloatChamber(command)
		print(StatusOfWaterChamber)
		VoltageLevelOfBattery = StatusOfWaterChamber[0]
	except:
		print("Fail to connect ESP8266 in the chamber!")

if __name__ == '__main__':
	global DataList
	global FlagOfException
	global StatusParameterList
	global StatusOfWaterChamber
	global BatteryStatusList
	global ExecutiveSchedule
	global PORT
	ExecutiveSchedule = None
	BatteryParameterList = [False, True, "[1.1, 1"]
	BatteryStatusList = [False,0,"[1.1, 1", "0", "0"]
	DataList = ["[1, 1, 0, 0, 0, 0, 0]", "[1, 1, 0, 0, 0, 0, 0, 1]", ", 2, 2, 2, 2, 2]"]
	FlagOfException = 0b0000000
	location = GetArgument()
	if(location == "Kaohsiung Farm"):
		PORT = 3031 #高雄魚塭
	elif(location=="Tainan Farm"):
		PORT = 3038 #台南魚塭
	SetScheduler()
	print('Start')
	while(True):
		schedule.run_pending()
		time.sleep(DelayTime)
	MainSocket.close()
