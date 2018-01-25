import os
import sys
import subprocess
from optparse import OptionParser
from datetime import datetime

def main():
    parser = OptionParser()

    parser.add_option('-u', '--username', dest='username',
                      help="Specify Your username'.")

    parser.add_option('-p','--password', dest='password',
                      help="Specify Your password'.")
    (options, args) = parser.parse_args()
    print (options.username)
    print (options.password)
	os.chdir('/home/odoo/Desktop/odoo10git')
	# os.system('git init')
	# os.system('git remote add origin https://github.com/khyasir/odoo-10.git')
	# os.system('git add *')
	# os.system('git status')
	# os.system('git commit -m "this is your comment"')
	# master='git push origin master'
	# p = os.system('echo %s| sudo -S %s' % (username, master))
	# os.system('git push origin master')
	os.system('echo %s' % (master))
	# username='khyasir'
	# password='yasir43'
	# # Wait for 5 seconds
	# time.sleep(10)
	# os.system('echo %s' % (username))
	# time.sleep(10)
	# os.system('echo %s' % (password))

if __name__ == '__main__':
    main()