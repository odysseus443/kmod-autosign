# Created by Meghadeep Roy Chowdhury 4/14/2021
# All rights reserved under GNU AGPLv3
# details: https://www.gnu.org/licenses/agpl-3.0.en.html
# Modified by odysseus443

import os
import datetime

# Kernel sign script path
# Common kernel path
path_common = '/lib/modules/'
# Key location
public_key = '/etc/pki/tls/mok/mok.der'
private_key = '/etc/pki/tls/mok/mok.key'


_date = datetime.datetime.now().strftime("%Y%m%d")

class MOKKeyError(Exception):
	""" Machine Owner Key not found in the keys directory """
	pass


class SignError(Exception):
	""" Error while signing the kernel modules """
	pass


def sign(kernel_modules, kernel):
	for i in kernel_modules:
		print('Signing ' + i)
		sign_script_path = '/usr/src/kernels/{uname_release}/scripts/sign-file'
		sign_script_path = sign_script_path.format(uname_release=kernel)
		run_script = sign_script_path + ' sha256 ' + private_key + ' ' + public_key + ' ' + i
		try:
			os.system(run_script)
			print('Signed ' + i)
			with open(f'/var/log/autosigner.log', 'a+') as f:
				f.write('Signed ' + i + '\n')
		except Exception as e:
			print('FAILURE: ' + i)
			print(e)
			with open(f'/var/log/autosigner.log', 'a+') as f:
				f.write(e + '\n')
				f.write(datetime.datetime.now().strftime('%c') + '\n')
			raise SignError

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
	kernel_modules = []
	added_modules = []
	with open('/etc/autosign.conf', 'a+') as f:
		config = f.readlines()
	kernel_modules_check = [i.replace('\n','') for i in config]
	for root, dirs, files in os.walk(module_path):
		for file in files:
			kernel_modules.append(os.path.join(root, file))
	if kernel_modules_check != kernel_modules:
		with open ('/etc/autosign.conf', 'a+') as fnew:
			for i in kernel_modules:
				if i not in kernel_modules_check and i != '':
					fnew.write(f'\n{i}')
					added_modules.append(i)
		with open(f'/var/log/autosigner.log', 'a+') as f:
			for i in added_modules:
				f.write(f'Found added module: {i}' + datetime.datetime.now().strftime('%c') + '\n')
		sign(added_modules, kernel_updated)
		return
	elif kernel_current != kernels_present[-1]:
		# Check if keys exist
		keys = [f.name for f in os.scandir('/etc/pki/tls/mok/') if f.is_file()]
		if ('mok.key' in keys) and ('mok.der' in keys):
			sign(kernel_modules, kernel_updated)
		else:
			print('Keys NOT FOUND')
			with open(f'/var/log/autosigner.log', 'a+') as f:
				f.write('Keys NOT FOUND. ' + datetime.datetime.now().strftime('%c') + '\n')
			raise MOKKeyError
		return
	else:
		print('Kernel not updated, signing new kernels not required.')
		with open(f'/var/log/autosigner.log', 'a+') as f:
			f.write('Kernel not updated, signing new kernels not required. ' + datetime.datetime.now().strftime('%c') + '\n')
		return


if __name__ == '__main__':
	with open(f'/var/log/autosigner.log', 'a+') as f:
		f.write('Service ran at ' + datetime.datetime.now().strftime('%c') + '\n')

	main()
