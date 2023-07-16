#!/bin/sh

set -x
# ../adb -host wait-for-device
now=$(date)
COUNTER=0
# START_TIME=$(SECONDS)

while true
do
    echo "Tested the $COUNTER times"
    # ../adb -host shell input tap 50 399 # Enter 360
    # sleep 1s

    ../adb -host shell input tap 65 182
    sleep 1s
    ../adb -host shell input tap 562 355
    sleep 1s
    ../adb -host shell input tap 300 115
    sleep 1s
    ../adb -host shell input tap 327 647
    sleep 1s

    # ../adb -host shell input tap 95 62 # Exit 360
    sleep 1s
    COUNTER=$((COUNTER + 1))
    echo "Current date: $(date) comparing $now"
done

# ELAPSED_TIME=$(($SECONDS - $START_TIME))
