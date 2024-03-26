from launch import LaunchDescription           # launch文件的描述类
from launch_ros.actions import Node            # 节点启动的描述类
# import manual as s

from mi.cyberdog_bringup.manual import get_namespace

#
# 预处理：仅处理命令行参数，详情参见 help_info
#


def generate_launch_description():             # 自动生成launch文件的函数
    return LaunchDescription([                 # 返回launch文件的描述信息
        Node(                                  # 配置一个节点的启动
            package='my_weakup',          # 节点所在的功能包
            executable='my_wakeup_node', # 节点的可执行文件
            namespace=get_namespace()
        ),
    ])
