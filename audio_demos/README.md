# audio_demos

### 概述

audio_demos为小米机器人cyberdog开源项目，音频模块使用demo.

开源地址：https://github.com/MiRoboticsLab

### docker环境

参考文档：https://miroboticslab.github.io/blogs/#/cn/dockerfile_instructions_cn

### 源码下载

将本项目工程下载到cyberdog_ws目录下

### 功能介绍

#### 1、talk#语音播报

```
//ros msg、srv接口
#include "protocol/srv/audio_execute.hpp"
#include "protocol/srv/audio_text_play.hpp"
#include "protocol/msg/audio_play_extend.hpp"
```

#### 2、set_mic # 打开、关闭麦克风

```
//ros msg、srv接口
#include "protocol/srv/audio_execute.hpp"
#include "protocol/msg/audio_status.hpp"
```

#### 3、set_voice# 音量设置与获取

```
//ros msg、srv接口
#include "std_srvs/srv/trigger.hpp"
#include "std_msgs/msg/u_int8.hpp"
```

#### 4、set_waken_words# 设置唤醒词

```
//ros msg、srv接口
#include "std_msgs/msg/string.hpp"
```

### 编译

```shell
source /opt/ros2/galactic/setup.bash

#第一次编译某个功能包需要使用--packages-up-to,编译该功能包及其依赖包

colcon build --merge-install --install-base /opt/ros2/cyberdog/ --packages-up-to audio_demos

#后续升级单个功能包使用--packages-select，只编译该功能包

colcon build --merge-install --install-base /opt/ros2/cyberdog/ --packages-select audio_demos
```

### 运行

#### 1、拷贝到机器狗上

```
#docker终端cyberdog_ws目录
mkdir -p audio_install/lib
mkdir -p audio_install/share
cp /opt/ros2/cyberdog/lib/audio_demos audio_install/lib
cp /opt/ros2/cyberdog/share/audio_demos audio_install/share
#本地终端cyberdog_ws目录
scp -r audio_install mi@192.168.55.1:/home/mi
#狗上终端/home/mi目录
cp -rf audio_install/lib /opt/ros2/cyberdog/lib
cp -rf audio_install/share /opt/ros2/cyberdog/share
sudo rm -rf audio_install

```

#### 2、在终端启动功能包

``` 
source /opt/ros2/cyberdog/setup.bash

#运行talker,运行后将听到狗发出一段语音（此demo需要联外网，外网不可用情况请情况请切换到离线语音）
ros2 run audio_demos talker --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"

#运行set_mic，运行后audio进入normal模式，可在代码中修改进入offmic模式
ros2 run audio_demos set_mic --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"

#运行set_voice，运行后将音量设置成50;可以根据唤醒机器狗，从语音上进行感受
ros2 run audio_demos set_voice --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"

#运行set_waken_words ，运行后唤醒词修改为”旺财旺财“
ros2 run audio_demos set_waken_words --ros-args -r __ns:=/`ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/"
```

