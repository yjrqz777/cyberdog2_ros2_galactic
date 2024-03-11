


ros2 pkg create wifi_ip --build-type ament_python --dependencies rclcpp

colcon build --merge-install --packages-select wifi_ip


cp -r /SDCARD/workspace/cyberdog2_ros2_galactic/install/share/wifi_ip/ /opt/ros2/cyberdog/share/


cp -r /SDCARD/workspace/cyberdog2_ros2_galactic/install/lib/wifi_ip/ /opt/ros2/cyberdog/lib/

