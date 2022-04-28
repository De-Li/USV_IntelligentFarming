#include <iostream> // for standard I/O
#include <string>   // for strings
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <typeinfo>
#include <math.h>
#include <Windows.h>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>
#include <opencv2/core.hpp>     // Basic OpenCV structures (cv::Mat)
#include<opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>  // Video write
#include <opencv2/imgproc/types_c.h>
#include <opencv2/core/cuda.hpp>
#include <opencv2\core\core.hpp>
#include <opencv2/highgui/highgui.hpp>
#pragma warning(disable : 4996)

using namespace cv;
using namespace std;
int main() {
	//printCudaDeviceInfo(0);
	// Create Background subtractor objects
	
	//Ptr<BackgroundSubtractor> pBackSub;
	//pBackSub = createBackgroundSubtractorMOG2();
	//pBackSub = createBackgroundSubtractorKNN();
	
	VideoCapture capture = VideoCapture(0);

	capture.open("FishVideo_20220322_17_4140-4250.MP4");
	if (!capture.isOpened())
	{
		cout << "Error opening video source!" << endl;
	}
	Mat OriginalFrame, GrayScaleFrame, BlacWhiteFrame;
	Mat ForeGroundMask;
	cout << "into the loop" << endl;
	auto start = chrono::steady_clock::now();
	int NumFrames = 1200;
	time_t Start, End;
	time(&Start);
	int i = 0;
	while (true)
	{
		i++;
		capture >> OriginalFrame;
		if (OriginalFrame.empty())
		{
			cout << "frame is empty" << endl;
			break;
		}
		
		//pBackSub->apply(OriginalFrame, ForeGroundMask, 0.5);
		
		//get the frame number and write it on the current frame
		rectangle(OriginalFrame, cv::Point(10, 2), cv::Point(100, 20),
			cv::Scalar(255, 255, 255), -1);
		stringstream ss;
		ss << capture.get(CAP_PROP_POS_FRAMES);
		string frameNumberString = ss.str();
		putText(OriginalFrame, frameNumberString.c_str(), cv::Point(15, 15),
			FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0));
		
		//cvtColor(OriginalFrame, GrayScaleFrame, CV_RGB2GRAY);
		//Mat bw;
		//threshold(gray, bw, 40, 255, CV_THRESH_BINARY_INV | CV_THRESH_OTSU);
		BlacWhiteFrame = OriginalFrame > 205;
		/*
		vector<Point> White_pixels;   // output, locations of non-zero pixels
		cv::findNonZero(BlacWhiteFrame, White_pixels);
		cout << "Cloud all White pixels: " << White_pixels.size() << endl; // amount of black pix
		if (White_pixels.size() > 200000)
		{
			//write video
			//imshow("Testing Video_OriginalFrame", OriginalFrame);
			//imshow("Testing Video_BlacWhiteFrame", BlacWhiteFrame);
		}
		
		imshow("Testing Video_OriginalFrame", OriginalFrame);
		imshow("Testing Video_BlacWhiteFrame", BlacWhiteFrame);
		//imshow("Testing Video_BlacWhiteFrame", GrayScaleFrame);
		//imshow("Testing Video_ForeGroundMask", ForeGroundMask);
		//get the input from the keyboard
		int keyboard = waitKey(30);
		if (keyboard == 'q' || keyboard == 27)
			break;
		if (i == NumFrames)
		{
			break;
		}
	}
	time(&End);
	double seconds = difftime(End, Start);
	cout << "Time taken : " << seconds << " seconds" << endl;
	double Fps = NumFrames / seconds;
	cout << "Estimated frames per second : " << Fps << endl;
	double fps = capture.get(CAP_PROP_FPS);
	cout << "Frames per second using video.get(CAP_PROP_FPS) : " << fps << endl;
	auto end = chrono::steady_clock::now();
	auto diff = end - start;
	cout << chrono::duration <double, milli>(diff).count() << " ms" << endl;
	capture.release();
	destroyAllWindows();
	system("pause");
	return 0;
}
