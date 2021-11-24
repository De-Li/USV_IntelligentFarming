/*
*****************************************************************
Project: Unmmaned surface vehicle
File name:GetDataFromSensors.c
related file:GetDataFromSensors.h, 
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/11/24
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
2021/11/24
Transform this script from main to functin.
---------------------------------------------------------------
******************************************************************
*/
#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>
#include"GetDataFromSensors.h"

//char** GetDataFromSensors(const char* Ip, const int Port){
int main(int argc , char *argv[]){
	char Ip[] = "192.168.0.200";
	int Port = 6969;
	
	//Setting the inquiry codes to each sensor.
	unsigned char InquiryCode[7][8] = {
		{0x01, 0x03, 0x00, 0x30, 0x00, 0x01, 0x84, 0x05},
		{0x01, 0x03, 0x00, 0x2b, 0x00, 0x01, 0xf4, 0x02},
		{0x01, 0x03, 0x00, 0x31, 0x00, 0x01, 0xd5, 0xc5},
		{0x01, 0x03, 0x00, 0x4c, 0x00, 0x01, 0x45, 0xdd},
		{0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xcb},
		{0x01, 0x03, 0x00, 0x2e, 0x00, 0x01, 0xe4, 0x03},
		{0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x54, 0x08}};
	
	char **ReturnValue = (char **)malloc(sizeof(char *)*7);
	for(int i =0;i<7;i++)
	{
		ReturnValue[i] = (char *)malloc(sizeof(char)*4);
	}
	int socket_desc;
	char ReceiveMessage[16] = "Reply received X";
	struct sockaddr_in server;
	//Receive buffer
	unsigned char server_reply[200];
	
	//While loop keep receive data from water sensors. 
	while(1)
	{
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1) printf("Could not create socket");
		
	server.sin_addr.s_addr = inet_addr(Ip);
	server.sin_family = AF_INET;
	server.sin_port = htons( Port );

	//Connect to remote server
	if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0){
		puts("connect error");
		//return 1;
	}	
	puts("Connected\n");
	
	//Send inquiry code
	for(int i=0; i<7 ; i++)
	{
		if( send(socket_desc ,InquiryCode[i] , sizeof(InquiryCode[0]) , 0) < 0)
		{
		puts("Send failed");
		//return 1;
		}
		puts("Data Send\n");
		
		//Receive a reply from the server
		if (recv(socket_desc, server_reply , 200 , 0) < 0)
		{
			puts("recv failed");
		}
		ReceiveMessage[15] = i + '0';
		puts(ReceiveMessage);
		
		//Store the sensing value in array
		if(i==4)
		{
			ReturnValue[i][0] = server_reply[3];
			ReturnValue[i][1] = server_reply[4];
			ReturnValue[i][0] = server_reply[5];
			ReturnValue[i][1] = server_reply[6];
			continue;
		}
		ReturnValue[i][0] = server_reply[3];
		ReturnValue[i][1] = server_reply[4];
		sleep(1);	
		}
	
	//Printing the results
	for (int i = 0; i< 7 ; i++) 
	{
        	for(int j=0;j<4;j++)
		{
			if(i!=4 && j>=2)
			{
				continue;
			}
			printf("%x", ReturnValue[i][j]);
			printf(" ");
		}
		printf("\n");
	}
	close(socket_desc);
	sleep(3);
	}
	return ReturnValue;	
}
