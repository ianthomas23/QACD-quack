# Generates .py files from .ui (Qt Designer) files.  Only generates those files
# that need to be updated, unless 'force' command line argument is specified.

import glob
import os
import subprocess
import sys


force_all = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'force':
        force_all = True
        print('Forcing all files to be updated')
    else:
        raise "The only valid command line argument is 'force'"


for ui_file in glob.glob('resources/*.ui'):
    basename = os.path.basename(ui_file)
    target_file = os.path.join('gui', os.path.splitext(basename)[0] + '.py')

    recreate = (force_all or not os.path.exists(target_file) or
                os.path.getmtime(ui_file) > os.path.getmtime(target_file))

    if recreate:
        print('Recreating {}'.format(target_file))
        cmd_list = ['pyuic5', '-x', ui_file, '-o', target_file]
        subprocess.call(cmd_list)
    else:
        print('{} is up to date'.format(target_file))
