/*
*****************************************************************
Project: Unmmaned surface vehicle
File name:GetDataFromSensors.h
related file:GetDataFromSensors.c Main_PostDataToServer.c
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
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

char* GetDataFromSensors(const char* Ip, const int Port);
