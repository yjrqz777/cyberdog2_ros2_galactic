import rclpy
from rclpy.node import Node
#include "protocol/srv/audio_execute.hpp"
#include "protocol/srv/audio_text_play.hpp"
#include "protocol/msg/audio_play_extend.hpp"
#include "std_srvs/srv/trigger.hpp"
#include "std_msgs/msg/u_int8.hpp"
from protocol.srv import AudioExecute
from protocol.srv import AudioTextPlay
from protocol.msg import AudioPlayExtend
from protocol.srv import AudioVolumeSet
from std_srvs.srv import Trigger
from std_msgs.msg import UInt8
from std_msgs.msg import Bool

import os
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"

"""
ros2 pkg create my_weakup --build-type ament_python --dependencies rclcpp
colcon build --merge-install --packages-select my_weakup

ros2 run my_weakup my_wakeup_node
ros2 run my_weakup my_wakeup_node
"""


class my_wakeup(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_audio_stat = self.create_client(AudioExecute,mi_node + "get_audio_state")   
        self.pub_audio_send = self.create_publisher(AudioPlayExtend, mi_node + "speech_play_extend", 10)

        self.sub = self.create_subscription(Bool, mi_node+'dog_wakeup', self.wakeup_callback, 10)


    def wakeup_callback(self, msg):
        #语音唤醒了msg.Data
        self.get_logger().info('cyberdog wakeup')
        self.topic_talk("开始执行任务")
        os.system('sh /home/mi/run.sh')
        self.topic_talk("执行完成")

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
        self.get_logger().info("topic_talk-------")



def main(args=None):
    rclpy.init(args=args)

    my_wakeup_node = my_wakeup("my_wakeup_node")
    my_wakeup_node.get_logger().info("Hello World!")
    rclpy.spin(my_wakeup_node)
    # audio_node.topic_talk("然后直接进行回调。")
    # audio_node.topic_talk("一系列订阅、回调、。")
    # audio_node.get_logger().info("2222-------")
    my_wakeup_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()