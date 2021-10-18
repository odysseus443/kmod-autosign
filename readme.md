# kmod_autosigner
- Created by Meghadeep Roy Chowdhury 4/14/2021
- All rights reserved under GNU AGPLv3
- details: https://www.gnu.org/licenses/agpl-3.0.en.html
- Modified by odysseus443

# Installation:
- `sudo chmod +x setup.sh`
- `sudo ./setup.sh`

# Explaination
- By running `setup.sh`, you `autosign.py` will be copied into `/sbin/` and `autosign.service` will be copied into `/lib/systemd/system/`.
- The bash script will also reload the systemctl daemons and enable the service automatically.