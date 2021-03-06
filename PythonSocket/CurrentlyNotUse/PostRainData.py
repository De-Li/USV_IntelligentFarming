"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:PostRainData.py
related file: Main_RainWater, ReadRainSensor.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/12/07
The Ip and port of Server
	HOST = '140.116.202.132'
    PORT = 3038
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
from ReadRainSensor import GetRainData
from ReadUnderWaterSensors import GetWaterData
import socket
import serial, time
def PostRainData():
	while(1):
		CurrentRainData = GetRainData()
		if CurrentRainData is not None:
			break			
	HOST = '192.168.1.228'
	PORT = 30000
	#print(CurrentRainData)
	#Create a socket
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             
        
	#encoding the receive data and sending to the server by UDP.
	client.sendto(CurrentRainData.encode('utf-8'), (HOST, PORT)) 
        
	#Waiting for the echo message from the server.
	serverMessage = str(client.recv(1024), encoding = 'utf-8')
	print('Server:', serverMessage)
        
	#sleep 1 second
	time.sleep(1)
	#client.close()
	
    #Visual studio git test
	#Visual Studio test from github
if __name__ == '__main__':
	PostRainData()
