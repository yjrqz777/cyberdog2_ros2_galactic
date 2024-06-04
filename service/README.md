

```
cyberdog_my_launch.service  
sudo cp ./service/cyberdog_my_launch.service /etc/systemd/system/
sudo cp ./service/cyberdog_my_run_launch.service /etc/systemd/system/
service 服务名 [start | stop | restart | reload | status]
```

```
[Unit]
Description="cyberdog my_wifi_ip"
Wants=mi_preset.service cyberdog_sudo.service cyberdog_autodock.service cyberdog_bringup.service SDCARD.mount
After=mi_preset.service cyberdog_sudo.service cyberdog_autodock.service cyberdog_bringup.service SDCARD.mount
Requires=cyberdog_autodock.service

[Service]
User=mi
Type=idle
ExecStartPre=/bin/sleep 5s
ExecStart=/bin/bash -c 'source /etc/mi/ros2_env.conf; source /SDCARD/workspace/cyberdog2_ros2_galactic/install/setup.bash; ros2 launch my_launch my_wifi_ip.launch.py'
TimeoutStopSec=1
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

由于此节点在SDCARD上，所以启动时必须依赖服务 SDCARD.mount


```

sudo systemctl start cyberdog_my_launch.service             手动开启  

sudo systemctl stop cyberdog_my_launch.service
sudo systemctl enable cyberdog_my_launch.service            开启自启动  
sudo systemctl disable cyberdog_my_launch.service
sudo systemctl status cyberdog_my_launch.service            查看状态  

sudo systemctl restart cyberdog_my_launch.service           重启服务  

journalctl -u cyberdog_my_launch.service -f

sudo systemctl start cyberdog_my_run_launch.service             手动开启  
sudo systemctl stop cyberdog_my_run_launch.service
sudo systemctl disable cyberdog_my_run_launch.service
sudo systemctl status cyberdog_my_run_launch.service
enable

journalctl -u cyberdog_my_run_launch.service -f
sudo systemctl status SDCARD.mount

```
