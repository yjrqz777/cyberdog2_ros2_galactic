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
from std_srvs.srv import Trigger
from std_msgs.msg import UInt8

mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"

"""
/audio_test$ colcon build
ros2 run audio_test audio_node
"""


class AudioT(Node):
    def __init__(self,name):
        super().__init__(name)
        self.time_per = 1
        self.count = 0
        self.get_audio_stat = self.create_client(AudioExecute,"get_audio_state")   
        self.get_logger().warn("self.get_audio_stat==%s"%self.get_audio_stat)
        # rclpy.shutdown()
        self.pub_volume_get = self.create_publisher(UInt8, mi_node + "volume_set", 10)
        self.pub_audio_send = self.create_publisher(AudioPlayExtend, mi_node + "speech_play_extend", 10)
        
"""

module_name: AudioTalkDemo
is_online: true
speech:
  module_name: AudioTalkDemo
  play_id: 32
text: 这是在线语音32,this is online voice.
---
module_name: AudioTalkDemo
is_online: true
speech:
  module_name: AudioTalkDemo
  play_id: 32
text: 你好
---

"""



# '''
# string module_name
# bool is_online
# AudioPlay speech
#         string module_name
#         uint16 play_id
# string text
#         speech_play_extend_voice->module_name = name_;
#         speech_play_extend_voice->is_online = online;
#         speech_play_extend_voice->speech.module_name = name_;
#         speech_play_extend_voice->speech.play_id = 32;  // please close to me.
#         speech_play_extend_voice->text = strs;

# '''
        msg_volume = UInt8()
        msg_volume.data = 20
        self.pub_volume_get.publish(msg_volume)


        msg_send = AudioPlayExtend()
        msg_send.is_online = True
        msg_send.module_name = "AudioTalkDemo"
        msg_send._speech.module_name = "AudioTalkDemo"
        msg_send._speech.play_id = 32
        msg_send.text = "你好"
        if self.get_audio_stat == None:
            self.get_logger().error("self.get_audio_stat--is-no-ok")

        self.pub_audio_send.publish(msg_send)
        self.get_logger().info("111111-------")
        self.timer = self.create_timer(self.time_per, self.timer_callback)



    def timer_callback(self):
        self.count += 1
        self.get_logger().info("Publishing: '%d'" % self.count)




def main(args=None):
    rclpy.init(args=args)

    audio_node = AudioT("audio_t")
    # audio_node.get_logger().info("Hello World!")
    rclpy.spin(audio_node)
    # audio_node.destroy_node()
    rclpy.shutdown()


