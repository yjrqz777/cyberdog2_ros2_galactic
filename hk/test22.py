# coding=utf-8
import os
import platform
from HCNetSDK import *
from PlayCtrl import *
import time

class HKCam(object):
    def __init__(self,camIP,username,password,devport=8011):
        # 登录的设备信息
        self.n = 0
        self.DEV_IP = create_string_buffer(camIP.encode())
        self.DEV_PORT =devport
        self.DEV_USER_NAME = create_string_buffer(username.encode())
        self.DEV_PASSWORD = create_string_buffer(password.encode())
        self.WINDOWS_FLAG = False if platform.system() != "Windows" else True
        self.funcRealDataCallBack_V30 = None
        self.recent_img = None #最新帧
        self.n_stamp = None #帧时间戳
        self.last_stamp = None #上次时间戳
        # 加载库,先加载依赖库                                                                   # 1 根据操作系统，加载对应的dll文件
        if self.WINDOWS_FLAG:            
            os.chdir(r'./lib/win')
            self.Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
            self.Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        else:
            os.chdir(r'./lib')
            self.Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
            self.Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')
        # 设置组件库和SSL库加载路径                                                              # 2 设置组件库和SSL库加载路径
        self.SetSDKInitCfg()
        # 初始化DLL
        self.Objdll.NET_DVR_Init()                                                               # 3 相机初始化
        # 启用SDK写日志
        # self.Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)
        os.chdir(r'../../') # 切换工作路径到../../
        # 登录
        (self.lUserId, self.device_info) = self.LoginDev()                                       # 4 登录相机
        self.Playctrldll.PlayM4_ResetBuffer(self.lUserId,1)#清空指定缓冲区的剩余数据。这个地方传进来的是self.lUserId，为什么呢？
        print(self.lUserId)
        if self.lUserId < 0:#登录失败
            err = self.Objdll.NET_DVR_GetLastError()
            print('Login device fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()
        else:
            print(f'摄像头[{camIP}]登录成功!!')
        self.start_play()                                                                         # 5 开始播放


        time.sleep(1)
 
    def start_play(self,):
        #global funcRealDataCallBack_V30                                                                        
        self.PlayCtrl_Port = c_long(-1)  # 播放句柄
        # 获取一个播放句柄 #wuzh获取未使用的通道号
        if not self.Playctrldll.PlayM4_GetPort(byref(self.PlayCtrl_Port)):
            print(u'获取播放库句柄失败')
        # 定义码流回调函数       
        self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.RealDataCallBack_V30)
        # 开启预览
        self.preview_info = NET_DVR_PREVIEWINFO()
        self.preview_info.hPlayWnd = 0
        self.preview_info.lChannel = 1  # 通道号
        self.preview_info.dwStreamType = 0  # 主码流
        self.preview_info.dwLinkMode = 0  # TCP
        self.preview_info.bBlocked = 1  # 阻塞取流
        # 开始预览并且设置回调函数回调获取实时流数据
        self.lRealPlayHandle = self.Objdll.NET_DVR_RealPlay_V40(self.lUserId, byref(self.preview_info), self.funcRealDataCallBack_V30, None)
        if self.lRealPlayHandle < 0:
            print ('Open preview fail, error code is: %d' %self. Objdll.NET_DVR_GetLastError())
            # 登出设备
            self.Objdll.NET_DVR_Logout(self.lUserId)
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()
        # lRealPlayHandle = self.OpenPreview(Objdll, lUserId, None)
        
    def SetSDKInitCfg(self,):
        # 设置SDK初始化依赖库路径
        # 设置HCNetSDKCom组件库和SSL库加载路径
        # print(os.getcwd())
        if self.WINDOWS_FLAG:
            strPath = os.getcwd().encode('gbk')
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\libssl-1_1-x64.dll'))
        else:
            strPath = os.getcwd().encode('utf-8')
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))
    def LoginDev(self,):
        # 登录注册设备
        device_info = NET_DVR_DEVICEINFO_V30()
        lUserId = self.Objdll.NET_DVR_Login_V30(self.DEV_IP, self.DEV_PORT, self.DEV_USER_NAME, self.DEV_PASSWORD, byref(device_info))
        return (lUserId, device_info)
    def read(self,):
        # while self.n_stamp==self.last_stamp:
        #     continue
        self.last_stamp=self.n_stamp
        return self.recent_img
 
    def DecCBFun(self,nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
            if pFrameInfo.contents.nType == 3:
                # t0 = time.time()
                # 解码返回视频YUV数据，将YUV数据转成jpg图片保存到本地
                # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
                nWidth = pFrameInfo.contents.nWidth
                nHeight = pFrameInfo.contents.nHeight
                #nType = pFrameInfo.contents.nType
                # dwFrameNum = pFrameInfo.contents.dwFrameNum
                # nStamp = pFrameInfo.contents.nStamp
                #print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)
                # if self.n == 0:

                    # self.n=1
                YUV = np.frombuffer(pBuf[:nSize],dtype=np.uint8)
                YUV = np.reshape(YUV,[nHeight+nHeight//2,nWidth])
                img_rgb = cv2.cvtColor(YUV,cv2.COLOR_YUV2BGR_YV12)
                print("1",end="\n")
                # img_rgb=cv2.resize(img_rgb,(500,500))
                # cv2.imshow('img',img_rgb)
                # cv2.waitKey(1)
                # self.recent_img,self.n_stamp = img_rgb,nStamp
 
    def RealDataCallBack_V30(self,lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        # 码流回调函数
        # print(lPlayHandle,dwDataType,pBuffer.contents.value,dwBufSize,pUser)
        # for i in range(0,dwBufSize):
        #     print(pBuffer.contents.value)
        # num = 42  
  
# 创建一个指向该整数的指针  
        # num_ptr = ctypes.pointer(ctypes.c_int(num))
        # print(num_ptr)
        if dwDataType == NET_DVR_SYSHEAD:
            print("NET_DVR_SYSHEAD")
            # # 设置流播放模式
            # self.Playctrldll.PlayM4_SetStreamOpenMode(self.PlayCtrl_Port, 0)
            # # 打开码流，送入40字节系统头数据
            # if self.Playctrldll.PlayM4_OpenStream(self.PlayCtrl_Port, pBuffer, dwBufSize, 1024*100000):
            #     # 设置解码回调，可以返回解码后YUV视频数据
            #     #global FuncDecCB
            #     self.FuncDecCB = DECCBFUNWIN(self.DecCBFun)
            #     self.Playctrldll.PlayM4_SetDecCallBackExMend(self.PlayCtrl_Port, self.FuncDecCB, None, 0, None)
            #     # 开始解码播放
            #     if self.Playctrldll.PlayM4_Play(self.PlayCtrl_Port, None):
            #         print(u'播放库播放成功')
            #     else:
            #         print(u'播放库播放失败')
            # else:
            #     print(u'播放库打开流失败')
        elif dwDataType == NET_DVR_STREAMDATA:
            print(pBuffer,dwBufSize)
            class c_ubyte(ctypes.Structure):
                _fields_ = [("value", ctypes.c_ubyte)]

            # 使用ctypes的from_address方法获取LP_c_ubyte对象
            lp_c_ubyte_object = ctypes.cast(id(pBuffer), ctypes.POINTER(c_ubyte))

            # 通过指针访问LP_c_ubyte对象
            for i in range(dwBufSize):
                byte_value = lp_c_ubyte_object[i].value
                print(byte_value,end=" ")
            exit()
            # YUV = np.frombuffer(pBuffer[:dwBufSize],dtype=np.uint8)
            # print(YUV)

            # for i in range(0,dwBufSize):
            #     print(pBuffer.contents.value)
            print("NET_DVR_STREAMDATA")
            # self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, pBuffer, dwBufSize)
        else:
            print (u'其他数据,长度:', dwBufSize)
    # def find_pic(self):
    #     # if self.n == 1:
    #     import cv2
    #         # self.n=2
    #     cv2.imshow('img',self.recent_img)
    #     cv2.waitKey(1)
        # print(self.Objdll.NET_DVR_SetCapturePictureMode(1))
        # dwPicSize = 1440*2560*30

        # jpeg_pic_buffer = create_string_buffer(dwPicSize)
        # lpSizeReturned = ctypes.c_ulong()
        # lRealPlay = self.Objdll.NET_DVR_CapturePictureBlock_New(self.lRealPlayHandle,jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
        # image_array = np.frombuffer(jpeg_pic_buffer, dtype=np.uint8)
        # print('image_array:',jpeg_pic_buffer.raw)
        # # 解码为图像
        # image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

        # # 显示图像
        # cv2.imshow('Image', image)
        # cv2.waitKey(0)

        # lRealPlayH = Objdll.NET_DVR_CaptureJPEGPicture_NEW(lUserId,1,ctypes.pointer(pic_s),jpeg_pic_buffer,dwPicSize,byref(lpSizeReturned))
        # print('---------------------2-----: %d' % self.Objdll.NET_DVR_GetLastError(),lRealPlay)    
    def release(self):
        self.Objdll.NET_DVR_StopRealPlay(self.lRealPlayHandle)
        if self.PlayCtrl_Port.value > -1:
            self.Playctrldll.PlayM4_Stop(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_CloseStream( self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_FreePort( self.PlayCtrl_Port)
            PlayCtrl_Port = c_long(-1)
            self.Objdll.NET_DVR_Logout(self.lUserId)
            self.Objdll.NET_DVR_Cleanup()
        print('释放资源结束')
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
 
if __name__=="__main__":
    camIP ='192.168.44.64'
    #camIP ='192.168.3.157'
    DEV_PORT = 8011
    username ='admin'
    password = 'air12345678'
    HIK= HKCam(camIP,username,password)
    last_stamp = 0
    import cv2
    import numpy as np
                # import cv2
    
    while True:
        
        print(2222)
        time.sleep(1)
        # t0 =time.time()
        # img = HIK.read()

        # time.sleep(2)
        # last_stamp=n_stamp
        # HIK.find_pic()
        # try:
        #     cv2.imshow('Image', img)
        # except:
        #     pass
        # cv2.waitKey(1)
        '''
        TODO
        '''
        # kkk = cv2.waitKey(1)
        # if kkk ==ord('q'):
        #     break
    HIK.release()