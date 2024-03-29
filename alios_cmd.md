# AliOS Command Tips

## ADB Basic

```sh
adb -host shell
```

### Fastboot

```sh
adb -host reboot recovery
adb -host reboot fastboot
```

_Check the fastboot.sh_

```sh
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img
fastboot reboot
```

### Remount

```sh
adb -host remount
adb -host shell "echo 'enable n;' > /proc/alog && mount -o remount,rw /"
```

### Logging

```sh
adb -host shell dmesg --follow --time-format iso
adb -host shell dmesg --follow --time-format iso > dmesg.log
```

```sh
adb -host logctl -p 2,3,4
```

_In adb shell_

```sh
echo 7 > /proc/sys/kernel/printk
echo 7 > /sys/class/ipcl/debug/debug_level
dmesg -n8
```

### Software Information

```sh
sys-test --get-ver
getprop ro.build.version.release
getprop | grep -i release
```

## Security

### Login

```sh
sendlink page://login.ivi.com/loginservice -e passwdlogin -d '{"name": "17000000008","password":"72hsh7*banma"}'
```

### Alisec

```sh
echo "enable 0;" >/proc/alog
echo "enable y;" >/proc/alog
```

### TA

ta_path: /lib/optee_armtz/

```sh
adb -host push ./alisec_patch/asecpolicy.bin /etc/security
```

## BSP

### YFVE Camera TVI/AHD parameter

```sh
i2cdump -f -y 1 0x44
```

```sh
i2cset -f -y 1 0x44 0x40 0x04
```

### Display

```sh
cat /sys/class/backlight/lcd-backlight/brightness
echo 100 >  /sys/class/backlight/lcd-backlight/brightness
```

EP39EV_FICMDayNightMd_CMD = 870,
EP39EV_ClstrDayNightMd_MSG = 1263,
EP39ER_FICMDayNightMd_CMD = 771,
EP39ER_ClstrDayNightMd_MSG = 1021,

### Touch Panel

```sh
getevent -l /dev/input/event1
```

### Serial-COM Logging

```sh
sudo picocom -b 921600 /dev/ttyUSB0

```

### Wifi

```sh
echo 0 > /dev/wmtWifi  移除wlan0和ap0
echo 1 > /dev/wmtWifi 创建wlan0
echo AP > /dev/wmtWifi  创建ap0
```

## Audio

```sh
# Open
setprop persist.audio.dump io

# Try to reproduce the audio issue

# close
setprop persist.audio.dump 0
```

## IPCL & vapisend

```sh
echo 2:IPCL_EOL_CMD_EVENT:1538,1>/sys/class/ipcl/debug/fake_uevent      # Factory Reseet
echo 1:IPCL_CAN_SIGNAL_EVENT:989,0> /sys/class/ipcl/debug/fake_uevent   # Closed ecall
```

```sh
# Veicle Power ON
echo 1:IPCL_CAN_SIGNAL_EVENT:50,2>/sys/class/ipcl/debug/fake_uevent
echo 0:IPCL_CAN_SIGNAL_EVENT:50,2>/sys/class/ipcl/debug/fake_uevent

# Power ON Air-Conditioner
vapisend ctrl.ac.power_status '{"CMD":"ctrl.ac.power_status","PARAM":"{\"sigVal\":\"1\"}"}'
vapisend ctrl.ac.power_status '{"CMD":"ctrl.ac.power_status","PARAM":"{\"sigVal\":\"0\"}"}'
echo 1:IPCL_CAN_SIGNAL_EVENT:51,1>/sys/class/ipcl/debug/fake_uevent
echo 1:IPCL_CAN_SIGNAL_EVENT:51,0>/sys/class/ipcl/debug/fake_uevent

# Air-Conditioner -> wind mode
vapisend ctrl.ac.driver_temperature '{"CMD":"ctrl.ac.driver_temperature","PARAM":"{\"sigVal\":\"26\"}"}'


# Quick-cooling
echo 1:IPCL_CAN_SIGNAL_EVENT:402,1>/sys/class/ipcl/debug/fake_uevent
echo 1:IPCL_CAN_SIGNAL_EVENT:402,0>/sys/class/ipcl/debug/fake_uevent

# Get quick-cooling calibration
vapisend -get system.setting.calibration custom_805306376
# DID:C019
# DATA:00 FF FF FF (00 - button, 01 - no button)


# read eco calibration
vapisend ctrl.ac.eco_switch '{"CMD":"ctrl.ac.eco_switch","PARAM":"{\"sigVal\":\"1\"}"}'
ctrl.ac.eco_switch
vapisend -get system.setting.calibration ElectricVehicle_AC_SupportECOSwitch
vapisend -get system.setting.calibration Vehicle_EnergyType
```

## CPU

```sh
cat /proc/interrupts | grep eth
echo 2 > /proc/irq/263/smp_affinity
```

## Debugging

### Capture Screenshot

```sh
uiautomator_screencap
```

```sh
adb -host shell weston-screenshooter
adb -host pull /data/screenshot.png
```

### Debug Logging

```sh
adb -host shell setprop persist.bmlog.log.level 3
```

```sh
adb -host shell atrace wm pm vm perf sched freq idle irq fusion  > atrace.log
```

_In adb shell_

```sh
debuggerd -b `pidof standsrv` > /private/standsrv.bt.log
gdb --batch -ex "thread apply all bt" -p `pidof standsrv`
```

### Video

```sh
mkdir /data/camera
setprop camera.client.dump 10 # Data will be stored in /data/camera
```

```sh
videocap -r -c 0 -t 10  -p /tmp/videocap.yuv
```

### Tips - 接进入 wifi 连接界面

使用 adb 命令跳过登陆页面，直接进入 wifi 连接界面的步骤： 0. 进入斑马系统的 shell 命令环境：adb -host shell

1. 跳过启动界面 killall startup
2. 进入系统设置页面 sendlink page://systemsetting.ivi.com/systemsetting
3. 手动连接 wifi
4. 重新进入登陆界面 sendlink page://startup.ivi.com/startup
5. 输入账号密码
   或用命令输入账号密码：sendlink page://login.ivi.com/loginservice -e passwdlogin - d'{"name":"17000000009","password":"72hsh7\*ni"}'

### System Calls

```sh
killall seed   # Kill all processes
```

### Pull Codes

```sh
adb -host shell
cd opt/app
ls
cd aircondition.ivi.com
pwd
exit
adb -host pull opt/app/aircondition.ivi.com aircondition.ivi.com
adb -host pull opt/app/smartcar.ivi.com/node_modules node_modules
```

## Javis

### Debugging

1.拉取场景引擎脚本

```sh
adb -host pull /private/jarvis .
```

2.打开场景引擎开机启动日志开关

theme_script_name: `state_E5BKBEU5TVSB0W1F2OHK`

```sh
adb -host remount
adb -host shell "echo 'enable n;' > /proc/alog && mount -o remount,rw /"
adb -host shell "setprop persist.sys.jarvis.logdebug 1"
adb -host shell "setprop persist.sys.jarvis.logfile 'true'"
adb -host shell "rm -rf /tmp/jarvisd.log"
```

3.重启之后，场景引擎开机日志记录在/tmp/jarvisd.log ，拉取出来即可，每次重启都会覆盖

### Command

```sh
setprop persist.sys.aui.extend.setting hdt
setprop persist.sys.aui.extend.setting hdt_light
```

## Keywords in logcat

background light power: bl_power

power management:

- PMRC_REQ_PWR_MODE_CHG
- PMRC_PM2PA_INFO_30MIN_TIMEOUT
- V850 Send PMRC_REQ_SYSTEM_OFF

cat all_log.log | grep -vE "PM2PA_INFO_REP_VOLTAGE" | grep -iE "PMRC_REQ_PWR_MODE_CHG|V850 Send|IPCL_CAN_SIGNAL_EVENT:50,|IPCL_CAN_SIGNAL_EVENT:200,|IPCL_CAN_SIGNAL_EVENT:10,|IPCL_CAN_SIGNAL_EVENT:11,|IPCL_CAN_SIGNAL_EVENT:1075,|ctrl.custom.536880839"

cat all_log.log

## Check fdisk exploded

```sh
du -sm *
```

## Debug RVC TVD

```sh
echo regw:0x14013434=0x040000ff > /sys/kernel/debug/mtkdrm
echo regw:0x14013434=0x04ff0080 > /sys/kernel/debug/mtkdrm
echo regw:0x14013434=0x04000080 > /sys/kernel/debug/mtkdrm
```

echo regw:0x14013434=0x04000080 > /sys/kernel/debug/mtkdrm
两种范围：
04000080 -- 0x07ff0080
或者
04000080 -- 0x040000ff
两种范围，第一种 080 是最大亮度，第二种 0ff 是最大亮度

# echo regw:0x14013434=0x040000dd > /sys/kernel/debug/mtkdrm -> EP39 Executed only

# echo regw:0x14013434=0x04ff0080 > /sys/kernel/debug/mtkdrm

```sh
因为接收camera数据、算法处理、显示输出是同时运行的异步线程，所以不能简单看 “收到数据 -> 算法开始处理   -> 开始输出到显示渲染”的耗时相减得到的结果，因为可能在一个时间点算法处理的是当前帧，而算法处理的是上一帧；
可以通过logctl 查看camera帧率、算法帧率来查看360的运行耗时：
camer帧率：（约30fps）
12-13 07:37:10.638  4  1542  8862 I SRV:  ShowFPS,CameraUtils.cpp,L22: cameraID: 2, cameraFps: 29.2
算法帧率：
命令执行logctl | grep srv_algo
显示帧率：（12-13 07:37:09.485 - 12-13 07:37:09.451 = 34ms， 30帧）
12-13 07:37:09.451  1  1542  2481 I SRV:  doReady,Window.cpp,L154: Window setVisibility true
12-13 07:37:09.485  1  1542  2481 I SRV:  doReady,Window.cpp,L154: Window setVisibility true


1.1 360收到摄像头数据（四路）：
12-13 07:37:09.435  2  1542  8868 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=1, StreamData address=0x7f80025af0, data->vaddr=0x7f391e8000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.437  2  1542  8862 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=2, StreamData address=0x7f6400f590, data->vaddr=0x7f37f26000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.437  2  1542  8880 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=3, StreamData address=0x7f700154a0, data->vaddr=0x7f3395c000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.439  4  1542  8874 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=4, StreamData address=0x7f70014e90, data->vaddr=0x7f3380a000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0

12-13 07:37:09.468  2  1542  8868 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=1, StreamData address=0x7f680069a0, data->vaddr=0x7f38f23000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.469  4  1542  8874 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=4, StreamData address=0x7f68006bc0, data->vaddr=0x7f336b8000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.470  4  1542  8862 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=2, StreamData address=0x7f68006560, data->vaddr=0x7f3a1b2000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0
12-13 07:37:09.472  4  1542  8880 I SRV:  OnPreviewTaken,CameraWrapper.cpp,L163: OnPreviewTaken, cameraId=3, StreamData address=0x7f700152f0, data->vaddr=0x7f310ab000, data->dataSize=0, data->info.imgSize=1382400, data->info.width=1280, data->info.height=720, data->info.stride=0

1.2 算法开始处理：
12-13 07:37:09.443  5  1542  2804 I SRV:  process,ZsvLinerPrivateData2.cpp,L558: m_zsv_vehicle_data size 1  push speed: 0 f_wheel_angle f_l: 2.0073 f_r: 1.75048 b_l: -0 b_r: -0 f_l_speed: 0 f_r_speed: 0 b_l_speed: 0 b_r_speed: 0 _vehicle_speed:  0 _left_run_wheel_speed: 0 _right_run_wheel_speed: 0 _left_wheel_speed: 0 _right_wheel_speed: 0 _elec_speed: 0 timestamp 996329538365
12-13 07:37:09.480  5  1542  2804 I SRV:  process,ZsvLinerPrivateData2.cpp,L558: m_zsv_vehicle_data size 1  push speed: 0 f_wheel_angle f_l: 2.0073 f_r: 1.75048 b_l: -0 b_r: -0 f_l_speed: 0 f_r_speed: 0 b_l_speed: 0 b_r_speed: 0 _vehicle_speed:  0 _left_run_wheel_speed: 0 _right_run_wheel_speed: 0 _left_wheel_speed: 0 _right_wheel_speed: 0 _elec_speed: 0 timestamp 996366573596


1.3 输入算法到算法处理完成输出：
暂无log

1.4 360输出到显示渲染：
12-13 07:37:09.451  1  1542  2481 I SRV:  doReady,Window.cpp,L154: Window setVisibility true
12-13 07:37:09.485  1  1542  2481 I SRV:  doReady,Window.cpp,L154: Window setVisibility true
```
