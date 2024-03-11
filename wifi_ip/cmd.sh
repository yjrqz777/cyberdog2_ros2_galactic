


ros2 pkg create wifi_ip --build-type ament_python --dependencies rclcpp

colcon build --merge-install --packages-select wifi_ip


