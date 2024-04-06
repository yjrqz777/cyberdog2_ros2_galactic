# cyberdog2 学习代码记录
## https://github.com/orgs/MiRoboticsLab/repositories?type=all  
2023年12月6日16:00:39 增加readme    
2023年12月6日21:23:09 测试了控制代码，控制了姿态，通过控制service控制了姿态（站立，趴下 demo: motion_action2    
2023年12月8日20:03:13 渐入佳境，改为使用python写就是快，目前发现只需要改写头文件就OK
```
例如：
#include "protocol/srv/audio_execute.hpp"         --> from protocol.srv import AudioExecute
#include "protocol/srv/audio_text_play.hpp"       --> from protocol.srv import AudioTextPlay
#include "protocol/msg/audio_play_extend.hpp"     --> from protocol.msg import AudioPlayExtend
#include "std_srvs/srv/trigger.hpp"               --> from std_srvs.srv import Trigger
#include "std_msgs/msg/u_int8.hpp"                --> from std_msgs.msg import UInt8
```

2023年12月8日20:36:32 成功实现wifi连接  
2023年12月8日21:41:37 talk_something/src/talkers.cpp 有一个bug,不能运行，明天修      
2023年12月9日12:57:14 talk_something/src/talkers.cpp 应用多线程 fix bug   
***
2023年12月19日17:12:28 测试camera  
2024年1月11日19:42:10 使用grpc 实现跑过程点grpc_demo/grpc_teleop2.py
2024年1月13日19:12:21  
想要控制狗的姿态，通过grpc控制失败，原因：未知 文件路径：/grpc_demo/grpc_motion_cmd.py           
通过lcm控制成功， *`但是是相对位移的控制`* 文件路径：/SDCARD/workspace/cyberdog2_ros2_galactic/loco_hl_example/basic_motion/main.py       
2024年1月18日15:52:23 增加海康摄像头

2024年1月19日16:35:45 ssh增加byobu-enable,关闭窗口依然可以运行

## 2024年3月7日21:37:22 增加tree.txt 说明文件目录 逐步更新


2024年3月8日19:53:25： grpc控制加入语言提醒


2024年3月11日16:47:40 增加wifi_ip 实现联网自动报ip,等待20秒

```
cyberdog_my_launch.service  
sudo cp cyberdog_my_launch.service /etc/systemd/system/
service 服务名 [start | stop | restart | reload | status]
```

```
[Unit]
Description="cyberdog my_wifi_ip"
Wants=mi_preset.service cyberdog_sudo.service cyberdog_autodock.service cyberdog_bringup.service SDCARD.mount
After=mi_preset.service cyberdog_sudo.service cyberdog_autodock.service cyberdog_bringup.service SDCARD.mount
Requires=cyberdog_autodock.service

[Service]
User=mi
Type=idle
ExecStartPre=/bin/sleep 5s
ExecStart=/bin/bash -c 'source /etc/mi/ros2_env.conf; source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash; ros2 launch my_launch my_wifi_ip.launch.py'
TimeoutStopSec=1
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

由于此节点在SDCARD上，所以启动时必须依赖服务 SDCARD.mount


```

sudo systemctl start cyberdog_my_launch.service             手动开启  
sudo systemctl stop cyberdog_my_launch.service
sudo systemctl enable cyberdog_my_launch.service            开启自启动  
sudo systemctl disable cyberdog_my_launch.service
sudo systemctl status cyberdog_my_launch.service            查看状态  

sudo systemctl restart cyberdog_my_launch.service           重启服务  

journalctl -u cyberdog_my_launch.service -f

sudo systemctl status SDCARD.mount

```


2024年3月11日20:47:45 日志：以上


2024.3.26 19：00 优化service

2024年4月5日17:53:36 尝试过10公分左右的台阶

2024年04月06日19:17:49
pcl_1_10 当编译motion_utils遇到pcl版本不对应，请使用1.10.0版本，并复制pcl_1_10/lib下文件到库路径/usr/lib/aarch64-linux-gnu/
```
查看库路径
ldconfig -p |grep pcl
复制
sudo cp -rf ./pcl_1_10/lib/lib* /usr/lib/aarch64-linux-gnu/
更新共享库
ldconfig
```


