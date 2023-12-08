# cyberdog2 学习代码记录
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