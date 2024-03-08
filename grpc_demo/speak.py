import rclpy
from rclpy.node import Node
from protocol.srv import AudioExecute
from protocol.msg import AudioPlayExtend

mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"


class AudioT(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_audio_stat = self.create_client(AudioExecute,mi_node + "get_audio_state")   
        self.get_logger().warn("self.get_audio_stat==%s"%self.get_audio_stat)
        self.pub_audio_send = self.create_publisher(AudioPlayExtend, mi_node + "speech_play_extend", 10)

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



class speaks():
    def __init__(self) -> None:
        rclpy.init()
        self.audio_node = AudioT("audio_t")

    def speak_something(self,string):
        self.audio_node.topic_talk(string)
    def destroy(self):
        self.audio_node.destroy_node()
        # rclpy.shutdown()

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