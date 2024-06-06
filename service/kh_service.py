import subprocess
import time
import logging
import sys

def main():
    # 设置日志记录到标准输出
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    logger.info("开始等待3分钟")
    # 延时2分钟
    time.sleep(180)
    
    command = (
        "/bin/bash -c 'source /etc/mi/ros2_env.conf; "
        "source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash; "
        "source /SDCARD/workspace/cyberdog2_ros2_galactic/hk_cam_ws/install/setup.bash; "
        "ros2 launch my_launch my_run.launch.py'"
    )
    
    logger.info("Executing command: %s", command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 读取子进程的输出和错误
    stdout, stderr = process.communicate()
    logger.info("Command output: %s", stdout.decode())
    if stderr:
        logger.error("Command error: %s", stderr.decode())

    logger.info("Script finished with return code %d", process.returncode)

if __name__ == "__main__":
    main()
