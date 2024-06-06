#!/bin/bash

# 输出启动信息到日志
echo "$(date) - Starting the script, waiting for 2 minutes..."

# 延时2分钟
sleep 180

# 输出执行命令信息到日志
echo "$(date) - Executing command: source /etc/mi/ros2_env.conf; source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash; source /SDCARD/workspace/cyberdog2_ros2_galactic/hk_cam_ws/install/setup.bash; ros2 launch my_launch my_run.launch.py"

# 执行命令
source /etc/mi/ros2_env.conf
source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash
source /SDCARD/workspace/cyberdog2_ros2_galactic/hk_cam_ws/install/setup.bash
ros2 launch my_launch my_run.launch.py

# 输出完成信息到日志
echo "$(date) - Script finished"
