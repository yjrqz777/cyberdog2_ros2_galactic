import cv2

# 从电脑摄像头捕获视频
cap = cv2.VideoCapture(5)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 将图像转换为灰度图
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    # # 应用阈值处理，将白色背景二值化为白色（255）
    # _, thresholded = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    # cv2.imshow('Rectangles2', thresholded)
    # # 寻找轮廓
    # contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # 显示结果图像
    cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 按下ESC键退出循环
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
