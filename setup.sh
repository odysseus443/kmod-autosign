#!/bin/sh
if (( $EUID != 0 )); then
    echo "Please run as root."
    exit
fi
cp autosign.py /sbin/
cp autosign.service /lib/systemd/system/
systemctl enable autosign.service --now
systemctl daemon-reload