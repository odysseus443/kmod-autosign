# kmod_autosigner
- Created by Meghadeep Roy Chowdhury 4/14/2021
- All rights reserved under GNU AGPLv3
- details: https://www.gnu.org/licenses/agpl-3.0.en.html
- Modified by odysseus443

## Supporting Software:
VMware, VirtualBox, Nvidia driver and any `kmod` that sits at `/lib/modules/{uname_release}/extra` and `/lib/modules/{uname_release}/misc` are automatically signed.

## Prerequisites:

**Creating the directory for soring the key**
-  `sudo mkdir /etc/pki/tls/mok`
-  `cd /etc/pki/tls/mok`

**Generating the key**
-  `sudo openssl req -new -x509 -newkey rsa:2048 -keyout mok.key -outform DER -out mok.der -nodes -days 36500 -subj "/CN=Descriptive name/"`

**Importing the key to the motherboard**
-  `sudo mokutil --import mok.der`

## Installation:
- `sudo chmod +x setup.sh`
- `sudo ./setup.sh`

## Notice:
If it doesn't work, please remove `/etc/autosign.conf` and reboot.

## Log:
The logs are at `/var/log/autosign.log`
Or using `journalctl -u autosign.service`

## Explaination:
- By running `setup.sh`, your `autosign.py` will be compiled into `pyc` and copied to `/usr/sbin/` and `autosign.service` will also be copied to `/lib/systemd/system/autosign.service`.
- The bash script will also reload the systemctl daemons and enable the service automatically.
