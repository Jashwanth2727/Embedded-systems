#!/bin/bash

LOGFILE="/home/rpi5/boot_wifi.log"
PYTHON_SCRIPT="/home/rpi5/myprogram.py"

SSID1="OHealth"
PASS1="your_password_1"

SSID2="Shashank"
PASS2="your_password_2"

SSID3="Jashwanth"
PASS3="your_password_3"

echo "========== $(date) ==========" >> "$LOGFILE"
echo "Boot startup script started" >> "$LOGFILE"

sleep 15

echo "Checking WiFi scan..." >> "$LOGFILE"
SCAN_RESULT=$(sudo nmcli -t -f SSID dev wifi list 2>>"$LOGFILE")

connect_wifi() {
    local SSID="$1"
    local PASS="$2"

    if echo "$SCAN_RESULT" | grep -Fxq "$SSID"; then
        echo "Found SSID: $SSID" >> "$LOGFILE"

        sudo nmcli dev wifi connect "$SSID" password "$PASS" >> "$LOGFILE" 2>&1
        sleep 8

        if sudo nmcli -t -f ACTIVE,SSID dev wifi | grep -q "^yes:$SSID$"; then
            echo "Connected to $SSID successfully" >> "$LOGFILE"
            return 0
        else
            echo "Failed to connect to $SSID" >> "$LOGFILE"
        fi
    else
        echo "SSID not found: $SSID" >> "$LOGFILE"
    fi

    return 1
}

connect_wifi "$SSID1" "$PASS1" || \
connect_wifi "$SSID2" "$PASS2" || \
connect_wifi "$SSID3" "$PASS3"

echo "Network status:" >> "$LOGFILE"
ip addr show >> "$LOGFILE" 2>&1

echo "Starting Python program..." >> "$LOGFILE"
exec /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOGFILE" 2>&1
