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

mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"

"""
/audio_test$ colcon build
colcon build --merge-install --packages-select audio_test
ros2 run audio_test audio_node


ros2 interface show protocol/srv/AudioTextPlay
# request
string module_name
bool is_online
AudioPlay speech
        string module_name
        uint16 play_id
string text
---
# response
uint8 status    # 0播放完毕,1播放失败
int32 code

"""


class AudioT(Node):
    def __init__(self,name):
        super().__init__(name)
        self.time_per = 5
        self.count = 0
        self.get_audio_stat = self.create_client(AudioExecute,mi_node + "get_audio_state")   
        self.get_logger().warn("self.get_audio_stat==%s"%self.get_audio_stat)
        # self.pub_volume_get = self.create_publisher(UInt8, mi_node + "volume_set", 10)
        self.pub_audio_send = self.create_publisher(AudioPlayExtend, mi_node + "speech_play_extend", 10)
        # self.pub_volume_get.publish(msg_volume)
        self.set_volume_client = self.create_client(AudioVolumeSet,mi_node+"audio_volume_set")
        self.set_volume(10)
        # self.get_logger().info("111111-------")
        # self.speak_service = self.create_service(AudioTextPlay, mi_node + "speak_text_play", self.speak_callback)
        # self.timer = self.create_timer(self.time_per, self.timer_callback)
        # self.destroy_node()
    # def speak_callback(self,request,response):
    #     msg_send = AudioPlayExtend()
    #     msg_send.is_online = True
    #     msg_send.module_name = "AudioT"
    #     msg_send._speech.module_name = "AudioT"
    #     msg_send._speech.play_id = 32
    #     msg_send.text = request.text
    #     self.pub_audio_send.publish(msg_send)
    #     self.get_logger().info("topic_talk-------")


    def set_volume(self,val):
        while not self.set_volume_client.wait_for_service(timeout_sec=1.0):
          self.get_logger().warn('service not available, waiting again...')
        set_volume = AudioVolumeSet.Request()
        set_volume.volume = val
        self.set_volume_client.call_async(set_volume).add_done_callback(self.set_volume_callback)

    def set_volume_callback(self,response):
        self.get_logger().warn("是否成功=%d, code = %d"%(response.result().success,response.result().code))

    def timer_callback(self):
        self.count += 1
        self.topic_talk("你好")
        self.get_logger().info("111111-------")
        self.get_logger().info("Publishing: '%d'" % self.count)

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

    audio_node = AudioT("audio_t")
    # audio_node.get_logger().info("Hello World!")
    
    # rclpy.spin_once(audio_node)
    audio_node.topic_talk("然后直接进行回调。")
    audio_node.topic_talk("一系列订阅、回调、。")
    # audio_node.get_logger().info("2222-------")
    # audio_node.destroy_node()
    # rclpy.shutdown()


if __name__ == "__main__":
    main()