#!/bin/sh

set -x



../adb -host shell "echo enable 0 > /proc/alog" 


while true
do

    echo "Timestamp: $(date)w" >> dump_irq.txt
    ../adb -host shell "cat /proc/softirqs" >> dump_irq.txt
    echo "------------------------------------------------------------------------\n" >> dump_irq.txt
    ../adb -host shell "cat /proc/interrupts | grep -i eth0" >> dump_irq.txt
    echo "------------------------------------------------------------------------\n" >> dump_irq.txt
    # ../adb -host shell "ethtool -S eth0" >> dump_irq.txt
    # echo "------------------------------------------------------------------------\n" >> dump_irq.txt
    sleep 1s

done

# ELAPSED_TIME=$(($SECONDS - $START_TIME))
