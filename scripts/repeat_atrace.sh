#!/bin/sh

set -x
# adb -host wait-for-device
now=$(date)
COUNTER=0
# START_TIME=$(SECONDS)

while true
do
    echo "Tested the $COUNTER times"
    COUNTER=$((COUNTER + 1))
    echo "Current date: $(date) comparing $now"
    # adb -host shell "mv /private/atrace.log.z /private/atrace.log.z.$COUNTER"
    adb -host shell atrace wm pm vm perf sched freq idle irq fusion -T 1 > atrace.log.$COUNTER.$now

done

# ELAPSED_TIME=$(($SECONDS - $START_TIME))
