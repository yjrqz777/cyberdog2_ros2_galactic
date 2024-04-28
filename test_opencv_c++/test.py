# import cv2

# # cv2.namedWindow('camera',cv2.WINDOW_NORMAL)
# # print(cap.read()[1])
# while True:
#     cap = cv2.VideoCapture('rtsp://admin:air12345678@192.168.44.64/Streaming/Channels/101')
#     ret, img = cap.read()
#     if not ret:
#         exit()
#     new_width = 500
#     new_height = 500
#     img = cv2.resize(img, (new_width, new_height))
#     cv2.imshow('camera',img)
#     cv2.waitKey(1)


from hikvision_python.sdk import HikvisionSdk, HikvisionSdkException
import cv2
import numpy as np
# 初始化SDK
sdk = HikvisionSdk()
# 连接摄像头，假设IP地址为192.168.1.100，端口号为8000
if not sdk.connect('192.168.1.100', 8000):
    print('连接摄像头失败！')
    exit(1)
# 开始预览，设置分辨率为1280x720
if not sdk.start_preview(1280, 720):
    print('启动预览失败！')
    exit(1)
while True:
    # 获取一帧视频数据，时长为1/30秒（约33毫秒）
    ret, frame = sdk.get_frame()
    if not ret:
        print('获取视频帧失败！')
        break
    # 将BGR图像转换为RGB图像
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 显示图像并等待1毫秒（用于控制帧率）
    cv2.imshow('Hikvision Camera', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出循环
        break