#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>

unsigned char* 2DArray[8];
unsigned char* 1DArray;

int main(int argc , char *argv[]){
	//0x01 0x03 0x00 0x30 0x00 0x01 0x84 0x05
	/*2DArray[0] = "0x01";
	2DArray[1] = "0x03";
	2DArray[2] = "0x00";
	2DArray[3] = "0x30";
	2DArray[4] = "0x00";
	2DArray[5] = "0x01";
	2DArray[6] = "0x84";
	2DArray[7] = "0x05";*/
		
	int socket_desc;
	struct sockaddr_in server;
	char *Message , server_reply[2000];
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
	//byte MessageByte[] = {0x01, 0x03, 0x00, 0x30, 0x00, 0x01, 0x84, 0x05};
	Message = "0x01 0x03 0x00 0x30 0x00 0x01 0x84 0x05";
	if( send(socket_desc , Message , sizeof(Message) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	printf("before receiving\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 2000 , 0) < 0){
		puts("recv failed");
	}
	printf("after receiving\n");
	puts("Reply received\n");
	puts(server_reply);
	//puts(read(socket_desc, server_reply , 2000));
	close(socket_desc);
	}
	return 0;
}
