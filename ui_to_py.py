import os
import subprocess


ui_files = [
    'About_Dialog.ui',
    #'Edit_Dialog.ui',
    #'Figure_Dialog.ui',
    #'K_dialog.ui',
    #'PhClust_Dialog.ui',
    #'Clust_Dialog.ui',
    #'Export_Dialog.ui',
    #'Import_Dialog.ui',
    #'MainWindow.ui',
    #'Ratio_Dialog.ui',
    ]
force_all = True


for ui_file in ui_files:
    target_file = os.path.splitext(ui_file)[0] + '_gen.py'

    recreate = (force_all or not os.path.exists(target_file) or
                os.path.getmtime(ui_file) > os.path.getmtime(target_file))

    if recreate:
        print('Recreating {}'.format(target_file))
        cmd_list = ['pyuic4', '-o', target_file, ui_file]
        print(' '.join(cmd_list))
        subprocess.call(cmd_list)
    else:
        print('{} is up to date'.format(target_file))
