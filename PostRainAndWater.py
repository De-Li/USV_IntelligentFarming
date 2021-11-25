from ReadRainSensor import GetRainData
import socket

if __name__ == '__main__':
    CurrentRainData = GetRainData()
    Host = '127.0.0.1'
    PORT = 30000
    ClientMessage = 'Hello!'
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    client.sendall(clientMessage.encode())
    
    serverMessage = str(client.recv(1024), encoding = 'utf-8')
    print('Server:', serverMessage)
    
    client.close()
    
