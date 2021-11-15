#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr

int main(int argc , char *argv[]){
	int socket_desc;
	struct sockaddr_in server;
	char *message , server_reply[2000];
	while(1)
	{
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1) printf("Could not create socket");
		
	server.sin_addr.s_addr = inet_addr("192.168.0.200");
	server.sin_family = AF_INET;
	server.sin_port = htons( 6969 );

	//Connect to remote server
	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0){
		puts("connect error");
		return 1;
	}
	
	puts("Connected\n");
	
	//Send some data
	message = "0x01 0x03 0x00 0x30 0x00 0x01 0x84 0x05";
	if( send(socket_desc , message , strlen(message) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 2000 , 0) < 0){
		puts("recv failed");
	}
	printf("after receiving\n");
	puts("Reply received\n");
	puts(server_reply);
	puts(read(socket_desc, server_reply , 2000));
	close(socket_desc);
	}
	return 0;
}
