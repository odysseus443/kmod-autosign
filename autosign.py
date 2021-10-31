# Created by Meghadeep Roy Chowdhury 4/14/2021
# All rights reserved under GNU AGPLv3
# details: https://www.gnu.org/licenses/agpl-3.0.en.html
# Modified by odysseus443

from genericpath import isfile
import os
import time
import logging
from systemd.journal import JournalHandler

# Common kernel path
path_common = '/lib/modules/'


# Key location
public_key = '/etc/pki/tls/mok/mok.der'
private_key = '/etc/pki/tls/mok/mok.key'
mok_dir = '/etc/pki/tls/mok/'


# Logging
logger = logging.getLogger('autosign')
logger.setLevel(logging.INFO)
journald_handler = JournalHandler()
journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
journald_handler.setLevel(level=logging.INFO)
logger.addHandler(journald_handler)
file_handler = logging.FileHandler('/var/log/autosign.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%b %d %H:%M:%S"))
file_handler.setLevel(level=logging.INFO)
logger.addHandler(file_handler)


# Time
_unixTimeNow = int(time.time())


def sign(kernel_modules, kernel):
	for i in kernel_modules:
		logger.info('Signing ' + i.split('/')[3] + ' ' + i.split('/')[-1])
		sign_script_path = f'/usr/src/kernels/{kernel}/scripts/sign-file'
		run_script = sign_script_path + ' sha256 ' + private_key + ' ' + public_key + ' ' + i
		try:
			os.system(run_script)
			logger.info('Signed ' + i.split('/')[3] + ' ' + i.split('/')[-1])
		except Exception as e:
			logger.error(str(e))
			return


def main():
	# Get current kernel info
	kernel_current = os.uname().release
	# Get list of kernels
	kernels_present = [f.name for f in os.scandir(path_common) if f.is_dir()]
	# Sort kernels alphabetically
	kernels_present.sort()
	# Only need to proceed if there's been a kernel update
	kernel_updated = kernels_present[-1]
	kernel_path = [path_common + f + '/' for f in kernels_present]
	module_path = [f + 'extra/' for f in kernel_path]
	module_misc = [f + 'misc/' for f in kernel_path]
	kernel_modules = []
	added_modules = []
	module_updated = []
	if os.path.isfile('/etc/autosign.conf'):
		with open('/etc/autosign.conf', 'r') as f:
			config = f.readlines()
	else:
		config = []
	kernel_modules_check = [i.replace('\n','') for i in config]
	for i in module_path:
		for root, dirs, files in os.walk(i):
			for file in files:
				kernel_modules.append(os.path.join(root, file))
	for i in module_misc:
		for root, dirs, files in os.walk(i):
			for file in files:
				kernel_modules.append(os.path.join(root, file))
	for i in kernel_modules:
		calc = _unixTimeNow - int(os.path.getctime(i))
		if calc < 600:
			module_updated.append(i)
	if not os.path.isfile(public_key) and os.path.isfile(private_key):
		logger.error('Keys NOT FOUND')
		return
	if kernel_modules_check != kernel_modules or module_updated != []:
		with open ('/etc/autosign.conf', 'w') as fnew:
			for i in kernel_modules:
				fnew.write(f'{i}\n')
				if i not in kernel_modules_check:
					added_modules.append(i)
					module_updated.append(i)
		if module_updated != [] or added_modules != []:
			for i in module_updated:
				item = i.split('/')[3] + ' ' + i.split('/')[-1]
				if i not in added_modules:
					logger.info(f'Found updated module: {item}')
			for i in added_modules:
				item = i.split('/')[3] + ' ' + i.split('/')[-1]
				if i not in module_updated:
					logger.info(f'Found added module: {item}')
		else:
			logger.info('No updates, signing new kernels not required.')
			return
		if kernel_current != kernel_updated:
			sign([i for i in kernel_modules if kernel_updated in i], kernel_updated)
		elif len(added_modules) > 0:
			sign([i for i in added_modules if kernel_updated in i], kernel_updated)
			sign([i for i in added_modules if kernel_current in i], kernel_current)
			return
		elif len(module_updated) > 0:
			if kernel_current != kernel_updated:
				sign([i for i in module_updated if kernel_updated in i], kernel_updated)
				return
			else:
				sign([i for i in module_updated if kernel_current in i], kernel_current)
				return
	elif kernel_current != kernel_updated:
		sign([i for i in kernel_modules if kernel_updated in i], kernel_updated)
		return
	else:
		logger.info('No updates, signing new kernels not required.')
		return


if __name__ == '__main__':
	logger.info('Service started')
	main()
