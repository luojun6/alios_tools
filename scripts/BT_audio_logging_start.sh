#!/bin/sh
set -x

adb -host wait-for-device

adb -host shell "echo enable 0 > /proc/alog"
adb -host shell "mount -o remount rw  /"

adb -host shell setprop bt.phonecall.dump true
adb -host shell setprop persist.audio.dump io
adb -host shell setprop persist.ecnr.dump true
adb -host shell setprop auiohal.dump.write 1
adb -host shell "echo '1' > /keyinfo/bt/bluesdk/hci_stack.txt"
adb -host shell "echo '1' > /data/bt/bluesdk/hci_stack.txt"
adb -host shell mkdir -p /private/log/
adb -host shell rm -rf /private/log/*
adb -host shell logctl -p 2,3,4

# adb -host shell killall startup
# adb -host shell killall login
# adb -host shell sendlink page://systemsetting.ivi.com/systemsetting
# adb -host shell systemctl restart bt

filename="logcat_phone_audio_1.log"

adb -host shell logctl > $filename
