import os
import select
import sys

if os.name == 'nt':
    import msvcrt
    print('os.name is nt')
else:
    import termios
    import tty 
    print('os.name is', os.name)

import time
import grpc
import json
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc
sys.path.append("/SDCARD/workspace/cyberdog2_ros2_galactic/hk")
from Ptz_Camera_Lib import Ptz_Camera
# from HCNetSDK import *

class Client:
    def __init__(self, cyberdog_ip: str, ca_cert: str, client_key: str, client_cert: str):
        creds = grpc.ssl_channel_credentials(
            open(ca_cert, 'rb').read(),
            open(client_key, 'rb').read(),
            open(client_cert, 'rb').read())
        channel_options = (('grpc.ssl_target_name_override', 'cyberdog2.server'), 
                           ('grpc.default_authority', 'cyberdog2.server'))
        chennel = grpc.secure_channel(cyberdog_ip + ':50052', creds, channel_options)
        self.__stub = cyberdog_app_pb2_grpc.GrpcAppStub(chennel)
        print('Client is ready.')

    def sendMsg(self, name_code, params):
        try:
            requset = cyberdog_app_pb2.SendRequest(nameCode=name_code,params=params)
            result_list = self.__stub.sendMsg(requset)
            for response in result_list:
                try: 
                    parsed_data = json.loads(response.data)
                    # print(parsed_data['feedback_code'])
                    self.analy_code(parsed_data['feedback_code'])
                except:
                    parsed_data = json.loads(response.data)
                    print(parsed_data)
                    # print(parsed_data['feedback_code'])
        except:
            print('failed to send msg')

    def analy_code(self,feedback_code):
        if feedback_code == 300:
            print("导航启动成功，设置目标点成功，正在规划路径")
        elif feedback_code == 307:
            print("正在导航中")
        elif feedback_code == 308:
            print("到达目标点")
        elif feedback_code == 302:
            print("底层导航功能服务连接失败，请重新发送目标")
        elif feedback_code == 303:
            print("发送目标点失败，请重新发送目标")
        elif feedback_code == 304:
            print("底层导航功能失败，请重新发送目标")
        elif feedback_code == 305:
            print("目标点为空，请重新选择目标")
        elif feedback_code == 306:
            print("规划路径失败，请重新选择目标")
        elif feedback_code == 309:
            print("正在检查地图")
        elif feedback_code == 310:
            print("地图检查成功")
        elif feedback_code == 311:
            print("地图不存在，请重新建图")
        elif feedback_code == 1000:
            print("正在激活依赖节点")
        elif feedback_code == 1001:
            print("激活依赖节点成功")
        elif feedback_code == 1002:
            print("激活依赖节点失败")
        else:
            print("feedback_code:{}".format(feedback_code))
        

class ProtoEncoder:
    def __init__(self):
        self.grpc_client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        # self.Ptz_cam = Ptz_Camera()

    def read_post(self):
        txt_files_os = [f for f in os.listdir("/home/mi/mapping") if f.endswith('.json')]
        print(txt_files_os)
        with open("/home/mi/mapping/" + txt_files_os[0], 'r') as file: 
            content = file.read()
            content= json.loads(content)
            label_num = len(content) - 2
            for i in range(1, 1 + 1):
                if i == 1:
                    
                    time.sleep(1)
                label_name = "".join("标签名称{}".format(i))
                x = content[label_name]["x"]
                y = content[label_name]["y"]
                json_str = self.encodeVel(x,y)
                label_name = ""
                self.grpc_client.sendMsg(6004, json_str)
                print(json_str)
                # self.Ptz_cam.take_control(TILT_DOWN,1)
                # self.Ptz_cam.take_control(ZOOM_OUT,1)
                # self.Ptz_cam.take_pic(p_size=8,p_name="{}".format(label_name))
                # Ptz_cam.LogoutDev()
                # if i == 1:
                #     Ptz_cam.LogoutDev()
                time.sleep(1)


    def encodeVel(self,x,y):
        cmd = {}
        # cmd['enable'] = True
        # cmd["is_version"] = True
        cmd["type"] = 1
        # cmd["outdoor"] = False
        # cmd["map_name"] = "rue"
        cmd["goalX"] = x
        cmd["goalY"] = y
        # cmd["theta"] = -180

        return json.dumps(cmd)

if __name__ == '__main__':
    # if len(sys.argv) < 5:
    #     print('Please input gRPC server IP, CA certificate, client key and client certificate')
    #     exit()
    # grpc_client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    Ptz_Camera()
    # send = ProtoEncoder()
    # send.read_post()


