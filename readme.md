# kmod_autosigner
- Created by Meghadeep Roy Chowdhury 4/14/2021
- All rights reserved under GNU AGPLv3
- details: https://www.gnu.org/licenses/agpl-3.0.en.html
- Modified by odysseus443

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

## Log:
The logs are at `/var/log/autosigner.log`

## Notice
The service should be working immediately if `/etc/autosign.conf` does not exist the script will treat all the present modules as new modules and sign the kernel recordingly, if there is a newer kernel present it will sign the newest one, otherwise it will sign the current kernel. 

## Explaination:
- By running `setup.sh`, you `autosign.py` will be copied into `/sbin/` and `autosign.service` will be copied into `/lib/systemd/system/`.
- The bash script will also reload the systemctl daemons and enable the service automatically.
