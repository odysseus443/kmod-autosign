# kmod_autosigner
- Created by Meghadeep Roy Chowdhury 4/14/2021
- All rights reserved under GNU AGPLv3
- details: https://www.gnu.org/licenses/agpl-3.0.en.html
- Modified by odysseus443

# Prerequisite:
  Install Nvidia drvier.

  Create signing keys
-  `sudo mkdir /etc/pki/tls/mok`
-  `cd /etc/pki/tls/mok`
-  `openssl req -new -x509 -newkey rsa:2048 -keyout mok.key -outform DER -out mok.der -nodes -days 36500 -subj "/CN=Descriptive name/"`
  
# Notice
  After the script installed it might not work immediately, please use script from this link: https://www.reddit.com/r/Fedora/comments/ktxulg/comment/gitx76s/?utm_source=share&utm_medium=web2x&context=3 to sign the kernel first since there might not be a newer kernel version for the program to detect and the program will think the kernel is not updated so it will not run the signing process.

# Installation:
- `sudo chmod +x setup.sh`
- `sudo ./setup.sh`

# Explaination:
- By running `setup.sh`, you `autosign.py` will be copied into `/sbin/` and `autosign.service` will be copied into `/lib/systemd/system/`.
- The bash script will also reload the systemctl daemons and enable the service automatically.
