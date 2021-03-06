import serial, time, re
#from datetime import datetime, timezone, timedelta
def SerialSetting(ser):
	ser.port = "/dev/ttyUSB0"

	#9600,N,8,1
	ser.baudrate = 9600
	ser.bytesize = serial.EIGHTBITS #number of bits per bytes
	ser.parity = serial.PARITY_NONE #set parity check
	ser.stopbits = serial.STOPBITS_ONE #number of stop bits
 
	ser.timeout = 0.5          #non-block read 0.5s
	ser.writeTimeout = 0.5     #timeout for write 0.5s
	ser.xonxoff = False    #disable software flow control
	ser.rtscts = False     #disable hardware (RTS/CTS) flow control
	ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
	try: 
		ser.open()        
	except Exception as ex:
		print ("open serial port error " + str(ex))
		exit() 
	return ser

def DecipherRainData(response):
	#extract the float data from response
	FloatData = re.findall("\d+\.\d+", response)
	try:
		if(FloatData[3] is not None):		
			#arrange rain data into CSV format.
			ArrangedResponse = ', ' +' , '.join(str(e) for e in FloatData)+', 0]'
			return ArrangedResponse
	except:
		return "Rain data is not complete!"
def GetRainData(TryLimit):
	'''
	#  +8 timezone
  tz = timezone(timedelta(hours=+8))

  # getting current time and specifying time zone and change into iso format.
  	datetime.now(tz).isoformat()
	'''
	ser = serial.Serial()
	ser.port = "/dev/ttyUSB0"
	
	#9600,N,8,1
	ser.baudrate = 9600
	ser.bytesize = serial.EIGHTBITS #number of bits per bytes
	ser.parity = serial.PARITY_NONE #set parity check
	ser.stopbits = serial.STOPBITS_ONE #number of stop bits
 
	ser.timeout = 0.5          #non-block read 0.5s
	ser.writeTimeout = 0.5     #timeout for write 0.5s
	ser.xonxoff = False    #disable software flow control
	ser.rtscts = False     #disable hardware (RTS/CTS) flow control
	ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
	#print("entering serial")
	i=0
	while(1):
		i = i + 1
		try: 
			if ser.isOpen():
				pass
			else:
				ser.open()        
		except Exception as ex:
			print ("open serial port error " + str(ex))
			exit() 		
		if ser.isOpen():	
			try:
				ser.flushInput() #flush input buffer
				ser.flushOutput() #flush output buffer
				#listen data per 0.1s
				response = ser.readline()
				if(response):	
					print(str(response))
					ser.close()
					#The sequence of response is Acc(Accumulation), EventAcc, TotalAcc, RInt.
					response = response.decode('UTF-8')
					ArrangedResponse = DecipherRainData(response)
					print(ArrangedResponse)
					return ArrangedResponse
				time.sleep(0.1)
				if(i==TryLimit/2):
					ser.close()
				elif(i==TryLimit):
					print("Rain receive waiting limit!")
					return None
			except Exception as e1:
				print ("communicating error " + str(e1))
				return "Communication Error"
		else:
			print ("open serial port error")
			return "Communication Error"

if __name__ == '__main__':
	#ser = serial.Serial()
	#ser = SerialSetting(ser)
	while(1):
		RainData = GetRainData(20)
		if RainData!=None:
			time.sleep(2)
			
