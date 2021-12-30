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
import urllib.request

HOST = '140.116.202.132'
PORT = 3038	

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
	while(1):
		CurrentWaterData = GetWaterData()
		if CurrentWaterData is not None:
			break
		
	#Create a socket, DGRAM means UDP protocal
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             
        	
	#encoding the receive data and sending to the server by UDP.
	client.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT)) 
		
	#Waiting for the command from the server.
	ServerMessage = str(client.recv(15), encoding = 'utf-8')
	Output = SendingMessageToFloatChamber(ServerMessage)
	if Output != "DoNothing":
		client.sendto(Output.encode('utf-8'), (HOST, PORT))
	#sleep 1 seconds
	#time.sleep(1)
	client.close()
	
def PostWeatherData():
	print("Entering PostWeatherData")
	
	while(1):
		CurrentRainData = GetRainData()
		if CurrentRainData is not None:
			print("CurrentRainData")
			print(CurrentRainData)
			break
	
	while(1):
		CurrentWeatherData = GetWeatherDataFromGroundStation()
		if CurrentWeatherData is not None:
			print("CurrentWeatherData")
			print(CurrentWeatherData)
			break
	'''
	CurrentWeatherData = GetWeatherDataFromGroundStation()	
	print("CurrentWeatherData")
	print(CurrentWeatherData)
	'''
	#Create a socket, DGRAM means UDP protocal
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#MeldedWeatherData = CurrentWeatherData + CurrentRainData
	#print(MeldedWeatherData)
	#encoding the receive data and sending to the server by UDP.
	#client.sendto(MeldedWeatherData.encode('utf-8'), (HOST, PORT)) 
        
	#sleep 1 seconds
	#time.sleep(1)
	client.close()


if __name__ == '__main__':
	#Declare threading objects
	#WaterThreading = threading.Thread(target = PostWaterData)
	#RainThreading = threading.Thread(target = PostRainData)
	#WeatherThreading = threading.Thread(target = PostWeatherData)
	while(1):
		WaterThreading = threading.Thread(target = PostWaterData)
		WeatherThreading = threading.Thread(target = PostWeatherData)
		CheckIfInternetIsConnected()
		#Engage threading objects
		#WaterThreading.start()
		#RainThreading.start()
		WeatherThreading.start()

		#WaterThreading.join()
		#RainThreading.join()
		WeatherThreading.join()

		print("Done")
		time.sleep(30)
