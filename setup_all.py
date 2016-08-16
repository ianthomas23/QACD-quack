#setup_all.py
import sys
from distutils.core import setup
import py2exe

sys.path.append("C:\Program Files (x86)\Google\\Drive\Microsoft.VC90.CRT")

from glob import glob
data_files = [("Microsoft.VC90.CRT",
              glob(r'C:\Program Files (x86)\Google\Drive\Microsoft.VC90.CRT\*.*'))]
                                        

setup(data_files=data_files,
      windows=['Main.py'])
