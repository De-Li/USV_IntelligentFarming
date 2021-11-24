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
---------------------------------------------------------------
******************************************************************
*/
#include<stdio.h>
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h>	//inet_addr
#include<unistd.h>
#include"GetDataFromSensors.h"

//char* GetDataFromSensors(const char* Ip, const int Port){
int main(int argc , char *argv[]){
	char* Ip = "192.168.0.200";
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
	/*
	//溶氧值
	unsigned char InquiryCode[0] ={0x01, 0x03, 0x00, 0x30, 0x00, 0x01, 0x84, 0x05};
	//水溫
	unsigned char InquiryCode[1] ={0x01, 0x03, 0x00, 0x2b, 0x00, 0x01, 0xf4, 0x02};
	//水質ORP
	unsigned char InquiryCode[2] ={0x01, 0x03, 0x00, 0x31, 0x00, 0x01, 0xd5, 0xc5};
	//濁度
	unsigned char InquiryCode[3] ={0x01, 0x03, 0x00, 0x4c, 0x00, 0x01, 0x45, 0xdd};
	//氨氮值
	unsigned char InquiryCode[4] ={0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xcb};
	//電導率
	unsigned char InquiryCode[5] ={0x01, 0x03, 0x00, 0x2e, 0x00, 0x01, 0xe4, 0x03};
	//PH值
	unsigned char InquiryCode[6] ={0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x54, 0x08};
	*/
	char ReturnValue[7][4]; 
	int socket_desc;
	struct sockaddr_in server;
	//Receive buffer
	unsigned char server_reply[200];
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
		return 1;
	}	
	puts("Connected\n");
	
	//Send inquiry code
	for(int i=0; i<7 ; i++)
	{
		if( send(socket_desc ,InquiryCode[i] , sizeof(InquiryCode[0]) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 1\n");
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
	for (int i = 0; i< 8 ; i++) 
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
	return 0;
	/*	
	//DissolvedOxygenValue_InquiryCode
	if( send(socket_desc ,DissolvedOxygenValue_InquiryCode , sizeof(DissolvedOxygenValue_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 1\n");
	//Store the sensing value in array
	ReturnValue[0][0] = server_reply[3];
	ReturnValue[0][1] = server_reply[4];
	sleep(1);	
	
	//WaterTemperature_InquiryCode
	if( send(socket_desc ,WaterTemperature_InquiryCode , sizeof(WaterTemperature_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 2\n");
	//Store the sensing value in array
	ReturnValue[1][0] = server_reply[3];
	ReturnValue[1][1] = server_reply[4];
	sleep(1);
		
	//OxidationReductionPotential_InquiryCode
	if( send(socket_desc ,OxidationReductionPotential_InquiryCode , sizeof(OxidationReductionPotential_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 3\n");
	//Store the sensing value in array
	ReturnValue[2][0] = server_reply[3];
	ReturnValue[2][1] = server_reply[4];
	sleep(1);
		
	//Turbidity_InquiryCode
	if( send(socket_desc ,Turbidity_InquiryCode , sizeof(Turbidity_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 4\n");
	//Store the sensing value in array
	ReturnValue[3][0] = server_reply[3];
	ReturnValue[3][1] = server_reply[4];
	sleep(1);
		
	//AmmoniacalNitrogen_InquiryCode
	if( send(socket_desc ,AmmoniacalNitrogen_InquiryCode , sizeof(AmmoniacalNitrogen_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 5\n");
	//Store the sensing value in array
	ReturnValue[4][0] = server_reply[3];
	ReturnValue[4][1] = server_reply[4];
	ReturnValue[4][0] = server_reply[5];
	ReturnValue[4][1] = server_reply[6];
	sleep(1);
		
	//Conductivity_InquiryCode
	if( send(socket_desc ,Conductivity_InquiryCode , sizeof(Conductivity_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 6\n");
	//Store the sensing value in array
	ReturnValue[5][0] = server_reply[3];
	ReturnValue[5][1] = server_reply[4];
	sleep(1);
		
	//PHValue_InquiryCode
	if( send(socket_desc ,PHValue_InquiryCode , sizeof(PHValue_InquiryCode) , 0) < 0){
		puts("Send failed");
		return 1;
	}
	puts("Data Send\n");
	//Receive a reply from the server
	if (recv(socket_desc, server_reply , 200 , 0) < 0){
		puts("recv failed");
	}
	puts("Reply received 7\n");
	//Store the sensing value in array
	ReturnValue[6][0] = server_reply[3];
	ReturnValue[6][1] = server_reply[4];
	*/	
}
