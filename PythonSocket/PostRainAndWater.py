from ReadRainSensor import GetRainData
import socket
import serial, time

if __name__ == '__main__':
    while(1):
        while(1):
            CurrentRainData = str(GetRainData() or 0)
            if(CurrentRainData != 0):
                break
        HOST = '192.168.1.228'
        PORT = 30000
        #ClientMessage = 'Hello!'
        print(CurrentRainData)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        client.sendto(CurrentRainData.encode('utf-8'), (HOST, PORT))      
        serverMessage = str(client.recv(1024), encoding = 'utf-8')
        print('Server:', serverMessage)
        time.sleep(1)
        client.close()
    
