

/mi_desktop_48_b0_2d_7b_02_9c

ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/map_builder 1
ros2 lifecycle set /mi_desktop_48_b0_2d_7b_02_9c/map_builder 3

colcon build --merge-install --packages-select nav2_control_demo


ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/start_mapping std_srvs/srv/SetBool "{data: true}"


ros2 service call /mi_desktop_48_b0_2d_7b_02_9c/stop_mapping visualization/srv/stop "{finish: true, map_name: 'map'}"


mi@mi-desktop:/SDCARD/workspace/cyberdog2_ros2_galactic$ ros2 interface show protocol/action/Navigation
#goal definition
uint8 NAVIGATION_TYPE_UNKNWON = 0
uint8 NAVIGATION_TYPE_START_AB = 1
uint8 NAVIGATION_TYPE_STOP_AB = 2
uint8 NAVIGATION_TYPE_START_FOLLOW = 3
uint8 NAVIGATION_TYPE_STOP_FOLLOW = 4
uint8 NAVIGATION_TYPE_START_MAPPING = 5
uint8 NAVIGATION_TYPE_STOP_MAPPING = 6
uint8 NAVIGATION_TYPE_START_LOCALIZATION = 7
uint8 NAVIGATION_TYPE_STOP_LOCALIZATION = 8
uint8 NAVIGATION_TYPE_START_AUTO_DOCKING = 9
uint8 NAVIGATION_TYPE_STOP_AUTO_DOCKING = 10
uint8 NAVIGATION_TYPE_START_UWB_TRACKING = 11
uint8 NAVIGATION_TYPE_STOP_UWB_TRACKING = 12
uint8 NAVIGATION_TYPE_START_HUMAN_TRACKING = 13
uint8 NAVIGATION_TYPE_STOP_HUMAN_TRACKING = 14
uint8 NAVIGATION_GOAL_TYPE_AB = 101
uint8 NAVIGATION_GOAL_TYPE_FOLLOW = 102
uint8 nav_type

geometry_msgs/PoseStamped[] poses # 导航的目标点设置
        std_msgs/Header header
                builtin_interfaces/Time stamp
                        int32 sec
                        uint32 nanosec
                string frame_id
        Pose pose
                Point position
                        float64 x
                        float64 y
                        float64 z
                Quaternion orientation
                        float64 x 0
                        float64 y 0
                        float64 z 0
                        float64 w 1

string label_id
string map_name

sensor_msgs/RegionOfInterest tracking_roi
        #
        uint32 x_offset
                         # (0 if the ROI includes the left edge of the image)
        uint32 y_offset
                         # (0 if the ROI includes the top edge of the image)
        uint32 height
        uint32 width
        bool do_rectify

uint8 TRACING_AUTO = 200 # 自主选择跟随位置
uint8 TRACING_BEHIND = 201 # 在目标后侧跟随
uint8 TRACING_LEFT = 202 # 在目标的左侧跟随
uint8 TRACING_RIGHT = 203 # 在目标的右侧跟随
uint8 relative_pos # 相对方位，以上方定义的枚举值指定
float32 keep_distance # 与跟随目标所保持的距离

bool outdoor
bool object_tracking
---
#result definition
uint8 result
uint8 NAVIGATION_RESULT_TYPE_SUCCESS = 0
uint8 NAVIGATION_RESULT_TYPE_ACCEPT = 1
uint8 NAVIGATION_RESULT_TYPE_UNAVALIBLE =2
uint8 NAVIGATION_RESULT_TYPE_FAILED = 3
uint8 NAVIGATION_RESULT_TYPE_REJECT = 4
uint8 NAVIGATION_RESULT_TYPE_CANCEL = 5
---
#feedback definition
#geometry_msgs/PoseStamped current_pose
#builtin_interfaces/Duration navigation_time
#builtin_interfaces/Duration estimated_time_remaining
#int16 number_of_recoveries
#float32 distance_remaining
#int16 number_of_poses_remaining
int32 NAVIGATION_FEEDBACK_RELOCING_SUCCESS = 0 # 重定位成功
int32 NAVIGATION_FEEDBACK_RELOCING_RETRYING = 100 # 重试重定位
int32 NAVIGATION_FEEDBACK_RELOCING_FAILED = 200 # 重定位失败

# Navigation feedback code for app handle
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB = 1
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB_SUCCESS = 2
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB_FAILURE = 3
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB_PATH_PLAN_SUCCESS = 4
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB_PATH_PLAN_FAILURE = 5
int32 NAVIGATION_FEEDBACK_NAVIGATING_AB_RUNNING = 20

# Build map feedback code for app handle
int32 NAVIGATION_FEEDBACK_SLAM_BUILD_MAPPING_SUCCESS = 6
int32 NAVIGATION_FEEDBACK_SLAM_BUILD_MAPPING_FAILURE = 7

# Relocation feedback code for app handle
int32 NAVIGATION_FEEDBACK_SLAM_RELOCATION_SUCCESS = 8
int32 NAVIGATION_FEEDBACK_SLAM_RELOCATION_FAILURE = 9

int32 NAVIGATION_FEEDBACK_BASE_TRACKING_NOEXCEPTION = 10 # UWB正常跟随中
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_DETECOTOREXCEPTION =11 # UWB跟随目标丢失
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_TFEXCEPTION =12 #  UWB跟随TF数据异常
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_PLANNNEREXCEPTION =13 # UWB跟随planner异常
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_CONTROLLEREXCEPTION =14 # UWB跟随controller异常
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_EMPTY_TARGET =15 # UWB启动时目标为空
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_STAIRJUMPING =16 # UWB跟随中触发了跳台阶
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_AUTOTRACKING =17 # UWB跟随中触发了自主行为
int32 NAVIGATION_FEEDBACK_BASE_TRACKING_BEHAVIORABNORM =18 # UWB跟随中的自主行为异常

int32 TASK_PREPARATION_EXECUTING = 1000 # 正在激活依赖节点
int32 TASK_PREPARATION_SUCCESS = 1001 # 激活依赖节点成功
int32 TASK_PREPARATION_FAILED = 1002 # 激活依赖节点失败
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_STARTING =500 # 人体与万物跟随启动中
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_READY =501 # 人体与万物跟随等待选择目标
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_OBJECT_SELECTED =502 # 人体与万物跟随目标已经选定
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_OBJECT_FOLLOWING =503 # 人体与万物跟随中
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_OBJECT_DISAPPEAR =504 # 人体与万物跟随目标丢失, 寻找目标
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_OBJECT_LOSE =505 # 人体与万物跟随目标彻底丢失，请重新选择目标
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_STARTING_FAILED =506 # 人体与万物跟随启动失败，请重试
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_OBJECT_SELECTED_FAILED =507 # 人体与万物跟随锁定目标失败，请重试
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_RESET_FAILED =508 # 人体与万物跟随选择自动重启失败，请重试
int32 NAVIGATION_FEEDBACK_VISION_TRACKING_TARGET_EMPTY =509 # 人体与万物跟随没有找到跟随目标，请重试
int32 feedback_code
string feedback_msg











