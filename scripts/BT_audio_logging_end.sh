#!/bin/sh
#adb='/mnt/c/work/tools/adb_fastboot_tools/windows/adb.exe'
set -x
adb -host wait-for-device

filename="log_phone_audio_1"
mkdir $filename

adb -host shell "rm -rf /data/THL/*"
adb -host shell "mkdir /data/THL"
adb -host shell "mv /data/sco_* /data/THL"
adb -host shell "mv /data/wave_* /data/THL"
adb -host shell "mv /tmp/audio* /data/THL"
adb -host shell "mv /data/mic_* /data/THL"
adb -host shell "mv /tmp/*.pcm /data/THL"

adb -host shell "mv /private/log/*.log /data/THL"
adb -host shell "mv /private/log/*.txt /data/THL"

adb -host pull /data/THL  $filename/
adb -host shell "killall logctl"
cp logcat* $filename
killall logcat* 
#ls $filename




