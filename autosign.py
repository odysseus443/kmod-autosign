# Created by Meghadeep Roy Chowdhury 4/14/2021
# All rights reserved under GNU AGPLv3
# details: https://www.gnu.org/licenses/agpl-3.0.en.html
# Modified by odysseus443

# Kernel sign script path
sign_script_path = '/usr/src/kernels/{uname_release}/scripts/sign-file'
# Common kernel path
path_common = '/lib/modules/'
# main.py directory path
main_path = '/var/log/autosign/autosign.py'

# Do not change below this line #

import os
import datetime


class MOKKeyError(Exception):
	""" Machine Owner Key not found in the keys directory """
	pass


class SignError(Exception):
	""" Error while signing the kernel modules """
	pass

_date = datetime.datetime.now().strftime("%Y%m%d")

def main():
	global sign_script_path
	# Get current kernel info
	kernel_current = os.uname().release

	# Get list of kernels
	kernels_present = [f.name for f in os.scandir(path_common) if f.is_dir()]
	# Sort kernels alphabetically
	kernels_present.sort()
	# Only need to proceed if there's been a kernel update
	if (kernel_current != kernels_present[-1]):
		kernel_updated = kernels_present[-1]
		print('Updated kernel found: ' + kernel_updated)
		kernel_path = path_common + kernel_updated + '/'
		module_path = kernel_path + 'extra'
		kernel_modules = []
		for root, dirs, files in os.walk(module_path):
			for file in files:
				kernel_modules.append(os.path.join(root, file))
		# Check if keys exist
		keys = [f.name for f in os.scandir('/etc/pki/tls/mok/') if f.is_file()]
		if ('mok.key' in keys) and ('mok.der' in keys):
			print('Keys found in keys directory.')
			public_key = '/etc/pki/tls/mok/mok.der'
			private_key = '/etc/pki/tls/mok/mok.key'
			sign_script_path = sign_script_path.format(uname_release=kernel_updated)
			for i in kernel_modules:
				print('Signing ' + i)
				run_script = sign_script_path + ' sha256 ' + private_key + ' ' + public_key + ' ' + i
				try:
					os.system(run_script)
					print('Signed ' + i)
					with open(f'/var/log/autosigner-{_date}.log', 'a+') as f:
						f.write('Signed ' + i + '\n')
				except Exception as e:
					print('FAILURE: ' + i)
					print(e)
					with open(f'/var/log/autosigner-{_date}.log', 'a+') as f:
						f.write(e + '\n')
						f.write(datetime.datetime.now().strftime('%c') + '\n')
					raise SignError
		else:
			print('Keys NOT FOUND')
			with open(f'/var/log/autosigner-{_date}.log', 'a+') as f:
				f.write('Keys NOT FOUND. ' + datetime.datetime.now().strftime('%c') + '\n')
			raise MOKKeyError
	else:
		print('Kernel not updated, signing new kernels not required.')
		with open(f'/var/log/autosigner-{_date}.log', 'a+') as f:
			f.write('Kernel not updated, signing new kernels not required. ' + datetime.datetime.now().strftime('%c') + '\n')


if __name__ == '__main__':
	with open(f'/var/log/autosigner-{_date}.log', 'a+') as f:
		f.write('Service ran at ' + datetime.datetime.now().strftime('%c') + '\n')

	main()
