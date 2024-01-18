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
DEV_PORT = 8000
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


# 设置SDK初始化依赖库路径
def SetSDKInitCfg():
    # 设置HCNetSDKCom组件库和SSL库加载路径
    print(os.getcwd())
    strPath = "/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib".encode('utf-8')
    print(strPath)
    # strPath = "/SDCARD/workspace/cyberdog2_ros2_galactic/hk"
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

    # os.chdir(r'/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib')
    Objdll = cdll.LoadLibrary(r'/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib/libhcnetsdk.so')
    # Playctrldll = cdll.LoadLibrary(r'/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib/libPlayCtrl.so')

    SetSDKInitCfg()  # 设置组件库和SSL库加载路径

    # 初始化DLL
    Objdll.NET_DVR_Init()
    # 登录设备
    (lUserId, device_info) = LoginDev(Objdll)
    pic = NET_DVR_JPEGPARA()
    pic.wPicSize = 8
    pic.wPicQuality = 1
    # os.chdir(r'../')
    print(os.getcwd())
    lRealPlayHandle = Objdll.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(pic), bytes('/SDCARD/workspace/cyberdog2_ros2_galactic/hk/pic/test.jpg', encoding="utf-8"))
    print(lRealPlayHandle)

    # 登出设备
    Objdll.NET_DVR_Logout(lUserId)

    # 释放资源
    Objdll.NET_DVR_Cleanup()

