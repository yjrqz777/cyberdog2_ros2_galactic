# coding=utf-8

import os
import platform
import tkinter
from tkinter import *
from HCNetSDK import *
from PlayCtrl import *
from time import sleep

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
    print(os.getcwd())
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
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    return (lUserId, device_info)


if __name__ == '__main__':
    # 获取系统平台
    GetPlatform()
    # 加载库,先加载依赖库
    if WINDOWS_FLAG:
        os.chdir(r'./hk/lib/win')
        Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
    else:
        os.chdir(r'./hk/lib')
        Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
        Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')
    SetSDKInitCfg()  # 设置组件库和SSL库加载路径
    # 初始化DLL
    Objdll.NET_DVR_Init()
    # 获取一个播放句柄
    # 登录设备


    device_info = NET_DVR_DEVICEINFO_V40()
    # device_info.byLoginMode = 1
    DEV_info = NET_DVR_USER_LOGIN_INFO()
    DEV_info.sDeviceAddress = '192.168.44.64'.encode('utf-8')
    DEV_info.wPort = 80
    DEV_info.sUserName = 'admin'.encode('utf-8')
    DEV_info.sPassword = 'air12345678'.encode('utf-8')
    DEV_info.byLoginMode = 1
    # DEV_info.byProxyType = 0
    DEV_info.byHttps = 0    

    lUserId = Objdll.NET_DVR_Login_V40(byref(DEV_info), byref(device_info))

    if lUserId < 0:
        err = Objdll.NET_DVR_GetLastError()
        print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()
    import grpc
