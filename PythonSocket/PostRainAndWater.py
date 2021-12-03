"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:PostRainAndWater.py
related file:ReadUnderWaterSensors.py, ReadRainSensor.py
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
2021/12/02
adding water UDP posting code
2021/11/30
adding some comments.
---------------------------------------------------------------
"""
from ReadRainSensor import GetRainData
from ReadUnderWaterSensors import GetWaterData
import socket, pickle
import serial, time
if __name__ == '__main__':	
	time.sleep(20)
	"""
	while(1):
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
	"""
	
	while(1):
		while(1):
			CurrentWaterData = GetWaterData()
			if CurrentWaterData is not None:
				break
		HOST = '192.168.0.110'
		PORT = 6969
		
		#Create a socket, DGRAM means UDP protocal
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             
        	
		#encoding the receive data and sending to the server by UDP.
		client.sendto(CurrentWaterData.encode('utf-8'), (HOST, PORT)) 
		
		#Waiting for the echo message from the server.
		#serverMessage = str(client.recv(1024), encoding = 'utf-8')
		#print('Server:', serverMessage)
        
		#sleep 30 seconds
		time.sleep(30)
		client.close()
     
    
