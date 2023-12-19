import rclpy

from rclpy.node import Node
# from protocol.msg import WifiStatus
# from protocol.srv import WifiConnect
from protocol.srv import CameraService
# from std_msgs.msg import Bools
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"

class camera_picture_node(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("Hello ROS 2")   

        self.sub_wifi_status = self.create_subscription(WifiStatus,mi_node + "wifi_status",self.wifi_status_callback,10)
        self.cli_wifi_connect = self.create_client(WifiConnect,mi_node + "connect_wifi")



    # def wifi_status_callback(self,wifi_status):
    #     self.get_logger().info("wifi_status_callback")
    #     self.get_logger().info("\nis_connected=%d\n\
    #                            ip=%s\n\
    #                            ssid=%s\n\
    #                            strength=%d\n\
    #                            "%(wifi_status.is_connected,\
    #                               wifi_status.ip,\
    #                                 wifi_status.ssid,\
    #                                     wifi_status.strength) )
        # rclpy.shutdown()


    # def send_request(self):
    #     self.get_logger().info("send_request")
    #     while not self.cli_wifi_connect.wait_for_service(timeout_sec=1.0):
    #         self.get_logger().warn('service not available, waiting again...')
    #     request = WifiConnect.Request()
    #     request.ssid = "dog"
    #     request.pwd = "12345678"

    #     # request.ssid = "404_m6200"
    #     # request.pwd = "404404404"
    #     future = self.cli_wifi_connect.call_async(request)
    #     future.add_done_callback(self.connect_is_ok_callback)
    
    # def connect_is_ok_callback(self,response):
    #     self.num_info(response.result().result)
        # self.get_logger().info("connect_is_ok = %d"%response.result().result)

def main(args=None):
    rclpy.init(args=args)
    node = camera_picture_node("picture_node")
    # node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
