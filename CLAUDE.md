# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repository is a ROS 2 Galactic workspace containing CyberDog2 learning/demo code. It is a collection of independent packages and scripts rather than one application: the top-level README explicitly notes that the whole repository cannot be built directly as one unit and packages should be built individually.

Most code targets the CyberDog2 runtime on Linux, usually with `/etc/mi/ros2_env.conf`, `/opt/ros2/cyberdog`, and `/SDCARD/workspace/cyberdog2_ros2_galactic` available. Many packages depend on Xiaomi/CyberDog ROS interfaces such as `protocol`, `cyberdog_common`, `cyberdog_debug`, `cyberdog_system`, `elec_skin`, `visualization`, and `cyberdog_visions_interfaces`, so builds on a generic ROS 2 installation will fail unless those dependencies are present.

## Build, test, and run commands

Use a Linux/CyberDog shell for ROS commands. Build selected packages; do not assume `colcon build` for the whole repository succeeds.

```bash
# CyberDog/ROS environment
source /opt/ros2/galactic/setup.bash
# On the robot, also load CyberDog environment/domain settings when running nodes
source /etc/mi/ros2_env.conf

# First build of a package plus dependencies
colcon build --merge-install --packages-up-to <package_name>

# Iterate on one package
colcon build --merge-install --packages-select <package_name>

# Build into CyberDog install base, as documented by audio_demos
colcon build --merge-install --install-base /opt/ros2/cyberdog/ --packages-up-to audio_demos
colcon build --merge-install --install-base /opt/ros2/cyberdog/ --packages-select audio_demos

# Source this workspace overlay after building
source install/setup.bash

# Run all tests for a selected package
colcon test --packages-select <package_name>
colcon test-result --verbose --all

# Run one generated Python package lint test directly
python3 -m pytest <package_name>/test/test_flake8.py
python3 -m pytest <package_name>/test/test_pep257.py
python3 -m pytest <package_name>/test/test_copyright.py
```

Common package-specific commands:

```bash
# Audio demos: namespace must match the active robot namespace
ros2 run audio_demos talker --ros-args -r __ns:=/$(ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/")
ros2 run audio_demos set_mic --ros-args -r __ns:=/$(ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/")
ros2 run audio_demos set_voice --ros-args -r __ns:=/$(ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/")
ros2 run audio_demos set_waken_words --ros-args -r __ns:=/$(ros2 node list | grep "mi_" | head -n 1 | cut -f 2 -d "/")

# Launch local helper nodes
ros2 launch my_launch my_wifi_ip.launch.py   # starts wifi_ip_node
ros2 launch my_launch my_test.launch.py      # starts my_weakup
ros2 launch my_launch my_run.launch.py       # starts hk_cam + hk_cam_slave from hk_cam_ws overlay

# Launch the Hikvision inspection stack through the service helper script
source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash
source /SDCARD/workspace/cyberdog2_ros2_galactic/hk_cam_ws/install/setup.bash
ros2 launch my_launch my_run.launch.py

# gRPC demos: regenerate stubs if cyberdog_app.proto changes
cd grpc_demo
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./cyberdog_app.proto
python3 grpc_teleop2.py 127.0.0.1 cert/ca-cert.pem cert/client-key.pem cert/client-cert.pem
```

Systemd service files live in `service/` and assume the workspace is deployed under `/SDCARD/workspace/cyberdog2_ros2_galactic`:

```bash
sudo cp ./service/cyberdog_my_launch.service /etc/systemd/system/
sudo cp ./service/cyberdog_my_run_launch.service /etc/systemd/system/
systemctl daemon-reload
sudo systemctl start cyberdog_my_launch.service
sudo systemctl status cyberdog_my_launch.service
journalctl -u cyberdog_my_launch.service -f
```

The repository contains a `hk_cam_ws` git submodule. If it is missing or empty, initialize it before building camera packages:

```bash
git submodule update --init --recursive
```

## Architecture and package map

### Launch and bringup

- `cyberdog_bringup` is a launch-generation package. Its `CMakeLists.txt` calls `automatically_generate_launch_files(NODE)`, which reads YAML metadata in `cyberdog_bringup/automatic/` and installs generated launch files. `bringup/manual.py` provides helpers such as `get_namespace()`, which builds the robot namespace from hostname and the `eth0` MAC address.
- `my_launch` is an `ament_python` launch-only package. `my_wifi_ip.launch.py`, `my_test.launch.py`, and `my_run.launch.py` start selected nodes using `mi.cyberdog_bringup.manual.get_namespace()`. `my_run.launch.py` depends on `hk_cam` and `hk_cam_slave`, so the `hk_cam_ws` overlay must also be sourced.
- `service/` contains systemd units and `kh_service.sh` for delayed startup after CyberDog services and `SDCARD.mount` are ready.

### Motion, audio, and robot interaction demos

- `motion_action` is a mixed C++/Python `ament_cmake` package. The C++ library wraps CyberDog motion protocol/LCM control and depends on `skin_manager`; scripts such as `motion_demo.py`, `motion_teleop.py`, and `pose_teleop.py` call motion helper functions. The package also builds C++ test executables (`manager_test`, `controller_test`, `publisher_test`, `client_test`).
- `skin_manager` builds a shared C++ library for electronic skin behavior through `elec_skin` and CyberDog protocol dependencies.
- `audio_demos` and `talk_something` are C++ protocol/audio examples. `audio_demos` exposes `talker`, `set_mic`, `set_voice`, and `set_waken_words`; `talk_something` builds `talks_node`.
- `audio_test`, `my_weakup`, `wifi_ip`, `wifi_test`, `camera_picture`, `ptz_camera`, and `nav2_test` are small `ament_python` packages with console entry points defined in their `setup.py` files.

### Navigation and perception

- `nav2_demo/nav2_control_demo` is a C++ package for mapping, localization, and navigation demos. It builds `nav2_mapping`, `nav2_localization`, and `nav2_navigatte_pose`, installs launch files and Nav2 parameter YAML, and depends on Nav2 plus CyberDog visualization/vision interfaces.
- `nav2_demo/README.md` documents the runtime flow for laser/vision mapping, localization, and AB-point navigation. It uses lifecycle nodes, mapping/location services, and the `protocol/action/Navigation` action named `start_algo_task`.
- `stair_find` is a C++ behavior/navigation package with a `stair_find` executable. Its CMake currently compiles `main.cpp`, `stair_find.cpp`, and `executor_base.cpp`; many related executor sources are present but commented out in the build.
- `pcl_1_10/` vendors PCL 1.10 files. The README notes this is needed when CyberDog motion-related builds encounter PCL version mismatches; copy the provided libraries into `/usr/lib/aarch64-linux-gnu/` only on the target system when that mismatch is confirmed.

### Interfaces and camera workspaces

- `my_interface` defines `my_interface/srv/PtzCam.srv` via `rosidl_generate_interfaces()`.
- `hk_cam_ws` is a separate ROS workspace tracked as a git submodule. It has its own `CLAUDE.md`; read that file before changing `hk_cam_ws/src/hk_interfaces`, `hk_cam_ws/src/hk_cam`, or `hk_cam_ws/src/hk_cam_slave`.
- Top-level `ptz_camera` and `hk/` are Python Hikvision SDK experiments; `hk_cam_ws` is the structured ROS 2 camera workspace used by `my_launch/my_run.launch.py`.

### Non-ROS demos and generated code

- `grpc_demo/` contains CyberDog app gRPC examples and generated `cyberdog_app_pb2*.py` stubs. Regenerate them from `cyberdog_app.proto` when the proto or gRPC/protobuf version changes.
- `loco_hl_example/` contains LCM high-level locomotion examples (`basic_motion`, `customized_gait`, `sequential_motion`) based on CyberDog locomotion control messages.
- `tree.txt` is an older directory snapshot and is useful for orientation, but it is not authoritative for current files.

## Important implementation notes

- Keep package changes scoped: because this is a collection of demos with many unavailable robot-specific dependencies, prefer `colcon build --packages-select` or `--packages-up-to` for the package being changed.
- Package and executable names are sometimes misspelled and should not be silently renamed (`my_weakup`, `nav2_navigatte_pose`, `moto_contor_test`, `grpc_cerate_map.py`) because launch files and notes may depend on those names.
- Runtime ROS domain/namespace matters. The top-level README recommends setting `ROS_DOMAIN_ID=5` in `/etc/mi/ros2_env.conf` and matching the developer shell to the same domain for distributed communication.
- Several scripts contain hard-coded CyberDog paths under `/SDCARD`, `/home/mi`, and `/opt/ros2/cyberdog`; preserve those assumptions unless explicitly making the code configurable.
