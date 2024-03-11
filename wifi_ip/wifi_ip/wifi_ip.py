import rclpy
import argparse
from rclpy.node import Node
from protocol.msg import WifiStatus
from protocol.srv import WifiConnect
from protocol.srv import Connector
from rclpy.executors import MultiThreadedExecutor
from protocol.srv import AudioVolumeSet

from protocol.msg import AudioPlayExtend
from protocol.srv import AudioExecute
# from std_msgs.msg import Bools

# protocol/srv/Connector

"""
ros2 service type  /mi_desktop_48_b0_2d_7b_02_9c/connect_wifi
protocol/srv/WifiConnect
ros2 interface show protocol/srv/WifiConnect
# 该服务用于请求wifi连接服务及表征连接响应信息的接口约束
string ssid                  # wifi名称
string pwd                   # 密码
---
uint8 result                 # 返回结果，取值范围受下述 RESULT_* 值约束，反之无效
# ---------------------------
uint8 RESULT_NO_SSID = 4     # 没找到请求的wifi
uint8 RESULT_ERR_PWD = 5     # 密码错误
uint8 RESULT_OTHER = 6       # 其它情况
uint8 RESULT_SUCCESS = 7     # 连接成功
uint8 RESULT_INTERRUPT = 14  # 过程被中断
uint8 RESULT_TIMEOUT = 15    # 连接超时
int32 code
###






/wifi_test$ colcon build 
colcon build --merge-install --packages-select wifi_test
ros2 run wifi_test wifi_node


/mi_desktop_48_b0_2d_7b_02_9c/connect

protocol/srv/Connector

string wifi_name
string wifi_password
string provider_ip
---
int32 CODE_SUCCESS = 0
int32 CODE_WIFI_NAME_FAIL = 8121
int32 CODE_WIFI_PASSWORD_FAIL = 8122
int32 CODE_WIFI_PROVIDER_IP_FAIL = 8123
int32 CODE_CONNECTION_TIMEOUT_FAIL = 8124

bool connected
int32 code


"""


mi_node = ""


class WifiNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.cout = 0
        self.sub_wifi_status = self.create_subscription(WifiStatus,mi_node+"wifi_status",self.wifi_status_callback,10)


        self.get_audio_stat = self.create_client(AudioExecute,mi_node+ "get_audio_state")   
        self.pub_audio_send = self.create_publisher(AudioPlayExtend,mi_node+"speech_play_extend", 10)

        self.set_volume_client = self.create_client(AudioVolumeSet,mi_node+"audio_volume_set")
        self.set_volume(40)


    def topic_talk(self,string):
        # self.get_logger().warn('service waiting')
        while not self.get_audio_stat.wait_for_service(1):
            self.get_logger().warn('service not available, waiting again...')
        msg_send = AudioPlayExtend()
        msg_send.is_online = True
        msg_send.module_name = "AudioT"
        msg_send._speech.module_name = "AudioT"
        msg_send._speech.play_id = 32
        msg_send.text = string
        self.pub_audio_send.publish(msg_send)
        self.get_logger().warn('publish---')





    def wifi_status_callback(self,wifi_status):
        # self.get_logger().info("wifi_status_callback")
        # if wifi_status.is_connected ==1:
        #     self.cout = self.cout
        if wifi_status.is_connected ==0:
            self.cout=0         
        if wifi_status.is_connected ==1:
            if self.cout != 16:
                self.cout = self.cout + 1
            if self.cout == 15:
                self.topic_talk(wifi_status.ip)
            # self.destroy_node()
        self.get_logger().info("\nis_connected=%d,self.cout=%d\n\
                            ip=%s\n\
                            ssid=%s\n\
                            strength=%d\n\
                            "%(wifi_status.is_connected,self.cout,\
                                wifi_status.ip,\
                                    wifi_status.ssid,\
                                        wifi_status.strength) )
        # self.destroy_node()




def main(args=None):

    rclpy.init(args=args)
    node = WifiNode("wifi_ip_node")
    # executor = MultiThreadedExecutor()
    # executor.add_node(node)
    # executor.spin()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()