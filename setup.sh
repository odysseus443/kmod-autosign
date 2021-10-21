#!/bin/sh
if (( $EUID != 0 )); then
    echo "Please run as root."
    exit
fi
rm -rf __pycache__/*
python -m py_compile autosign.py
mv __pycache__/* /sbin/autosign.pyc
cp autosign.service /lib/systemd/system/
systemctl enable autosign.service --now
systemctl daemon-reload