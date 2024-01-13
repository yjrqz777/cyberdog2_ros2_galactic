import os
import select
import sys
import time
if os.name == 'nt':
    import msvcrt
    print('os.name is nt')
else:
    import termios
    import tty 
    print('os.name is', os.name)

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
            result_list = self.__stub.sendMsg(
                cyberdog_app_pb2.SendRequest(
                    nameCode=name_code,
                    params=params))
            try:
                for response in result_list:
                    try:
                        parsed_data = json.loads(response.data)
                    except:
                        parsed_data = parsed_data
                    print("1:{}".format(parsed_data) )
            except:
                resp = list(result_list)
                print("2:{} ".format(resp) )
        except:
            print('failed to send msg')



class ProtoEncoder:
    def encodeVel(self, vel):
        cmd = {}
        cmd['motion_id'] = 303
        cmd['cmd_type'] = 1
        cmd['cmd_source'] = 3
        cmd['value'] = 0
        cmd['step_height'] = [0.06, 0.06]
        cmd['vel_des'] = vel
        return json.dumps(cmd)

    '''
    int32 motion_id;
    int32 cmd_source;    # 指令来源，app填0
    float32 vel_des[3];  # x方向， y方向， 旋转, "vel_des": [x, y, z]
    float32 pos_des[3];  # [1]值有效, "pos_des": [0, value, 0]
    float32 rpy_des[3];  # [2]值有效, "rpy_des": [0, 0, value]
    float32 step_height[3];  # 抬腿高度，，最大值运控组不确定，当前可按0.06m设定

    int32 contact;          contact：低四位用于位控姿态模式(mode/gait_id:21/0 )下定义哪条腿抬起，默认值0x0F，\
        表示四条腿都不抬起。如需抬起一条腿，比如：0b1110抬右前腿，0b1101左前腿，0b1011右后腿，0b0111抬左后腿

    int32 duration       # 执行时间
    int32 value         #bit1: 0表示内八节能步态   1表示垂直步态

        msg.mode = 21 # Position interpolation control
        msg.gait_id = 0
        msg.rpy_des = [0, 0.3, 0] # Head up
        msg.duration = 500 # Expected execution time, 0.5s 
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        time.sleep( 0.5 )

    '''

    def stopSignal(self):
        cmd = {}
        cmd['mode'] = 212
        cmd['cmd_source'] = 3
        cmd['value'] = 0
        cmd['gait_id'] = 0


        # cmd["vel_des"] = [0,0,0.1]
        cmd['duration'] = 500     
        # # cmd["contact"] = 0b1110
        cmd["rpy_des"] = [0, 0.26, 0]
        # cmd['pos_des'] = [0.16, 0.23, 0.23]
        # cmd['step_height'] = [0.01, 0.01, 0.01]

        return json.dumps(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Please input gRPC server IP, CA certificate, client key and client certificate')
        exit()
    grpc_client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    encoder = ProtoEncoder()
    stop_signal = False
    json_str = encoder.stopSignal()
    # json_str = encoder.encodeVel(vel)
    print(json_str)
    grpc_client.sendMsg(1004, json_str)
    time.sleep( 0.5 )

