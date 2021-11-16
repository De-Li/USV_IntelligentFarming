#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr

unsigned char* array[8];

int main(int argc , char *argv[]){
	//0x01 0x03 0x00 0x30 0x00 0x01 0x84 0x05
	arry[0] = "0x01";
	arry[1] = "0x03";
	arry[2] = "0x00";
	arry[3] = "0x30";
	arry[4] = "0x00";
	arry[5] = "0x01";
	arry[6] = "0x84";
	arry[7] = "0x05";
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
	//Message = "0x01 0x03 0x00 0x30 0x00 0x01 0x84 0x05";
	if( send(socket_desc , array , sizeof(array) , 0) < 0){
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
	//puts(read(socket_desc, server_reply , 2000));
	close(socket_desc);
	}
	return 0;
}
