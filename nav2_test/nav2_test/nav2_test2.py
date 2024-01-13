#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from protocol.action import Navigation
from protocol.msg import AlgoTaskStatus
from protocol.srv import StopAlgoTask
from rclpy.executors import MultiThreadedExecutor

import time
mi_node = "/mi_desktop_48_b0_2d_7b_02_9c/"
'''
ros2 pkg create nav2_test --build-type ament_python --dependencies rclcpp

colcon build --merge-install --packages-select nav2_test

'''



class nva2_test(Node):
    def __init__(self, name):
        super().__init__(name)
        self._action_client = ActionClient(self, Navigation, mi_node + 'start_algo_task')

        self.stop_task = self.create_client(StopAlgoTask,mi_node + "stop_algo_task")

        # self.sub_wifi_status = self.create_subscription(
        #     AlgoTaskStatus,
        #     mi_node + "algo_task_status",
        #     self.task_status_callback,10)

        self.get_logger().info("----INIT----")


    def send_stop_task_request(self,id):
        self.get_logger().info("send_request")
        while not self.stop_task.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn('service not available, waiting again...')
        request = StopAlgoTask.Request()
        request.task_id = id
        request.map_name = "map22"
        future = self.stop_task.call_async(request)
        future.add_done_callback(self.stop_task_callback)

    def stop_task_callback(self,response):
        self.get_logger().info("connect_is_ok = {}+{}".format(response.result(), response.result().result))
        # self.get_logger().info("connect_is_ok = %d"%response.result().result)

    def send_task_id(self,id):
        task_msg = Navigation.Goal()
        task_msg.nav_type = id
        # if id == 6:

        # task_msg.poses = [
        #             "x": 0.49946996569633486,
        #             "y": 0.032208945602178577

        # ]

        task_msg.map_name = "map"

        # task_msg.label_id = "1"
        task_msg.outdoor = False
        while not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn('service not available, waiting again...')
            
        self._send_task = self._action_client.send_goal_async(
            task_msg,
            feedback_callback = self.task_msg_callback)
        self.get_logger().info("----SEND----")

        self._send_task.add_done_callback(self.send_response_callback)
        
    def send_response_callback(self,done_back):
        goal_handle = done_back.result()                   # 接收动作的结果
        self.get_logger().info("----{}----".format(goal_handle.accepted ))
        if not goal_handle.accepted:                    # 如果动作被拒绝执行
            self.get_logger().error('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted ')

        self._get_result_future = goal_handle.get_result_async()              # 异步获取动作最终执行的结果反馈
        self._get_result_future.add_done_callback(self.get_result_callback)   # 设置一个收到最终结果的回调函数 

    def get_result_callback(self, future):                                    # 创建一个收到最终结果的回调函数
        result = future.result().result                                       # 读取动作执行的结果
        self.get_logger().info('Result: {},{}'.format(result,result.result))            # 日志输出执行结果

    def task_msg_callback(self, feedback_msg):
        self.get_logger().info("----MSG----")
        feedback = feedback_msg.feedback
        self.get_logger().info("----{}+{}+{}----".format(feedback,feedback.feedback_code,feedback.feedback_msg))


    def task_status_callback(self,task_status):
        pass
        self.get_logger().info("task_status")
        self.get_logger().info("task_status:{},task_sub_status:{}"
                               .format(task_status.task_status,task_status.task_sub_status))

def main(args=None):
    rclpy.init(args=args)
    node = nva2_test("nav2_test_node")
    # node.send_task_id(1)
    node.send_stop_task_request(5) 
    # rclpy.spin(node)
    # # node.destroy_node()
    # rclpy.shutdown()
    # time.sleep(2)
    # node.send_task_id(6)
    executor = MultiThreadedExecutor()

    rclpy.spin(node, executor=executor)

    node.destroy()
    rclpy.shutdown()

if __name__ == "__main__":

    main()
