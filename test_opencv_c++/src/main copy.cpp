#include <opencv2/opencv.hpp>
// #include <iostream>
// using namespace std;
using namespace cv;

// int main(int argc,char** argv)
// {
//  std::cout<<"hello opencv"<<std::endl;

//  //灰度图显示
//  Mat src = imread("./pic/3.png",IMREAD_GRAYSCALE);//读取进来的数据以矩阵的形势,第二个参数代表显示一张灰度图像。
//  if (src.empty()) 
//  {
//   std::cout<<"could not load image"<<endl;//如果图片不存在 将无法读取，打印到终端。
//  }
//  //超过屏幕的图像无法显示时候调用此函数。
//  namedWindow("输入窗口", WINDOW_GUI_EXPANDED);//创建了一个新窗口，参数1表示名称，第二个参数代表一个自由的比例
//  imshow("输入窗口", src);//表示显示在新创建的输入窗口上，第一个参数表示窗口名称，src表示数据对象Mat 
//  waitKey(0);//执行到这句，程序阻塞。参数表示延时时间。单位ms
//  destroyAllWindows();//销毁前面创建的显示窗口
//  return 0;
// }

#include <stdio.h>
#include <iostream>
// #include "Windows.h"
#include "HCNetSDK.h"
#include <time.h>
#include <cstring>
#include <time.h>
#include <unistd.h>
using namespace std;

// typedef HWND (WINAPI *PROCGETCONSOLEWINDOW)();
// PROCGETCONSOLEWINDOW GetConsoleWindowAPI;

void CALLBACK g_ExceptionCallBack(DWORD dwType, LONG lUserID, LONG lHandle, void *pUser)
{
    char tempbuf[256] = {0};
    switch(dwType) 
    {
    case EXCEPTION_RECONNECT:    //预览时重连
        printf("----------reconnect--------%d\n", time(NULL));
    break;
    default:
    break;
    }
}
void printImageData(char *pPicBuf, DWORD dwPicSize) {
    // 将图片数据按字节打印出来
    for (DWORD i = 0; i < dwPicSize; ++i) {
        std::cout << static_cast<int>(pPicBuf[i]) << " ";
    }
    std::cout << std::endl;
}
int main() {

  //---------------------------------------
  // 初始化
  NET_DVR_Init();
  //设置连接时间与重连时间
  NET_DVR_SetConnectTime(2000, 1);
  NET_DVR_SetReconnect(10000, true);

  //---------------------------------------
  //设置异常消息回调函数
  NET_DVR_SetExceptionCallBack_V30(0, NULL,g_ExceptionCallBack, NULL);

  //---------------------------------------
  // 获取控制台窗口句柄
//   HMODULE hKernel32 = GetModuleHandle("kernel32");
//   GetConsoleWindowAPI = (PROCGETCONSOLEWINDOW)GetProcAddress(hKernel32,"GetConsoleWindow");

  //---------------------------------------
  // 注册设备
  LONG lUserID;

  //登录参数，包括设备地址、登录用户、密码等
  NET_DVR_USER_LOGIN_INFO struLoginInfo = {0};
  struLoginInfo.bUseAsynLogin = 0; //同步登录方式
  strcpy(struLoginInfo.sDeviceAddress, "192.168.44.64"); //设备IP地址
  struLoginInfo.wPort = 8011; //设备服务端口
  strcpy(struLoginInfo.sUserName, "admin"); //设备登录用户名
  strcpy(struLoginInfo.sPassword, "air12345678"); //设备登录密码

  //设备信息, 输出参数
  NET_DVR_DEVICEINFO_V40 struDeviceInfoV40 = {0};

  lUserID = NET_DVR_Login_V40(&struLoginInfo, &struDeviceInfoV40);
  if (lUserID < 0)
  {
      printf("Login failed, error code: %d\n", NET_DVR_GetLastError());
      NET_DVR_Cleanup();
      return 1;
  }

  //---------------------------------------
  //启动预览并设置回调数据流
  LONG lRealPlayHandle;
//   HWND hWnd = GetConsoleWindowAPI();     //获取窗口句柄
  NET_DVR_PREVIEWINFO struPlayInfo = {0};
//   struPlayInfo.hPlayWnd = 1;         //需要SDK解码时句柄设为有效值，仅取流不解码时可设为空
  struPlayInfo.lChannel     = 1;       //预览通道号
  struPlayInfo.dwStreamType = 0;       //0-主码流，1-子码流，2-码流3，3-码流4，以此类推
  struPlayInfo.dwLinkMode   = 0;       //0- TCP方式，1- UDP方式，2- 多播方式，3- RTP方式，4-RTP/RTSP，5-RSTP/HTTP
  struPlayInfo.bBlocked     = 1;       //0- 非阻塞取流，1- 阻塞取流

  lRealPlayHandle = NET_DVR_RealPlay_V40(lUserID, &struPlayInfo, NULL, NULL);
  if (lRealPlayHandle < 0)
  {
      printf("NET_DVR_RealPlay_V40 error\n");
      NET_DVR_Logout(lUserID);
      NET_DVR_Cleanup();
      return 0;
  }else
  {
    std::cout << "lRealPlayHandle = "<<lRealPlayHandle << endl;
  }



    sleep(4);
    NET_DVR_JPEGPARA pic_s = {0};
    pic_s.wPicQuality = 0;
    pic_s.wPicSize = 0;
    std::cout<< NET_DVR_SetCapturePictureMode(1) << endl;
    // char name[50];
    // for (int i = 0; i < 10; i++)
    // {    
    //     sprintf(name,"/home/jetson/my_ros2/test_opencv_c++/build/%d.jpg",i);
    //     std::cout<<  " NET_DVR_Capture="  <<NET_DVR_CaptureJPEGPicture(lUserID,1,&pic_s,name) << endl;
    // }
    
    // std::cout<<  "    NET_DVR_Capture="  <<NET_DVR_CaptureJPEGPicture(lUserID,1,&pic_s,"/home/jetson/my_ros2/test_opencv_c++/build/1.jpg") << endl;
    std::cout << NET_DVR_GetLastError()<< std::endl;
    unsigned long long dwPicSize = 2920687200*2;
    std::cout << "dwPicSize=" <<dwPicSize << std::endl;
    char *pPicBuf = new char[dwPicSize]; // 分配足够的内存用于存放图片数据
    unsigned int lpSizeReturned;
    // int err =  NET_DVR_CaptureJPEGPicture_NEW(lUserID,1,&pic_s,pPicBuf,dwPicSize,&lpSizeReturned);
    std::cout << lpSizeReturned <<"\nerr=="<< err << "\n"<< pPicBuf << std::endl;
    if ( err ==1)
    {
     namedWindow("输入窗口", WINDOW_GUI_EXPANDED);//创建了一个新窗口，参数1表示名称，第二个参数代表一个自由的比例
     imshow("输入窗口", pPicBuf);//表示显示在新创建的输入窗口上，第一个参数表示窗口名称，src表示数据对象Mat         
    }

        // printImageData(pPicBuf, dwPicSize);
    else{
        std::cout << NET_DVR_GetLastError()<< std::endl;
    }





    // sleep(3);
  //---------------------------------------
  //关闭预览
  NET_DVR_StopRealPlay(lRealPlayHandle);
  //注销用户
  NET_DVR_Logout(lUserID);
  //释放SDK资源
  NET_DVR_Cleanup();

  return 0;
}



