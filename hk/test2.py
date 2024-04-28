# coding=utf-8

import os
import platform
# import tkinter
# from tkinter import *
from HCNetSDK import *
from PlayCtrl import *
from time import sleep
# import numpy as np
# import cv2
# 登录的设备信息
DEV_IP = create_string_buffer(b'192.168.44.64')
DEV_PORT = 8011
DEV_USER_NAME = create_string_buffer(b'admin')
DEV_PASSWORD = create_string_buffer(b'air12345678')

print('DEV_IP:', DEV_IP)

WINDOWS_FLAG = True
win = None  # 预览窗口
funcRealDataCallBack_V30 = None  # 实时预览回调函数，需要定义为全局的

PlayCtrl_Port = c_long(-1)  # 播放句柄
Playctrldll = None  # 播放库
FuncDecCB = None   # 播放库解码回调函数，需要定义为全局的

# 获取当前系统环境
def GetPlatform():
    sysstr = platform.system()
    print('' + sysstr)
    if sysstr != "Windows":
        global WINDOWS_FLAG
        WINDOWS_FLAG = False

# 设置SDK初始化依赖库路径
def SetSDKInitCfg():
    # 设置HCNetSDKCom组件库和SSL库加载路径
    # print(os.getcwd())
    if WINDOWS_FLAG:
        strPath = os.getcwd().encode('gbk')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll'))
        Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\libssl-1_1-x64.dll'))
    else:
        strPath = os.getcwd().encode('utf-8')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))

def LoginDev(Objdll):
    # 登录注册设备
    # device_info = NET_DVR_DEVICEINFO_V30()
    # lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    # device_info = NET_DVR_DEVICEINFO_V30()
    # lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))

    device_info = NET_DVR_DEVICEINFO_V40()
    DEV_info = NET_DVR_USER_LOGIN_INFO()
    # DEV_info.byLoginMode = 0
    DEV_info.sDeviceAddress = bytes("192.168.44.64", "ascii")
    DEV_info.wPort = 8011
    # DEV_info.bUseAsynLogin=0
    DEV_info.sUserName = bytes("admin", "ascii")
    DEV_info.sPassword = bytes("air12345678", "ascii")
    # DEV_info.byLoginMode = 1
    lUserId = Objdll.NET_DVR_Login_V40(byref(DEV_info), byref(device_info))

    return (lUserId, device_info)


def OpenPreview(Objdll, lUserId, callbackFun):
    '''
    打开预览
    '''
    preview_info = NET_DVR_PREVIEWINFO()
    preview_info.hPlayWnd = 1
    preview_info.lChannel = 1  # 通道号
    preview_info.dwStreamType = 0  # 主码流
    preview_info.dwLinkMode = 1  # TCP
    preview_info.bBlocked = 1  # 阻塞取流

    # 开始预览并且设置回调函数回调获取实时流数据
    lRealPlayHandle = Objdll.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), None, None)
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock(lUserId,bytes('./pic/test.jpg', encoding="utf-8"))
    import time
    time.sleep(2)
    print('---------------------1-----: %d' % Objdll.NET_DVR_GetLastError(),lRealPlayHandle)     
    
    return lRealPlayHandle


if __name__ == '__main__':
    # 创建窗

    # 获取系统平台
    GetPlatform()

    # 加载库,先加载依赖库
    if WINDOWS_FLAG:
        
        os.chdir(r'./lib/win')
        Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
        
    else:
        os.chdir(r'./lib')
        Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
        Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')

    SetSDKInitCfg()  # 设置组件库和SSL库加载路径

    # 初始化DLL
    Objdll.NET_DVR_Init()
    # 启用SDK写日志
    # Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)
   
    # 获取一个播放句柄
    if not Playctrldll.PlayM4_GetPort(byref(PlayCtrl_Port)):
        print(u'获取播放库句柄失败')

    # 登录设备
    (lUserId, device_info) = LoginDev(Objdll)
    if lUserId < 0:
        err = Objdll.NET_DVR_GetLastError()
        print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()
    # print('Login device success',lUserId,dir(device_info),device_info.__dict__)
    # 定义码流回调函数
    # funcRealDataCallBack_V30 = REALDATACALLBACK(RealDataCallBack_V30)
    # 开启预览
    lRealPlayHandle = OpenPreview(Objdll, lUserId, None)
    
    dwPicSize = 1440*2560*30

    jpeg_pic_buffer = create_string_buffer(dwPicSize)
    lpSizeReturned = ctypes.c_ulong()
    # sPicFileName =   # 保存图片的文件名
    print('os.getcwd', os.getcwd())
    # os.chdir(r'../../')
    # print(Objdll.NET_DVR_SetCapturePictureMode(1))
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock(lUserId, b"1.jpg")
    # print(Objdll.NET_DVR_SetCapturePictureMode(1))
    try:
        while True:
            lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock_New(lUserId,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
            print('---------------------2-----: %d' % Objdll.NET_DVR_GetLastError(),lRealPlayHandle)    
            # print(jpeg_pic_buffer.raw)
            image_array = np.frombuffer(jpeg_pic_buffer, dtype=np.uint8)
            image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
            # h,w,c = image.shape
            # print(h,w,c,dwPicSize,h*w*c)
            resized_image = cv2.resize(image, (512, 512), interpolation=cv2.INTER_AREA)

            cv2.imshow('Image', resized_image)
            cv2.waitKey(1)
    except KeyboardInterrupt:

        pic = NET_DVR_JPEGPARA()
        pic.wPicSize = 8
        pic.wPicQuality = 1
        print('os.getcwd', os.getcwd())
        os.chdir(r'../../')
        # lRealPlayHandle = Objdll.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(pic), bytes('./pic/test.jpg', encoding="utf-8"))



        if lRealPlayHandle < 0:
            print ('Open preview fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
            # 登出设备
            Objdll.NET_DVR_Logout(lUserId)
            # 释放资源
            Objdll.NET_DVR_Cleanup()
            exit()



        Objdll.NET_DVR_StopRealPlay(lRealPlayHandle)
        # sleep(14)

        if PlayCtrl_Port.value > -1:
            Playctrldll.PlayM4_Stop(PlayCtrl_Port)
            Playctrldll.PlayM4_CloseStream(PlayCtrl_Port)
            Playctrldll.PlayM4_FreePort(PlayCtrl_Port)
            PlayCtrl_Port = c_long(-1)

        # 登出设备
        Objdll.NET_DVR_Logout(lUserId)

        # 释放资源
        Objdll.NET_DVR_Cleanup()

