#配置用户名
git config --global user.name "yjrqz777"

#配置邮箱
git config --global user.email  3210551161@qq.com


ros2 pkg create audio_test --build-type ament_python --dependencies rclcpp

ros2 pkg create wifi_test --build-type ament_python --dependencies rclcpp


ros2 pkg create my_interface --build-type ament_cmake


colcon build --merge-install --packages-select moto_contor_test

colcon build --merge-install --packages-select nav2_control_demo



ros2 run moto_contor_test talks_node --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"`

ros2 run moto_contor_test talks_node --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c

ros2 run motion_action2 client_test --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c


ros2 run talk_something talks_node --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c

                                                         /mi_desktop_48_b0_2d_7b_02_9c/motion_sequence_cmd

ros2 run moto_contor_test set_voice --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c
ros2 run audio_demos set_voice --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"`


ros2 run motion_action client_test " {motion_id: 1}" --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c

ros2 service list | grep set_elec_skin
ros2 service type /mi_desktop_48_b0_2d_7b_02_9c/set_elec_skin
ros2 interface show std_srvs/srv/SetBool

ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/enable_elec_skin std_srvs/srv/SetBool '{data: 1}'
ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/set_elec_skin protocol/srv/ElecSkin '{mode: 4,wave_cycle_time: 2}'


# request
int32 mode # 0-全黑 1-全白 2-前向后渐变 3-后向前渐变 4-闪烁 5-随机 6-动态（随落地腿变色）
int32 wave_cycle_time # 2-5静态效果模式下表示变色时间，6动态模式下0值表示落地腿变白，非零表示变深色
---
# response
bool success

ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/camera_service protocol/srv/CameraService "{command: 9, args: ''}"
ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/camera_service protocol/srv/CameraService "{command: 9, width: 640, height: 480, fps: 0}"
ros2 topic list|grep speech_play_extend
/mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend


ros2 topic echo /mi_desktop_48_b0_2d_7b_02_9c/volume_get
ros2 topic info /mi_desktop_48_b0_2d_7b_02_9c/volume_get

protocol/msg/AudioPlayExtend

ros2 interface show protocol/msg/AudioPlayExtend


string module_name
bool is_online
AudioPlay speech
        string module_name
        uint16 play_id
        ...
string text

ros2 topic pub --once /mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend protocol/msg/AudioPlayExtend "{}"
ros2 topic pub <topic_name> <msg_type> '<args>'

        speech_play_extend_voice->module_name = name_;
        speech_play_extend_voice->is_online = online;
        speech_play_extend_voice->speech.module_name = name_;
        speech_play_extend_voice->speech.play_id = 32;  // please close to me.
        speech_play_extend_voice->text = strs;
        speech_play_extend_->publish(std::move(speech_play_extend_voice));

ros2 topic pub /mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend protocol/msg/AudioPlayExtend "{module_name: 'test', is_online: true, speech: {module_name: 'test', play_id: 32 }, text: '程纪云，你在干嘛呢，休息一会吧，'}"



ros2 run motion_action client_test --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c "{mode: 111}" 



ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/camera_service protocol/srv/CameraService "{command: 1, args: ''}"

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




sudo mv /etc/mr813_version /etc/mr813_version.backup

