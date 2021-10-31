#!/bin/sh
if (( $EUID != 0 )); then
    echo "Please run as root."
    exit
fi
if [ -d "__pycache__" ]; then
  # Control will enter here if $DIRECTORY exists.
  rm -rf __pycache__
fi
python -m py_compile autosign.py
mv -f __pycache__/* /usr/sbin/autosign.pyc
cp autosign.service /lib/systemd/system/
systemctl enable autosign.service --now
systemctl daemon-reload
rm -rf __pycache__