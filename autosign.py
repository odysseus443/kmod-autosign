# Created by Meghadeep Roy Chowdhury 4/14/2021
# All rights reserved under GNU AGPLv3
# details: https://www.gnu.org/licenses/agpl-3.0.en.html
# Modified by odysseus443

from genericpath import isfile
import os
import datetime
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
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
file_handler.setLevel(level=logging.INFO)
logger.addHandler(file_handler)


# Time
_date = datetime.datetime.now().strftime("%Y%m%d")
_unixTimeNow = int(time.time())

def sign(kernel_modules, kernel):
	for i in kernel_modules:
		logger.info('Signing ' + i.split('/')[-1])
		sign_script_path = '/usr/src/kernels/{uname_release}/scripts/sign-file'
		sign_script_path = sign_script_path.format(uname_release=kernel)
		run_script = sign_script_path + ' sha256 ' + private_key + ' ' + public_key + ' ' + i
		try:
			os.system(run_script)
			logger.info('Signed ' + i.split('/')[-2] + i.split('/')[-1])
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
	kernel_path = path_common + kernel_updated + '/'
	module_path = kernel_path + 'extra'
	module_misc = kernel_path + 'misc'
	kernel_modules = []
	added_modules = []
	module_updated = []
	if os.path.isfile('/etc/autosign.conf'):
		with open('/etc/autosign.conf', 'r') as f:
			config = f.readlines()
	else:
		config = []
	kernel_modules_check = [i.replace('\n','') for i in config]
	for root, dirs, files in os.walk(module_path):
		for file in files:
			kernel_modules.append(os.path.join(root, file))
	for root, dirs, files in os.walk(module_misc):
		for file in files:
			kernel_modules.append(os.path.join(root, file))
	for i in kernel_modules:
		calc = _unixTimeNow - int(os.path.getctime(i))
		if calc < 600:
			module_updated.append(i)
	if not os.path.isfile(public_key) and os.path.isfile(private_key):
		logger.error('Keys NOT FOUND')
		return
	if kernel_modules_check != kernel_modules or len(module_updated) > 0:
		with open ('/etc/autosign.conf', 'a+') as fnew:
			for i in kernel_modules:
				if i not in kernel_modules_check:
					fnew.write(f'{i}\n')
					added_modules.append(i)
		with open ('/etc/autosign.conf', 'r') as rm_lst:
			newlist = [i.replace('\n', '') for i in rm_lst.readlines()]
			for i in newlist:
				if i not in kernel_modules:
					newlist.remove(i)
		if newlist != []:
			with open ('/etc/autosign.conf', 'w') as rm:
				for i in newlist:
					rm.write(f'{i}\n')
		for i in module_updated:
			item = i.split('/')[-1]
			if i in added_modules:
				logger.info(f'Found added module: {item}')
			else:
				logger.info(f'Found updated module: {item}')
		if kernel_current != kernel_updated:
			sign(kernel_modules, kernel_updated)
		elif len(added_modules) > 0:
			if kernel_current != kernel_updated:
				sign(added_modules, kernel_current)
				return
			else:
				sign(added_modules, kernel_current)
				return
		elif len(module_updated) > 0:
			if kernel_current != kernel_updated:
				sign(module_updated, kernel_updated)
				return
			else:
				sign(module_updated, kernel_current)
				return
	elif kernel_current != kernel_updated:
		sign(kernel_modules, kernel_updated)
		return
	else:
		logger.info('No updates, signing new kernels not required.')
		return


if __name__ == '__main__':
	logger.info('Service started')
	main()
