## disable selinux:

adb root
adb shell setenforce 0

## 截屏：

adb shell screencap -p /sdcard/screencap.png
adb pull /sdcard/screencap.png

## 录屏：

adb shell screenrecord /sdcard/screenrecord.mp4
adb pull /sdcard/screenrecord.mp4

## dump 360 step：

1. 在 data 下 mkdir debug 文件夹和 dump 文件夹
   adb root;adb remount;adb shell;cd data/;mkdir debug/;mkdir dump;adb push camerasource_dump.cmd /data/debug

2. adb shell setenforce 0

3. adb shell; ps -A | grep -iE "atccamhalserver";kill -9 atccamhalserver 的进程

4. 执行上面 1 到 3 指令后查看/data/dump 目录下生成的视频流截取内容

说明：data/dump 目录下会存储 50 帧摄像头输出的视频流，格式为 yuv
