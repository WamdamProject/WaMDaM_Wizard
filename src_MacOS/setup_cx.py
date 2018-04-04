import sys, os
from cx_Freeze import setup, Executable

# Build tree of files given a dir (for appending to py2exe data_files)
# Taken from http://osdir.com/ml/python.py2exe/2006-02/msg00085.html

includes = ['sys', "sqlalchemy"]
excludes = []
packages = ["sqlalchemy"]
path = []
build_exe_options = {
    # 'icon'    : "WaMDaM_Wizard.ico",
    'includes': includes,
    'excludes': excludes,
    'packages': packages,
    'path'    : path,
    'include_msvcr': True,
    'include_files': [],
}

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "WaMDaM",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]wamdam.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
setup(
    name="WaMDaM_Main_Setup",
    version="1.0.0",
    description="",
    options={'build_exe': build_exe_options, 'bdist_msi': bdist_msi_options},
    executables=[Executable("wamdam.py", base=base, icon="WaMDaM_Wizard.ico")]
)
