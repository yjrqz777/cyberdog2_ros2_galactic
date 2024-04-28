#!/usr/bin/env python3
# coding=utf-8

import time
import os
import platform
from HCNetSDK import *
from PlayCtrl import *
# from time import sleep
# import numpy as np
# import cv2
# 登录的设备信息
DEV_IP = b'192.168.44.64'
DEV_PORT = 8011
bUseAsynLogin = 0
DEV_USER_NAME = b'admin'
DEV_PASSWORD = b'air12345678'

# print('DEV_IP:', DEV_IP)

# win = None  # 预览窗口
funcRealDataCallBack_V30 = None  # 实时预览回调函数，需要定义为全局的

PlayCtrl_Port = c_long(-1)  # 播放句柄
Playctrldll = None  # 播放库
FuncDecCB = None   # 播放库解码回调函数，需要定义为全局的
x = 0



# 设置SDK初始化依赖库路径
def SetSDKInitCfg():
    # 设置HCNetSDKCom组件库和SSL库加载路径
    print(os.getcwd())
    strPath = os.getcwd().encode('utf-8')
    sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
    sdk_ComPath.sPath = strPath
    Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
    Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
    Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))

def LoginDev(Objdll):
    # 登录注册设备
    device_info = NET_DVR_DEVICEINFO_V40()
    DEV_info = NET_DVR_USER_LOGIN_INFO()
    # DEV_info.byLoginMode = 0
    DEV_info.sDeviceAddress = DEV_IP
    DEV_info.wPort = DEV_PORT
    DEV_info.bUseAsynLogin=0
    DEV_info.sUserName = DEV_USER_NAME
    DEV_info.sPassword = DEV_PASSWORD
    # DEV_info.byLoginMode = 1
    lUserId = Objdll.NET_DVR_Login_V40(byref(DEV_info), byref(device_info))

    if lUserId < 0:
        err = Objdll.NET_DVR_GetLastError()
        print('Login device fail,%d error code is: %d' % (err,Objdll.NET_DVR_GetLastError()))
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()
    return (lUserId, device_info)

def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    import numpy
    import cv2
    if pFrameInfo.contents.nType == 3:
        t0 = time.time()
        # 解码返回视频YUV数据，将YUV数据转成jpg图片保存到本地
        # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
        nWidth = pFrameInfo.contents.nWidth
        nHeight = pFrameInfo.contents.nHeight
        #nType = pFrameInfo.contents.nType
        dwFrameNum = pFrameInfo.contents.dwFrameNum
        nStamp = pFrameInfo.contents.nStamp
        #print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)
        # if self.n == 0:
        #     import numpy as np
        #     # import cv2
        #     self.n=1
        YUV = numpy.frombuffer(pBuf[:nSize],dtype=numpy.uint8)
        YUV = numpy.reshape(YUV,[nHeight+nHeight//2,nWidth])
        img_rgb = cv2.cvtColor(YUV,cv2.COLOR_YUV2BGR_YV12)
        print("-------------------------")

        # image_array = numpy.frombuffer(pBuf, dtype=numpy.uint8)
        # print('image_array:',image_array)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # width, height, channels = 640, 480, 3
        # image = cv2.imdecode(img_rgb, flags=cv2.IMREAD_COLOR)

        try:
            # image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_NEAREST)
            image = img_rgb[0:500, 0:500]
            # sFileName = ('../../pic/test_stamp[%d].jpg'% i)
            # cv2.imwrite(sFileName, image)
            cv2.imshow('Image', image)
            cv2.waitKey(1)
        except:
            pass


def RealDataCallBack_V30(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    # 码流回调函数
    if dwDataType == NET_DVR_SYSHEAD:
        # 设置流播放模式
        Playctrldll.PlayM4_SetStreamOpenMode(PlayCtrl_Port, 0)
        # 打开码流，送入40字节系统头数据
        if Playctrldll.PlayM4_OpenStream(PlayCtrl_Port, pBuffer, dwBufSize, 1024*1024):
            # 设置解码回调，可以返回解码后YUV视频数据
            global FuncDecCB
            FuncDecCB = DECCBFUNWIN(DecCBFun)
            Playctrldll.PlayM4_SetDecCallBackExMend(PlayCtrl_Port, FuncDecCB, None, 0, None)
            # 开始解码播放
            if Playctrldll.PlayM4_Play(PlayCtrl_Port, None):
                print(u'播放库播放成功')
            else:
                print(u'播放库播放失败')
        else:
            print(u'播放库打开流失败')
    elif dwDataType == NET_DVR_STREAMDATA:
        Playctrldll.PlayM4_InputData(PlayCtrl_Port, pBuffer, dwBufSize)
    else:
        print (u'其他数据,长度:', dwBufSize)
        
def OpenPreview(Objdll, lUserId, callbackFun):
    '''
    打开预览
    '''
    preview_info = NET_DVR_PREVIEWINFO()
    # preview_info.hPlayWnd = 0
    preview_info.lChannel = 1  # 通道号
    preview_info.dwStreamType = 0  # 主码流
    preview_info.dwLinkMode = 1  # TCP
    preview_info.bBlocked = 1  # 阻塞取流
    # 开始预览并且设置回调函数回调获取实时流数据
    lRealPlayHandle = Objdll.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun, None)
    if lRealPlayHandle < 0:
        print("lRealPlayHandle111",lRealPlayHandle)
    return lRealPlayHandle


if __name__ == '__main__':

    os.chdir(r'./lib/linux64')
    Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
    Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')

    SetSDKInitCfg()  # 设置组件库和SSL库加载路径

    Objdll.NET_DVR_Init()
   
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

    funcRealDataCallBack_V30 = REALDATACALLBACK(RealDataCallBack_V30)
    # 开启预览
    lRealPlayHandle = OpenPreview(Objdll, lUserId, funcRealDataCallBack_V30)
    if lRealPlayHandle < 0:
        print ('Open preview fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        # 登出设备
        Objdll.NET_DVR_Logout(lUserId)
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()

    time.sleep(30)

    # dwPicSize = 1080*1920*2
    # jpeg_pic_buffer = create_string_buffer(dwPicSize)
    # pJpeg = (ctypes.c_ubyte * dwPicSize)()
    # lpSizeReturned = ctypes.c_ulong()

    # for i in range(0,10000):

    #     # print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)

    #     # lRet = Playctrldll.PlayM4_ConvertToJpegFile(pBuf, nSize, nWidth, nHeight, nType, c_char_p(sFileName.encode()))
    #     # time.sleep(0.001)
    #     start_time = time.time()

    #     lRet = Playctrldll.PlayM4_GetJPEG(PlayCtrl_Port,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
    #     print('---------------------2-----: {}-{}-{}'.format(Objdll.NET_DVR_GetLastError(), lRet, lpSizeReturned))
    #     end1_time = time.time()
    #     import numpy
    #     import cv2
    #     image_array = numpy.frombuffer(jpeg_pic_buffer, dtype=numpy.uint8)
        # print('image_array:',image_array)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # width, height, channels = 640, 480, 3
        # image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
        # s=0
        # end2_time = time.time()
        # # try:
        # #     h,w,s = image.shape
        # # except:
        # #     h,w = image.shape
        # # print(h,w,s)
        # # print(len(image_array))
        
        # try:
        #     # image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_NEAREST)
        #     image = image[0:500, 0:500]
        #     # sFileName = ('../../pic/test_stamp[%d].jpg'% i)
        #     # cv2.imwrite(sFileName, image)
        #     cv2.imshow('Image', image)
        #     end2_time = time.time()
        #     cv2.waitKey(1)
        #     print('执行时间：', end1_time - start_time,end2_time - start_time)
        # except:
        #     pass

    # 停止解码，释放播放库资源
    if PlayCtrl_Port.value > -1:
        Playctrldll.PlayM4_Stop(PlayCtrl_Port)
        Playctrldll.PlayM4_CloseStream(PlayCtrl_Port)
        Playctrldll.PlayM4_FreePort(PlayCtrl_Port)
        PlayCtrl_Port = c_long(-1)

    # 登出设备
    Objdll.NET_DVR_Logout(lUserId)

    # 释放资源
    Objdll.NET_DVR_Cleanup()

