if (( $EUID != 0 )); then
    echo "Please run as root."
    exit
fi
systemctl disable autosign.service
systemctl daemon-reload
rm -rf /lib/systemd/system/autosign.service
rm -rf /usr/sbin/autosign.pyc