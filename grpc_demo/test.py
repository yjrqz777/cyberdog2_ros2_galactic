
import os
import select
import sys

if os.name == 'nt':
    import msvcrt
    print('os.name is nt')
else:
    import termios
    import tty 
    print('os.name is', os.name)

import time
import grpc as gpcs
import json
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc
sys.path.append("/SDCARD/workspace/cyberdog2_ros2_galactic/hk")
from Ptz_Camera_Lib import Ptz_Camera as a



a()