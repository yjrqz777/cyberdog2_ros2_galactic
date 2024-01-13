# grpc demo

## 安装

`pip3 install grpcio grpcio_tools`


python3 -m pip install grpcio grpcio_tools -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip install protobuf==4.0.0rc1 i https://pypi.tuna.tsinghua.edu.cn/simple

`python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./cyberdog_app.proto`
## 运行
请先获取到机器人在局域网中的IP，参数分别为：机器人的ip、CA证书、client秘钥、client证书  
`python3 grpc_teleop.py 192.168.xxx.xxx cert/ca-cert.pem cert/client-key.pem cert/client-cert.pem`  
操作方法类似turtlebot3的遥控程序，w、x、a、d分别为前后左右加速，不按键盘时速度保持不变，s为停止，esc为退出  


python3 /SDCARD/workspace/cyberdog2_ros2_galactic/grpc_demo/grpc_teleop2.py 127.0.0.1 /SDCARD/workspace/cyberdog2_ros2_galactic/grpc_demo/cert/ca-cert.pem /SDCARD/workspace/cyberdog2_ros2_galactic/grpc_demo/cert/client-key.pem /SDCARD/workspace/cyberdog2_ros2_galactic/grpc_demo/cert/client-cert.pem

python3 grpc_teleop2.py 127.0.0.1 cert/ca-cert.pem cert/client-key.pem cert/client-cert.pem


python3 grpc_cerate_map.py 127.0.0.1 cert/ca-cert.pem cert/client-key.pem cert/client-cert.pem
