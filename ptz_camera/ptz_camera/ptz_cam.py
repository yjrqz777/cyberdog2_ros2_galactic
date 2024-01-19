import rclpy as a
import argparse
import rclpy.node as s

from HCNetSDK import *
from PlayCtrl import *
# mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"
# # protocol/srv/Connector
import sys, os
# sys.path.append("/SDCARD/workspace/cyberdog2_ros2_galactic/hk")
# from Ptz_Camera_Lib import Ptz_Camera
# 

# '''
# uint8 cmd
# uint8 time
# bool is_pic
# string pic_name
# '''

# Node = rclpy.node.Node

# class Ptz_Cam_Node(Node):
#     def __init__(self,name):
#         super().__init__(name)
#         self.get_logger().info("Hello ROS ")   
#         self.ptz_service = self.create_service(PtzCam, "ptz_service", self.cmd_callback)
#         # self.ptz_con = Ptz_Camera()

#     def cmd_callback(self, request, response):                                           # 创建回调函数，执行收到请求后对数据的处理
#         cmd = request.cmd
#         time = request.time
#         is_pic = request.is_pic
#         pic_name = request.pic_name
#         self.ptz_con.take_control(cmd, time)
#         if is_pic:
#             response = self.ptz_con.take_pic(p_name = pic_name)
        
#         return response    


# def main(args=None):
#     rclpy.init(args=args)
#     node = Ptz_Cam_Node("Ptz_Cam_Node")
#     rclpy.spin(node)
#     rclpy.shutdown()




if __name__ == "__main__":

    # main()
    DEV_IP = create_string_buffer(b'192.168.44.64')
    DEV_PORT = 443
    DEV_USER_NAME = create_string_buffer(b'admin')
    DEV_PASSWORD = create_string_buffer(b'air12345678')
    strPath = os.getcwd().encode('utf-8')
    print(strPath)
    os.chdir(r'/SDCARD/workspace/cyberdog2_ros2_galactic/ptz_camera/ptz_camera/lib')
    Objdll = cdll.LoadLibrary('./libhcnetsdk.so')
    strPath = os.getcwd().encode('utf-8')
    print(strPath)
    # os.chdir(r'./lib')
    strPath = os.getcwd().encode('utf-8')
    print(strPath)
    sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
    sdk_ComPath.sPath = strPath
    Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
    Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
    Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))
    # 初始化DLL
    syr = Objdll.NET_DVR_Init()
    print(syr)
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
    print(lUserId)
    if lUserId < 0:
        err = Objdll.NET_DVR_GetLastError()
        print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        # 释放资源
        Objdll.NET_DVR_Cleanup()
        exit()