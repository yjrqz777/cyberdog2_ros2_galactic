#配置用户名
git config --global user.name "yjrqz777"

#配置邮箱
git config --global user.email  3210551161@qq.com


ros2 pkg create moto_contor_test --build-type ament_cmake --dependencies rclcpp

colcon build --merge-install --packages-select moto_contor_test

ros2 run moto_contor_test talks_node --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"`

ros2 run moto_contor_test talks_node --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c

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



ros2 topic list|grep speech_play_extend
/mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend


ros2 topic echo /mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend
ros2 topic info /mi_desktop_48_b0_2d_7b_02_9c/speech_play_extend

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



ros2 run motion_action controller_test "{mode: 111}" --ros-args -r __ns:=/mi_desktop_48_b0_2d_7b_02_9c
