import socket

HOST = '192.168.1.228'
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print('create socket')
s.bind((HOST, PORT))
print('Listening for broadcast at ', s.getsockname())

while True:
    data, address = s.recvfrom(65535)
    print('Server received from {}:{}'.format(address, data.decode('utf-8')))
    s.sendto("Hello it is server".encode('utf-8'),address)
