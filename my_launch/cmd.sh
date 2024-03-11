

ros2 pkg create my_launch --build-type ament_python --dependencies rclcpp


colcon build --merge-install --packages-select my_launch



ros2 launch my_launch my_wifi_ip.launch.py