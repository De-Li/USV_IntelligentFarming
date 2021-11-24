/*
*****************************************************************
Project: Unmmaned surface vehicle
File name:Main_PostDataToServer.c
related file:GetDataFromSensors.h, GetDataFromSensors.c
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/11/24
The Info of water sensors wifi adapter 
IP：192.168.0.200
PORT：6969
---------------------------------------------------------------
Log:
---------------------------------------------------------------
******************************************************************
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include "GetDataFromSensors.h"
#define PORTOFSERVER 30000 /* Open Port on Remote Host */
#define IPOFSERVER "140.116.201.71"
#define MAXDATASIZE 200 /* Max number of bytes of data */

int main(int argc, char *argv[])
{
    char* IpOfWaterSensors = "192.168.0.200";
    int PortOfWaterSensors = 6969;
    char* DataFromWaterSensors =  GetDataFromSensors(IpOfWaterSensors, PortOfWaterSensors); 
    /*
    int sockfd;
    char buffer[MAXDATASIZE];
    char *hello = "Hello from client";
    struct sockaddr_in     servaddr;
   
    // Creating socket file descriptor
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }
   
    memset(&servaddr, 0, sizeof(servaddr));
       
    // Filling server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    servaddr.sin_addr.s_addr = ADDRESSOFSERVER;
       
    int n, len;
       
    sendto(sockfd, (const char *)hello, strlen(hello),
        MSG_CONFIRM, (const struct sockaddr *) &servaddr, 
            sizeof(servaddr));
    printf("Hello message sent.\n");
           
    n = recvfrom(sockfd, (char *)buffer, MAXLINE, 
                MSG_WAITALL, (struct sockaddr *) &servaddr,
                &len);
    buffer[n] = '\0';
    printf("Server : %s\n", buffer);
   
    close(sockfd);
    */
    return 0;
}
