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
        if feedback_code == 6:
            print("启动成功")
        elif feedback_code == 7:
            print("启动失败")
        elif feedback_code == 8:
            print("重定位成功")
        elif feedback_code == 9:
            print("重定位失败")
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

    def read_post(self):
        json_str = self.encodeVel()
        self.grpc_client.sendMsg(6009, json_str)
        print(json_str)
        time.sleep(1)


    def encodeVel(self):
        cmd = {}

        cmd["type"] = 5
        cmd["outdoor"] = False
        cmd["map_name"] = "rue"

        return json.dumps(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Please input gRPC server IP, CA certificate, client key and client certificate')
        exit()
    grpc_client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    send = ProtoEncoder()
    send.read_post()


