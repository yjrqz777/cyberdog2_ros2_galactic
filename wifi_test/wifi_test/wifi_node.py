import rclpy

from rclpy.node import Node
from protocol.msg import WifiStatus
from protocol.srv import WifiConnect
# from std_msgs.msg import Bools
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"

class WifiNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("Hello ROS 2")   

        self.sub_wifi_status = self.create_subscription(WifiStatus,mi_node + "wifi_status",self.wifi_status_callback,10)
        self.cli_wifi_connect = self.create_client(WifiConnect,mi_node + "wifi_connect")


    def wifi_status_callback(self,wifi_status):
        self.get_logger().info("wifi_status_callback")
        self.get_logger().info("\nis_connected=%d\nip=%s\nssid=%s\nstrength=%d\n"%(wifi_status.is_connected,wifi_status.ip,wifi_status.ssid,wifi_status.strength) )
        rclpy.shutdown()




def main(args=None):
    rclpy.init(args=args)
    node = WifiNode("wifi_node")
    rclpy.spin(node)
    rclpy.shutdown()
