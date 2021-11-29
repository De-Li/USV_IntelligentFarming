from ReadRainSensor import GetRainData
import socket

if __name__ == '__main__':
    CurrentRainData = GetRainData()
    HOST = '192.168.1.228'
    PORT = 30000
    #ClientMessage = 'Hello!'
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.sendto(CurrentRainData.encode('utf-8'), (HOST, PORT))
    
    serverMessage = str(client.recv(1024), encoding = 'utf-8')
    print('Server:', serverMessage)
    
    client.close()
    
