/*
 * Copyright(C) 2011,Hikvision Digital Technology Co., Ltd
 *
 * File   name：main.cpp
 * Discription：demo for muti thread get stream
 * Version    ：1.0
 * Author     ：luoyuhua
 * Create Date：2011-12-10
 * Modification History：
 */

#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <errno.h>
#include "HCNetSDK.h"
#include "LinuxPlayM4.h"
// #include "DataType.h"
#include "iniFile.h"
#include <vector>  
#include <unistd.h>
#include <opencv2/opencv.hpp>
typedef unsigned char*          PBYTE;
LONG nport=1;
// dad
//  using namespace cv;
//  取流相关信息，用于线程传递
typedef struct tagREAL_PLAY_INFO
{
	char szIP[16];
	int iUserID;
	int iChannel;
} REAL_PLAY_INFO, *LPREAL_PLAY_INFO;

// 回调实时流，由于调用NET_DVR_SaveRealData，此处不处理
void g_RealDataCallBack_V30(LONG lRealHandle, DWORD dwDataType, BYTE *pBuffer, DWORD dwBufSize, void *dwUser)
{
	// LPREAL_PLAY_INFO pPlayInfo = (LPREAL_PLAY_INFO)dwUser;
	// printf("[g_RealDataCallBack_V30]Get data, ip=%s, channel=%d, handle=%d, data size is %d, thread=%d\n",
	// pPlayInfo->szIP, pPlayInfo->iChannel, lRealHandle, dwBufSize, pthread_self());

	// printf("[g_RealDataCallBack_V30]Get data, handle=%d, data size is %d, thread=%d\n",
	// lRealHandle, dwBufSize, pthread_self());
	// NET_DVR_SaveRealData(lRealHandle, cFilename);
}

// 全局变量，用于标识是否处于 I 帧状态
bool g_isIFrame = false;

// 提取并显示每一帧图片的函数
void ProcessFrame(unsigned char *pBuffer, int nSize)
{
	if (g_isIFrame)
	{
		printf("----1----\n");
		// 使用 OpenCV 将数据转换为图像
		cv::Mat frame(1, nSize, CV_8UC1, pBuffer);
		// std::cout << frame <<std::endl;
		cv::Mat image = cv::imdecode(frame, cv::IMREAD_COLOR);
		if (!image.empty())
		{
			// 显示图片
			cv::imshow("Frame", image);
			cv::waitKey(1); // 显示图片并等待一会，避免程序立即退出
		}
		else
		{
			std::cerr << "Failed to decode image." << std::endl;
		}
		// 显示图片
		// cv::imshow("Frame", image);
		// cv::waitKey(1); // 显示图片并等待一会，避免程序立即退出
	}
}

void PsDataCallBack(LONG lRealHandle, DWORD dwDataType, BYTE *pPacketBuffer, DWORD nPacketSize, void *pUser)
{
	// std::cerr << dwDataType << std::endl;
	// if (dwDataType == NET_DVR_SYSHEAD) {
	//     // 如果是系统头，可能需要处理一些额外的信息，但在此示例中我们不需要
	//     // 这里我们简单地假设每个系统头后面都跟着一个 I 帧
	//     g_isIFrame = true;
	// } else if(dwDataType ==NET_DVR_STREAMDATA) {
	//     // 如果不是系统头，则可能是数据帧
	//     if (g_isIFrame) {
	//         // 如果处于 I 帧状态，就处理当前帧
	//         ProcessFrame(pPacketBuffer, nPacketSize);
	// 		// printf("----1----\n");
	//     }
	// }

	if (dwDataType == NET_DVR_SYSHEAD)
	{
		PlayM4_SetStreamOpenMode(nport, 0);
		if (PlayM4_OpenStream(nport, pPacketBuffer, nPacketSize, 1024 * 1024))
		{
			if (PlayM4_Play(nport, NULL))
			{
				std::cout << "播放库播放成功" << std::endl;
				// print(u'播放库播放成功')
			}

			else
			{
				std::cout << "播放库播放失败" << std::endl;
			}
		}
		else
		{
			std::cout << "播放库打开流失败" << std::endl;
		}
	}
	else if (dwDataType == NET_DVR_STREAMDATA)
	{
		// 如果不是系统头，则可能是数据帧
		PlayM4_InputData(nport, pPacketBuffer, nPacketSize);
	}
}

FILE *g_pFile = NULL;

// void PsDataCallBack(LONG lRealHandle, DWORD dwDataType,BYTE *pPacketBuffer,DWORD nPacketSize, void* pUser)
// {

// 	if (dwDataType  == NET_DVR_SYSHEAD)
// 	{
// 		//写入头数据
// 		g_pFile = fopen("./record/ps.txt", "wb");

// 		if (g_pFile == NULL)
// 		{
// 			printf("CreateFileHead fail\n");
// 			return;
// 		}

// 		//写入头数据
// 		fwrite(pPacketBuffer, sizeof(unsigned char), nPacketSize, g_pFile);
// 		printf("write head len=%d\n", nPacketSize);
// 			for (int i = 0; i < nPacketSize; i++)
// 			{
// 				// std::cout << "%d"(*pPacketBuffer++) <<std::endl;
// 				printf("%x",*pPacketBuffer);
// 				pPacketBuffer++;
// 			}
// 			std::cout << std::endl;
// 		// std::cout << *pPacketBuffer << nPacketSize <<std::endl;
// 	}
// 	else
// 	{
// 		if(g_pFile != NULL)
// 		{
// 			fwrite(pPacketBuffer, sizeof(unsigned char), nPacketSize, g_pFile);
// 			printf("write data len=%d\n", nPacketSize);

// 		}
// 	}

// }

int GetStream()
{
	// 从配置文件读取设备信息
	IniFile ini("Device.ini");
	unsigned int dwSize = 0;
	char sSection[16] = "DEVICE";

	int iRealPlayHandle = 0;
	char *sIP = ini.readstring(sSection, "ip", "error", dwSize);
	int iPort = ini.readinteger(sSection, "port", 0);
	char *sUserName = ini.readstring(sSection, "username", "error", dwSize);
	char *sPassword = ini.readstring(sSection, "password", "error", dwSize);
	int iChannel = ini.readinteger(sSection, "channel", 1);

	NET_DVR_DEVICEINFO_V30 struDeviceInfo;
	int iUserID = NET_DVR_Login_V30(sIP, iPort, sUserName, sPassword, &struDeviceInfo);
	if (iUserID >= 0)
	{

		// NET_DVR_CLIENTINFO ClientInfo = {0};
		// ClientInfo.lChannel     = iChannel;  //channel NO.
		// ClientInfo.lLinkMode    = 0;
		// ClientInfo.sMultiCastIP = NULL;
		// int iRealPlayHandle = NET_DVR_RealPlay_V30(iUserID, &ClientInfo, PsDataCallBack, NULL, 0);
		NET_DVR_PREVIEWINFO struPreviewInfo = {0};
		struPreviewInfo.lChannel = iChannel;
		struPreviewInfo.dwStreamType = 0;
		struPreviewInfo.dwLinkMode = 1;
		struPreviewInfo.bBlocked = 1;
		struPreviewInfo.hPlayWnd=NULL;
		struPreviewInfo.bPassbackRecord = 0;
		iRealPlayHandle = NET_DVR_RealPlay_V40(iUserID, &struPreviewInfo, PsDataCallBack, NULL);
		if (iRealPlayHandle >= 0)
		{
			printf("[GetStream]---RealPlay %s:%d success, \n", sIP, iChannel, NET_DVR_GetLastError());
			// int iRet = NET_DVR_SaveRealData(iRealPlayHandle, "./record/realplay.dat");
			// NET_DVR_SetStandardDataCallBack(iRealPlayHandle, StandardDataCallBack, 0);
		}
		else
		{
			printf("[GetStream]---RealPlay %s:%d failed, error = %d\n", sIP, iChannel, NET_DVR_GetLastError());
		}
	}
	else
	{
		printf("[GetStream]---Login %s failed, error = %d\n", sIP, NET_DVR_GetLastError());
	}
	// return iRealPlayHandle;
	return iUserID;
}



// BOOL PlayM4_GetJPEG(  
// 	LONG     nPort,  
// 	PBYTE    pJpeg,  
// 	DWORD    nBufSize,
//   	DWORD   *pJpegSize);

int main()
{
	NET_DVR_Init();
	std::cout << "PlayM4_GetPort(&nport); = " << PlayM4_GetPort(&nport) << std::endl;

	NET_DVR_SetLogToFile(3, "./record/");
	int iUserID = GetStream();
	// cv::namedWindow("Frame", cv::WINDOW_NORMAL);
	// NET_DVR_API BOOL __stdcall NET_DVR_CapturePictureBlock_New(LONG iRealHandle, char *pPicBuf, DWORD dwPicSize, DWORD *lpSizeReturned);
	char c = 0;
	sleep(1);
	DWORD dwPicSize = 1024*1024*3;
	PBYTE pJpeg2 = NULL;
	DWORD size = 0;
	BOOL ret = 0;
	std::cout << "nport = " << nport << std::endl;
	for (int i = 0; i < 500; i++)
	{
		/* code */
	pJpeg2 = new unsigned char[dwPicSize];
	
	ret = PlayM4_GetJPEG(nport,pJpeg2,dwPicSize,&size);

	// std::cout << ret << "\n" << size << "\n" << *(&pJpeg2) << std::endl;
// for (int i = 0; i < size; i++)
// {
// 	// std::cout  << *(pJpeg2+i) << std::endl;
// 	printf("%d ",(int)*(pJpeg2+i));
// }
	cv::Mat frame(1, size, CV_8UC1, pJpeg2);
	// std::cout << frame <<std::endl;
	cv::Mat image = cv::imdecode(frame, cv::IMREAD_COLOR);

    cv::Mat grayImg;  
  
    // 将彩色图像转换为灰度图像  
    cv::cvtColor(image, grayImg, cv::COLOR_BGR2GRAY);  

    cv::Size size = grayImg.size();  
    std::cout << "Width: " << size.width << ", Height: " << size.height << std::endl;  
  
    // 定义剪裁区域，这里我们剪裁图片的中心部分  
    int crop_x = size.width / 4;  
    int crop_y = size.height / 4;  
    int crop_width = size.width / 2;  
    int crop_height = size.height / 2;  
    cv::Rect roi(0, 0, crop_width, crop_height);  
  
    // 剪裁图片  
    cv::Mat cropped_img = grayImg(roi);  
    // cv::Mat color_image(1080, 1920, CV_8UC3);
  
  
  	char name[] = "name-%d-"; 
    // 检查图像是否正确解码  
    if (!image.empty()) {  
		
		printf("----%d----\n",i);
		sprintf(name,"name-%d-",i);
        cv::imshow("Decoded JPEG Image", cropped_img);  
        // 等待按键事件，0表示无限等待  
        cv::waitKey(1);  
    } else {  
        std::cerr << "无法解码JPEG图像数据" << std::endl;  
    }  

	delete[] pJpeg2;  
	}
	// NET_DVR_CapturePicture(m_lPlayHandle,PicName)

	// DWORD dwPicSize = 1000000;
	// char pPicBuf[dwPicSize]={0};
	// DWORD lpSizeReturned=0;
	// int lRealPlayHandle = NET_DVR_CapturePictureBlock_New(iUserID,pPicBuf,dwPicSize,&lpSizeReturned);
	// int lRealPlayHandle=NET_DVR_CapturePictureBlock(iUserID, "1.jpg",1);


	// NET_DVR_CapturePicture();

	NET_DVR_JPEGPARA pic;
	pic.wPicSize = 9;
	pic.wPicQuality = 2;
	// printf("-----------");
	// int lRealPlayHandle = NET_DVR_CaptureJPEGPicture(iUserID,1,&pic,"./1.jpg");
	// printf("-------------2----%d----%d",NET_DVR_GetLastError() ,lRealPlayHandle);
	// int lRealPlayHandle=0;
	// char *test;
	// for (int i = 0; i < 9; i++)
	// {
	// 	sprintf(test,"./%d.jpg",i);
	// 	lRealPlayHandle = NET_DVR_CaptureJPEGPicture(iUserID,1,&pic,test);
	// 	printf("-------------2----%d----%d",NET_DVR_GetLastError() ,lRealPlayHandle);
	// }

	// while('q' != c)
	// {
	// 	printf("input 'q' to quit\n");
	// 	printf("input: ");
	// 	scanf("%c", &c);
	// }

	cv::destroyAllWindows();
	NET_DVR_Cleanup();
	return 0;
}
