# coding=utf-8

import time
import os
import platform
# import tkinter
# from tkinter import *
from HCNetSDK import *
from PlayCtrl import *
# from time import sleep
# import numpy as np
# import cv2
# 登录的设备信息
# DEV_IP = create_string_buffer(b'192.168.44.64')
# DEV_PORT = 8011
# DEV_USER_NAME = create_string_buffer(b'admin')
# DEV_PASSWORD = create_string_buffer(b'air12345678')

# print('DEV_IP:', DEV_IP)

# WINDOWS_FLAG = True
# win = None  # 预览窗口
funcRealDataCallBack_V30 = None  # 实时预览回调函数，需要定义为全局的

PlayCtrl_Port = c_long(-1)  # 播放句柄
Playctrldll = None  # 播放库
FuncDecCB = None   # 播放库解码回调函数，需要定义为全局的
x = 0
# 获取当前系统环境
def GetPlatform():
    sysstr = platform.system()
    # print('' + sysstr)
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
    device_info = NET_DVR_DEVICEINFO_V40()
    DEV_info = NET_DVR_USER_LOGIN_INFO()
    # DEV_info.byLoginMode = 0
    DEV_info.sDeviceAddress = bytes("192.168.44.64", "ascii")
    DEV_info.wPort = 8011
    DEV_info.bUseAsynLogin=0
    DEV_info.sUserName = bytes("admin", "ascii")
    DEV_info.sPassword = bytes("air12345678", "ascii")
    # DEV_info.byLoginMode = 1
    lUserId = Objdll.NET_DVR_Login_V40(byref(DEV_info), byref(device_info))

    # device_info = NET_DVR_DEVICEINFO_V30()
    # lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    if lUserId < 0:
        err = Objdll.NET_DVR_GetLastError()
        print('Login device fail,%d error code is: %d' % (err,Objdll.NET_DVR_GetLastError()))
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()
    # else:
    #     print('登录成功，设备序列号：%s' % str(device_info.struDeviceV30.sSerialNumber, encoding = "utf8"))
    return (lUserId, device_info)

def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    global x
    # 解码回调函数
    # print("------------2")
    if pFrameInfo.contents.nType == 3:
        # 解码返回视频YUV数据，将YUV数据转成jpg图片保存到本地
        # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
        sFileName = ('../../pic/test_stamp[%d].jpg'% pFrameInfo.contents.nStamp)
        nWidth = pFrameInfo.contents.nWidth
        nHeight = pFrameInfo.contents.nHeight
        nType = pFrameInfo.contents.nType
        dwFrameNum = pFrameInfo.contents.dwFrameNum
        nStamp = pFrameInfo.contents.nStamp
        dwPicSize = nWidth*nHeight*2
        jpeg_pic_buffer = create_string_buffer(dwPicSize)
        pJpeg = (ctypes.c_ubyte * dwPicSize)()
        lpSizeReturned = ctypes.c_ulong()
        # print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)

        # lRet = Playctrldll.PlayM4_ConvertToJpegFile(pBuf, nSize, nWidth, nHeight, nType, c_char_p(sFileName.encode()))
        lRet = Playctrldll.PlayM4_GetJPEG(nPort,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
        import numpy
        import cv2
        image_array = numpy.frombuffer(jpeg_pic_buffer, dtype=numpy.uint8)
        # print('image_array:',image_array)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # width, height, channels = 640, 480, 3
        print(len(image_array))
        # 将一维数组重新构造成相应维度的数组
        # image_array = image_array.reshape(nHeight, nWidth, -1)

        # 假设 x1, y1, x2, y2 是你要剪切的区域的左上角和右下角的坐标
        # x1, y1, x2, y2 = 100, 100, 300, 300

        # 使用切片操作剪切出感兴趣的区域
        # cropped_image = image_array[y1:y2, x1:x2]
        # image = cv2.imdecode(cropped_image, flags=cv2.IMREAD_COLOR)
        # h,w,c = image.shape
        # print(h,w,c,dwPicSize,h*w*c)
        x = x+1
        print(x)
        # image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_NEAREST)
        # cv2.imwrite(sFileName, image)
        # time.sleep(1)
        # resized_image = cv2.imread(sFileName)
        # cv2.imshow('Image', image)
        cv2.waitKey(1)
        # print("------>",lRet,Playctrldll.PlayM4_GetLastError(nPort))
        # print(jpeg_pic_buffer.value)
        # if lRet == 0:
        #     print('PlayM4_ConvertToJpegFile fail, error code is:', Playctrldll.PlayM4_GetLastError(nPort))
        # else:
        #     print('PlayM4_ConvertToJpegFile success')


def RealDataCallBack_V30(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    # 码流回调函数
    if dwDataType == NET_DVR_SYSHEAD:
        # 设置流播放模式
        Playctrldll.PlayM4_SetStreamOpenMode(PlayCtrl_Port, 0)
        # 打开码流，送入40字节系统头数据
        if Playctrldll.PlayM4_OpenStream(PlayCtrl_Port, pBuffer, dwBufSize, 1024*1024):
            # 设置解码回调，可以返回解码后YUV视频数据
            # global FuncDecCB
            # FuncDecCB = DECCBFUNWIN(DecCBFun)
            # Playctrldll.PlayM4_SetDecCallBackExMend(PlayCtrl_Port, FuncDecCB, None, 0, None)
            # 开始解码播放
            if Playctrldll.PlayM4_Play(PlayCtrl_Port, None):
                print(u'播放库播放成功')
            else:
                print(u'播放库播放失败')
        else:
            print(u'播放库打开流失败')
    elif dwDataType == NET_DVR_STREAMDATA:
        # print("----")
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
    preview_info.dwStreamType = 1  # 主码流
    preview_info.dwLinkMode = 1  # TCP
    preview_info.bBlocked = 1  # 阻塞取流
    print("--------------5")
    # 开始预览并且设置回调函数回调获取实时流数据
    lRealPlayHandle = Objdll.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun, None)
    print("--------------6")
    if lRealPlayHandle < 0:
        print("lRealPlayHandle111",lRealPlayHandle)
    # dwPicSize = 1440*2560*50
    # import time
    # time.sleep(5)
    # jpeg_pic_buffer = create_string_buffer(dwPicSize)
    # lpSizeReturned = ctypes.c_ulong()
    # Objdll.NET_DVR_SetCapturePictureMode(1)
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock_New(lUserId,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
    # print('---------------------2-----: %d' % Objdll.NET_DVR_GetLastError(),lRealPlayHandle)    
    return lRealPlayHandle


if __name__ == '__main__':

    GetPlatform()

    # 加载库,先加载依赖库
    if WINDOWS_FLAG:
        os.chdir(r'./lib/win')
        Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
    else:
        os.chdir(r'./lib/linux')
        Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
        Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')

    SetSDKInitCfg()  # 设置组件库和SSL库加载路径

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
    print("-----ok")

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


    # dwPicSize = 1024*1024*2
    # jpeg_pic_buffer = create_string_buffer(dwPicSize)
    # pJpeg = (ctypes.c_ubyte * dwPicSize)()
    # lpSizeReturned = ctypes.c_ulong()

    # lRet = Playctrldll.PlayM4_GetJPEG(PlayCtrl_Port,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
    time.sleep(3)

    dwPicSize = 1024*1024*3
    jpeg_pic_buffer = create_string_buffer(dwPicSize)
    pJpeg = (ctypes.c_ubyte * dwPicSize)()
    lpSizeReturned = ctypes.c_ulong()

    for i in range(0,1000):

        # print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)

        # lRet = Playctrldll.PlayM4_ConvertToJpegFile(pBuf, nSize, nWidth, nHeight, nType, c_char_p(sFileName.encode()))
        # time.sleep(0.001)
        start_time = time.time()

        lRet = Playctrldll.PlayM4_GetJPEG(PlayCtrl_Port,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
        print('---------------------2-----: {}-{}-{}'.format(Objdll.NET_DVR_GetLastError(), lRet, lpSizeReturned))
        end1_time = time.time()
        import numpy
        import cv2
        image_array = numpy.frombuffer(jpeg_pic_buffer, dtype=numpy.uint8)
        # print('image_array:',image_array)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # width, height, channels = 640, 480, 3
        image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
        s=0
        end2_time = time.time()
        # try:
        #     h,w,s = image.shape
        # except:
        #     h,w = image.shape
        # print(h,w,s)
        # print(len(image_array))
        
        try:
            # image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_NEAREST)
            image = image[0:500, 0:500]
            # sFileName = ('../../pic/test_stamp[%d].jpg'% i)
            # cv2.imwrite(sFileName, image)
            cv2.imshow('Image', image)
            end2_time = time.time()
            cv2.waitKey(1)
            print('执行时间：', end1_time - start_time,end2_time - start_time)
        except:
            pass
        
    # time.sleep(10)

    # sPicFileName =   # 保存图片的文件名
    # print('os.getcwd', os.getcwd())
    # os.chdir(r'../../')
    # print(Objdll.NET_DVR_SetCapturePictureMode(1))
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock(lUserId, b"1.jpg")
    # print('---------------------1-----: %d' % Objdll.NET_DVR_GetLastError(),lRealPlayHandle) 
    # Objdll.NET_DVR_SetCapturePictureMode(1)
    # import numpy as np
    # import cv2
    # time.sleep(2)
    # dwPicSize = 1440*2560*20
    # jpeg_pic_buffer = create_string_buffer(dwPicSize)
    # lpSizeReturned = ctypes.c_ulong()
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock_New(lUserId,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
    # print('---------------------2-----: %d' % Objdll.NET_DVR_GetLastError(),lRealPlayHandle)  
    # pic = NET_DVR_JPEGPARA()
    # pic.wPicSize = 8
    # pic.wPicQuality = 1
    # print('os.getcwd', os.getcwd())
    # os.chdir(r'../../')
    # lRealPlayHandle = Objdll.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(pic), bytes('./pic/test.jpg', encoding="utf-8"))
    # # print('pic:', dir(pic))                                                   ../../pic/test.jpg
    # print('lRealPlayHandle:', dir(lRealPlayHandle))
    # print('pic:', pic)
    # print('lRealPlayHandle:', lRealPlayHandle)
    # if lRealPlayHandle < 0:
    #     print ('Open preview fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
    #     # 登出设备
    #     Objdll.NET_DVR_Logout(lUserId)
    #     # 释放资源
    #     Objdll.NET_DVR_Cleanup()
    #     exit()

    #show Windows
    # win.mainloop()


    # 云台控制
    # lRet = Objdll.NET_DVR_PTZControl_Other(lUserId, 1, ZOOM_IN, 0)
    # if lRet == 0:
    #     print('Stop ptz control fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
    # else:
    #     print('Stop ptz control success')

    # sleep(3)

    # # 停止云台控制
    # lRet = Objdll.NET_DVR_PTZControl_Other(lUserId, 1, ZOOM_IN, 1)
    # if lRet == 0:
    #     print('Stop ptz control fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
    # else:
    #     print('Stop ptz control success')
    # 关闭预览
    # Objdll.NET_DVR_StopRealPlay(lRealPlayHandle)
    # sleep(14)
    # pic = NET_DVR_JPEGPARA()
    # pic.wPicSize = 8
    # pic.wPicQuality = 1
    # print('os.getcwd', os.getcwd())
    # os.chdir(r'../../')

    # dwPicSize = 1024*1024*5
    # jpeg_pic_buffer = create_string_buffer(dwPicSize)
    # lpSizeReturned = ctypes.c_ulong()
    # # lRealPlayHandle = Objdll.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(pic), bytes('./pic/test.jpg', encoding="utf-8"))
    # # print(Objdll.NET_DVR_SetCapturePictureMode(1))
    # lRealPlayHandle = Objdll.NET_DVR_CapturePictureBlock_New(lUserId,jpeg_pic_buffer,dwPicSize,ctypes.byref(lpSizeReturned))
    # print('Stop ptz control fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
    # import time
    # time.sleep(2)
    # print('lRealPlayHandle:', lRealPlayHandle,lpSizeReturned)

    # image_array = np.frombuffer(jpeg_pic_buffer, dtype=np.uint8)
    # print('image_array:',jpeg_pic_buffer.raw)
    # # 解码为图像
    # image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

    # # 显示图像
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.imshow('pic',pic)
    # cv2.waitKey(0)
    # print(jpeg_pic_buffer.raw,pic)
    # if lRealPlayHandle == 0:
    #     err = Objdll.NET_DVR_GetLastError()
    #     print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
    #     # 释放资源
    #     Objdll.NET_DVR_Cleanup()
    #     exit()
    # print('lRealPlayHandle:', lRealPlayHandle,jpeg_pic_buffer)                                                   # ../../pic/test.jpg
    # 停止解码，释放播放库资源
    # if PlayCtrl_Port.value > -1:
    #     Playctrldll.PlayM4_Stop(PlayCtrl_Port)
    #     Playctrldll.PlayM4_CloseStream(PlayCtrl_Port)
    #     Playctrldll.PlayM4_FreePort(PlayCtrl_Port)
    #     PlayCtrl_Port = c_long(-1)

    # 登出设备
    Objdll.NET_DVR_Logout(lUserId)

    # 释放资源
    Objdll.NET_DVR_Cleanup()

