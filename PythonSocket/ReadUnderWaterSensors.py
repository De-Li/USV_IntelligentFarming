"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:ReadUnderWaterSensors.py
related file:PostRainAndWater.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/11/30
The Ip and port of the wifi adapter in 5936 router field.
  HOST = '192.168.0.200'
  PORT = 6969
2021/11/30
The "inquiry" code for Under water sensors. 水質感測設備"詢問"碼
	溶氧值:0x01, 0x03, 0x00, 0x30, 0x00, 0x01, 0x84, 0x05
	水溫:0x01, 0x03, 0x00, 0x2b, 0x00, 0x01, 0xf4, 0x02
	水質ORP:0x01, 0x03, 0x00, 0x31, 0x00, 0x01, 0xd5, 0xc5
	濁度:0x01, 0x03, 0x00, 0x4c, 0x00, 0x01, 0x45, 0xdd
	氨氮值:0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xcb
	電導率:0x01, 0x03, 0x00, 0x2e, 0x00, 0x01, 0xe4, 0x03
	PH值:0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x54, 0x08
	------------------------------------------------------------------
	The "feedback" code for Under water sensors.水質感測設備"應答"碼
	溶氧值:0x01, 0x03, 0x02, 0x02, 0x01, 0xf8, 0x58
	水溫:0x01, 0x03, 0x02, 0x00, 0xc1, 0x79, 0xd4
	水質ORP:0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	濁度:0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	氨氮值:0x01, 0x03, 0x04, 0x2c, 0x81, 0x40, 0x91, 0x52, 0xe7
	電導率:0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	PH值:0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	
---------------------------------------------------------------
Log:
2021/11/30
Create script for read under water sensors.
---------------------------------------------------------------
"""
import socket
import time
def GetWaterData():

  	HOST = '192.168.0.200'
  	PORT = 6969
  	#InquiryArray = bytearray()
  	#InquiryArray.append(0x01)
  	InquiryArray = bytes([0x01, 0x03, 0x00, 0x2b, 0x00, 0x01, 0xf4, 0x02])
	print("Inquiry code :")
	print(InquiryArray)
  	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  	client.connect((HOST, PORT))
  	client.sendall(InquiryArray)

  	serverMessage = client.recv(1024)
  	print('Server:', serverMessage)

  	client.close()
if __name__ == '__main__':
	while(1):  
		#get water information
		WaterQualityData = GetWaterData()
		#Sleep 1 second
		time.sleep(2)
		
