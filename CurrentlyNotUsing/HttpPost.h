/*
*****************************************************************
Project: Unmmaned surface vehicle
File name:HttpPost.h
related file:HttpPost.cpp, GetWaterInfo.cpp
function:Posting under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
---------------------------------------------------------------
Log:
---------------------------------------------------------------
******************************************************************
#progma once
#include <string>
#include <vector>
using namespace std;

class HttpPost
{
  private:
    string m_Ip;
    int m_Port;
  
  public:
    //constructor
    HttpPost(const string ip, const int port);
    
    //destructor
    ~HttpPost();
    
    //Http post function
    string PostData(const string data);
    
    //Transfer the string to Json type
    static string GetJson(const string data, int length);
    
}
