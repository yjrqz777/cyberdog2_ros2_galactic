import rclpy

from rclpy.node import Node
# from protocol.msg import WifiStatus
# from protocol.srv import WifiConnect
from sensor_msgs.msg import Image
from protocol.srv import CameraService
# from std_msgs.msg import Bools
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"
import cv2
import os
import numpy as np
# sensor_msgs/msg/Image
'''
uint8 SET_PARAMETERS = 0
uint8 TAKE_PICTURE = 1
uint8 START_RECORDING = 2
uint8 STOP_RECORDING = 3
uint8 GET_STATE = 4
uint8 DELETE_FILE = 5
uint8 GET_ALL_FILES = 6
uint8 START_LIVE_STREAM = 7
uint8 STOP_LIVE_STREAM = 8
uint8 START_IMAGE_PUBLISH = 9
uint8 STOP_IMAGE_PUBLISH = 10

uint8 command
# command arguments
string args
uint16 width
uint16 height
uint16 fps
---
uint8 RESULT_SUCCESS = 0
uint8 RESULT_INVALID_ARGS = 1
uint8 RESULT_UNSUPPORTED = 2
uint8 RESULT_TIMEOUT = 3
uint8 RESULT_BUSY = 4
uint8 RESULT_INVALID_STATE = 5
uint8 RESULT_INNER_ERROR = 6
uint8 RESULT_UNDEFINED_ERROR = 255

uint8 result
string msg
int32 code



'''


'''
mi@mi-desktop:~$ ros2 interface show sensor_msgs/msg/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image

std_msgs/Header header # Header timestamp should be acquisition time of image
        builtin_interfaces/Time stamp
                int32 sec
                uint32 nanosec
        string frame_id
                             # Header frame_id should be optical frame of camera
                             # origin of frame should be optical center of cameara
                             # +x should point to the right in the image
                             # +y should point down in the image
                             # +z should point into to plane of the image
                             # If the frame_id here and the frame_id of the CameraInfo
                             # message associated with the image conflict
                             # the behavior is undefined

uint32 height                # image height, that is, number of rows
uint32 width                 # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.ros.org and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.hpp

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)


colcon build --merge-install --packages-select camera_picture

ros2 run camera_picture camera_picture_node

ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/camera_service protocol/srv/CameraService "{command: 1, args: ''}"


ros2 run camera_test camera_server __ns:=/mi_desktop_48_b0_2d_7b_02_9c

ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/camera_service protocol/srv/CameraService "{command: 1, args: ''}"

ros2 run camera_test stereo_camera __ns:=/mi_desktop_48_b0_2d_7b_02_9c


ros2 launch camera_test stereo_camera.py 
#查看name space

ros2 node list 

###如果是开机自启，注意topic前加上命名空间

ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/stereo_camera configure 

ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/stereo_camera activate

ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/stereo_camera deactivate

ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/stereo_camera cleanup

'''

class camera_picture_node(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("Hello ROS 2")   
      # self.sub_wifi_status = self.create_subscription(WifiStatus,mi_node + "wifi_status",self.wifi_status_callback,10)
        self.picture_date = self.create_subscription(Image,mi_node + "image_rgb",self.picture_date_callback,10)
        self.camera_state = self.create_client(CameraService,mi_node + "camera_service")



    def picture_date_callback(self,images_date):
        self.get_logger().info("picture_date_callback")
        print(len(images_date.data))
        print(images_date.width,images_date.height,images_date.encoding,images_date.is_bigendian,images_date.step)
        # cv2.imshow('Array Image', images_date.data)
        # cv2.waitKey(0)  # 等待按下任意键关闭图像窗口
        # self.get_logger().warn(images_date.data)
        # with open("picture.txt","w") as f:
        #     array_string = ' '.join(map(str, images_date.data))
        #     print(array_string)
        #     f.write(array_string)
        # f.close()
        numpy_image = np.array(images_date.data)
        print(type(numpy_image))
        width = images_date.width
        height = images_date.height
        two_dimensional_array = numpy_image.reshape(height, width,3)
        cv2.imshow('Array Image', two_dimensional_array)
        cv2.waitKey(1)  # 等待按下任意键关闭图像窗口
        # cv2.imwrite("file_name.png", two_dimensional_array)
        # self.get_logger().info("\nis_connected=%d\n\
        #                        ip=%s\n\
        #                        ssid=%s\n\
        #                        strength=%d\n\
        #                        "%(wifi_status.is_connected,\
        #                           wifi_status.ip,\
        #                             wifi_status.ssid,\
        #                                 wifi_status.strength) )
        # rclpy.shutdown()


    def state_send_request(self):
        self.get_logger().info("send_request")
        while not self.camera_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service not available, waiting again...')
        request = CameraService.Request()
        request.command = 10
        request.args = ''
        request.width = 640
        request.height = 480
        request.fps = 0

        future = self.camera_state.call_async(request)
        future.add_done_callback(self.camera_callback)
        self.get_logger().info("send_request2")
    
    def camera_callback(self,response):
        '''
        uint8 result
        string msg
        int32 code
        '''
        # self.num_info(response.result())
        # self.get_logger().info("send_request")
        self.get_logger().info("result = %d, msg=%s, code=%d" %(response.result().result, response.result().msg, response.result().code ))
        # rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = camera_picture_node("picture_node")
    # node.state_send_request()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()