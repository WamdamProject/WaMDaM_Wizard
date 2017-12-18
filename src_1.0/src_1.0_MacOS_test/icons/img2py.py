
"""This module contains a simple function to encode any number of
bitmap files to a .py file

It works independently from the WaMDaM Wizard. So it's run just once to create 
the icons.py. Then it is not used, unless the user wants to add a new icon. 
Then they need to run it again to generate the bitmap of the new icon.

"""

import glob
import os
import re

import wx
from wx.tools import img2py

output = 'icons1.py'

# get the list of BMP files
#files = [f for f in os.listdir('.') if re.search(r'odm\d*x\d*\.png', f)]
#files = [f for f in os.listdir('.') if re.search('gtk-execute', f)]
files = glob.glob('*.png') #TODO: chose your extension here ........... (icons_png/)

open(output, 'w')

# call img2py on each file
for file in files:
    print "files: ", file


    # extract the basename to be used as the image name
    name = os.path.splitext(os.path.basename(file))[0]

    # encode it
    if file == files[0]:
        cmd = "-u -i -n %s %s %s" % (name, file, output)
    else:
        cmd = "-a -u -i -n %s %s %s" % (name, file, output)
    img2py.main(cmd.split())
