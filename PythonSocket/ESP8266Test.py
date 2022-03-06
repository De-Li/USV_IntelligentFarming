import socket, time, select, re

def SendingMessageToFloatChamber(command):
	#Raspberry Pi send message to ESP8266 on the Float chamber
	#Client_TCP_IP = "192.168.1.104"
	Client_TCP_IP = "192.168.1.37"
	Client_TCP_PORT = 5555
	ReturnList = []
	#MESSAGE = "Hello this is raspberry pi!"
	#Create TCP socket
	Send_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet, # TCP
	Send_Sock.settimeout(5)
	Send_Sock.connect((Client_TCP_IP, Client_TCP_PORT))
	
	#command = "11.7,13.7,180,180,120,300,20,600"
	Send_Sock.send(command.encode('utf-8'))
	Reply = Send_Sock.recv(30)
	'''
	#print(Reply)
	Reply = Reply.decode('utf-8')
	#Check if the voltage is below the limit, if the voltage is below the limit then shut the float chamber down.
	VoltageValue = re.findall("\d+\.\d+", Reply)
	VoltageValue = float(VoltageValue[0])
	status = re.findall("\d+", Reply)
	status = int(status[2])
	if(VoltageValue >= 11.70):
		ReturnList.append("[" + str(VoltageValue) + ', ' + str(status))
		ReturnList.append("Normal")
		if(status == 1):
			ReturnList.append(True)
		elif(status == 0):
			ReturnList.append(False)
	elif(VoltageValue < 11.7):
			try:
				Send_Sock.connect((Client_TCP_IP,Client_TCP_PORT))
			except:
				ReturnList.append("[" + str(VoltageValue) + ', ' + str(status))
				ReturnList.append("Lose connection to the ESP8266 on the Float chamber, fail to shut down.(the battery is too low)")
				Send_Sock.close()
				return ReturnList
			#Send_Sock.send('3'.encode('utf-8'))
			#Reply = Send_Sock.recv(30)
			#status = re.findall("\d+", Reply.decode('utf-8'))
			#status = int(status[2])
		ReturnList.append("[" + str(VoltageValue) + ', ' + str(status))
		ReturnList.append("The voltage of battery is too low, SHUTDOWN!")
		#print("The voltage of battery is too low, SHUTDOWN!")
		if(status == 1):
			ReturnList.append(True)
		elif(status == 0):
			ReturnList.append(False)
	#print(ReturnList)
	#close the socket
	Send_Sock.close()
	return ReturnList
	'''
if __name__ == '__main__':
	i=0
	while(1):
		if(i%2==0):
			command = "11.7,13.7,180,180,120,300,20,600"
		else:
			command = "1,1,1,1,1,1,1,1"
		try:
			SendingMessageToFloatChamber(command)
		except:
			print("waiting")
		time.sleep(1)
