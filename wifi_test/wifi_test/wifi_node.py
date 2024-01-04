import rclpy
import argparse
from rclpy.node import Node
from protocol.msg import WifiStatus
from protocol.srv import WifiConnect
from protocol.srv import Connector
# from std_msgs.msg import Bools
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"
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



class WifiNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("Hello ROS 2")   

        self.sub_wifi_status = self.create_subscription(WifiStatus,mi_node + "wifi_status",self.wifi_status_callback,10)
        # self.cli_wifi_connect = self.create_client(WifiConnect,mi_node + "connect_wifi")
        self.app_wifi_connect = self.create_client(Connector,mi_node + "connect")

    def wifi_status_callback(self,wifi_status):
        self.get_logger().info("wifi_status_callback")
        self.get_logger().info("\nis_connected=%d\n\
                               ip=%s\n\
                               ssid=%s\n\
                               strength=%d\n\
                               "%(wifi_status.is_connected,\
                                  wifi_status.ip,\
                                    wifi_status.ssid,\
                                        wifi_status.strength) )
        # rclpy.shutdown()
    def send_app_request(self):
        self.get_logger().info("send_request")
        while not self.app_wifi_connect.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn('service not available, waiting again...')
        request = Connector.Request()
        if n==1:
            request.wifi_name = "dog"
            request.wifi_password = "12345678"
        if n==2:
            request.wifi_name = "404_m6200"
            request.wifi_password = "404404404"
        request.provider_ip = ip
        future = self.app_wifi_connect.call_async(request)
        future.add_done_callback(self.connect_app_callback)

    def connect_app_callback(self,response):
        self.get_logger().info("connect_is_ok = %d"%response.result().connected)
        self.num_info(response.result().code)
        # self.get_logger().info("connect_is_ok = %d"%response.result().result)

    # def send_request(self):
    #     self.get_logger().info("send_request")
    #     while not self.cli_wifi_connect.wait_for_service(timeout_sec=1.0):
    #         self.get_logger().warn('service not available, waiting again...')
    #     request = WifiConnect.Request()
    #     if n==1:
    #         request.ssid = "dog"
    #         request.pwd = "12345678"
    #     if n==2:
    #         request.ssid = "404_m6200"
    #         request.pwd = "404404404"
    #     future = self.cli_wifi_connect.call_async(request)
    #     future.add_done_callback(self.connect_is_ok_callback)
    
    # def connect_is_ok_callback(self,response):
    #     self.num_info(response.result().result)
    #     # self.get_logger().info("connect_is_ok = %d"%response.result().result)

    def num_info(self, num):
        if num == 4:
            self.get_logger().warn("RESULT_NO_SSID-没找到请求的wifi\n")
        elif num == 5:
            self.get_logger().warn("RESULT_ERR_PWD-密码错误\n")
        elif num == 6:
            self.get_logger().warn("RESULT_OTHER-其它情况\n")
        elif num == 7 or num == 0:
            self.get_logger().warn("RESULT_SUCCESS-连接成功\n")
        elif num == 14:
            self.get_logger().warn("RESULT_INTERRUPT-过程被中断\n")
        elif num == 15 or num == 8124:
            self.get_logger().warn("RESULT_TIMEOUT-连接超时\n")
        elif num == 8121:
            self.get_logger().warn("CODE_WIFI_NAME_FAIL-连接失败\n")
        elif num == 8122:
            self.get_logger().warn("CODE_WIFI_PASSWORD_FAIL-连接失败\n")
        elif num == 8123:
            self.get_logger().warn("CODE_WIFI_PROVIDER_IP_FAIL-连接失败\n")



def main(args=None):
    global n, ip
    parser = argparse.ArgumentParser(description='两个参数，1是wifi编号，2是app的ip地址')
    #type是要传入的参数的数据类型  help是该参数的提示信息
    parser.add_argument('--i', dest='int', metavar='1 or 2',type=int, help='wifi编号')
    parser.add_argument('--ip', dest='ip',metavar='192.168.1.1',type=str, help='app的ip地址')
    argss = parser.parse_args()
    n=argss.int
    ip=argss.ip
    print(n,ip)
    rclpy.init(args=args)
    node = WifiNode("wifi_node")
    node.send_app_request()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()