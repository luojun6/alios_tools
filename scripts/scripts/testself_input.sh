set -x
../adb -host wait-for-device

while true
do
    ../adb -host shell input tap 65 182
    ../adb -host shell input tap 562 355
    ../adb -host shell input tap 300 115
    ../adb -host shell input tap 327 647
done
