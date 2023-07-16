#!/bin/sh

set -x


adb -host shell "echo enable 0 > /proc/alog" 


while true
do

    echo "Timestamp: $(date)w" >> ethtool.txt
    adb -host shell "ethtool -S eth0" >> ethtool.txt
    echo "------------------------------------------------------------------------\n" >> ethtool.txt
    sleep 1s

done

# ELAPSED_TIME=$(($SECONDS - $START_TIME))
