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

# 2024年3月7日21:37:22 增加tree.txt 说明文件目录 逐步更新


2024年3月8日19:53:25： grpc控制加入语言提醒


2024年3月11日16:47:40 增加wifi_ip 实现联网自动报ip,等待15秒