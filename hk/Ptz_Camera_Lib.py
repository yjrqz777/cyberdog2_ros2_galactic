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


class Ptz_Camera():
    def __init__(self) -> None:
        self.Objdll = cdll.LoadLibrary('/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib/libhcnetsdk.so')
        self.SetSDKInitCfg()  # 设置组件库和SSL库加载路径
        # 初始化DLL
        self.Objdll.NET_DVR_Init()
        # 获取一个播放句柄
        # 登录设备


        # self.device_info = NET_DVR_DEVICEINFO_V30()

        # self.lUserId = self.Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(self.device_info))
        
        # device_info = NET_DVR_DEVICEINFO_V40()
        # device_info.byLoginMode = 1
        # DEV_info = NET_DVR_USER_LOGIN_INFO()
        # DEV_info.sDeviceAddress = '192.168.44.64'.encode('utf-8')
        # DEV_info.wPort = 8011
        # DEV_info.sUserName = 'admin'.encode('utf-8')
        # DEV_info.sPassword = 'air12345678'.encode('utf-8')
        # DEV_info.byLoginMode = 1
        # self.lUserId = self.Objdll.NET_DVR_Login_V40(byref(DEV_info), byref(device_info))
        
        if self.lUserId < 0:
            err = self.Objdll.NET_DVR_GetLastError()
            print('Login device fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()

    def SetSDKInitCfg(self):
        # 设置HCNetSDKCom组件库和SSL库加载路径
        # strPath = os.getcwd().encode('utf-8')
        strPath = "/SDCARD/workspace/cyberdog2_ros2_galactic/hk/lib".encode('utf-8')
        # print(strPath)
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))


    def LogoutDev(self):
        self.Objdll.NET_DVR_Logout(self.lUserId)
        self.Objdll.NET_DVR_Cleanup()

    def take_pic(self, p_size = 9, p_quality = 0, p_name = 'test'):
        '''
        wPicSize 
        图片尺寸：0-CIF(352*288/352*240)，
        1-QCIF(176*144/176*120)，
        2-4CIF(704*576/704*480)或D1(720*576/720*486)，
        3-UXGA(1600*1200)， 4-SVGA(800*600)，
        5-HD720P(1280*720)，6-VGA(640*480)，7-XVGA(1280*960)，
        8-HD900P(1600*900)，9-HD1080P(1920*1080)，10-2560*1920， 
        11-1600*304，12-2048*1536，13-2448*2048，14-2448*1200，15-2448*800，
        16-XGA(1024*768)，17-SXGA(1280*1024)，18-WD1(960*576/960*480), 19-1080I(1920*1080)，
        20-576*576，21-1536*1536，22-1920*1920，23-320*240，24-720*720，25-1024*768，
        26-1280*1280，27-1600*600， 28-2048*768，29-160*120，75-336*256，78-384*256，
        79-384*216，80-320*256，82-320*192，83-512*384，127-480*272，128-512*272，
        161-288*320，162-144*176，163-480*640，164-240*320，165-120*160，166-576*720，
        167-720*1280，168-576*960，180-180*240, 181-360*480, 182-540*720, 183-720*960, 
        184-960*1280, 185-1080*1440, 500-384*288, 0xff-Auto(使用当前码流分辨率) 
        wPicQuality 
        图片质量系数：0-最好，1-较好，2-一般 
        '''
        # sleep(14)   # 等待14秒，确保摄像头自动聚焦完成
        pic = NET_DVR_JPEGPARA()
        pic.wPicSize = p_size
        pic.wPicQuality = p_quality
        # print('os.getcwd', os.getcwd())
        # os.chdir(r'../../')
        lRealPlayHandle = self.Objdll.NET_DVR_CaptureJPEGPicture(self.lUserId, 1, byref(pic), bytes('//SDCARD/picture/{}.jpg'.format(p_name), encoding="utf-8"))
        print('lRealPlayHandle:', lRealPlayHandle)   

    def take_control(self,control_cmd = 0,control_time = 1):
        '''
        宏定义 宏定义值 含义                 \n
        LIGHT_PWRON 2 接通灯光电源          \n
        WIPER_PWRON 3 接通雨刷开关          \n
        FAN_PWRON 4 接通风扇开关            \n
        HEATER_PWRON 5 接通加热器开关       \n
        AUX_PWRON1 6 接通辅助设备开关       \n
        AUX_PWRON2 7 接通辅助设备开关       \n
        ZOOM_IN 11 焦距变大(倍率变大)       \n
        ZOOM_OUT 12 焦距变小(倍率变小)      \n
        FOCUS_NEAR 13 焦点前调              \n
        FOCUS_FAR 14 焦点后调               \n
        IRIS_OPEN 15 光圈扩大               \n
        IRIS_CLOSE 16 光圈缩小              \n
        TILT_UP 21 云台上仰                 \n
        TILT_DOWN 22 云台下俯               \n
        PAN_LEFT 23 云台左转                \n
        PAN_RIGHT 24 云台右转               \n
        '''
        lRet = self.Objdll.NET_DVR_PTZControl_Other(self.lUserId, 1, control_cmd , 0)
        if lRet == 0:
            print('Stop ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Stop ptz control success')
        sleep(control_time)
        lRet = self.Objdll.NET_DVR_PTZControl_Other(self.lUserId, 1, control_cmd , 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Stop ptz control success')
        if control_cmd ==11 or control_cmd == 12:
            sleep(14)   # 等待14秒，确保摄像头自动聚焦完成
        else:
            sleep(1)

if __name__ == '__main__':
    # 加载库,先加载依赖库
    Ptz_cam = Ptz_Camera()
    # 云台控制 
    Ptz_cam.take_control(TILT_DOWN,1)
    Ptz_cam.take_control(ZOOM_OUT,1)

    Ptz_cam.take_pic(p_size=8,)
    Ptz_cam.LogoutDev()
    # ../../pic/test.jpg
    # 停止解码，释放播放库资源
    # 登出设备


