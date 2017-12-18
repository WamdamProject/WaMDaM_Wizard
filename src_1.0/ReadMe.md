# Create an executable the WaMDaM Wizard (.exe) for windows
 
1. In the CDM terminal, navigate to directory where wamdam.py exist in your pc.   
You need to have pyinstaller python package on your machine.  
You can do so  
```pip install pyinstaller```

2. Execute the following command in the cmd.exe 

``` pyinstaller --clean --icon=WaMDaM_Wizard.ico --onedir --noconfirm --noupx --onefile --windowed wamdam.py```

The image called "WaMDaM_Wizard.ico" will be used as icon for the executable. The image (icon) is free/open source

# Create a msi installer for Windows

In the terminal, navigate to the directory where wamdam.py exists. Run this command:   
```python setup_cx.py bdist_msi```


Before that, make sure you have all the wamdam needed libraries are installed. Besides those libraries, you need to have these libraries below. For some reason I need to follow the steps below to install the libraries, the hard way.

1. Download this folder [site-packages](https://github.com/amabdallah/draftWaMDaM/blob/master/site-packages.zip)

Unzip it and copy the four unzipped folders:cx_Freeze, cx_Freeze-5.0.2.dist-info, suds, and suds-0.4-py2.7.egg-info
directly into the directory below: 
C:\Users\Adel\AppData\Roaming\Python\Python27\site-packages    # change "Adel" to the user name on your machine

2. Note that the cx_Freeze folder has a file called hooks.py that needs to update its path to where the sqlite3.dll file exist on your machine.
Navigate to the cx_Freeze folder like the path below, open the hooks.py file in any text editor. 
C:\Users\Adel\AppData\Roaming\Python\Python27\site-packages\cx_Freeze

At the bottom on the file, replace the existing path underlined in red as shown in the screenshot below. To find where the path exist to your sqlite3.dll file, navigate to this path and find 
C:\Users\Adel\AppData\Roaming\pyinstaller\bincache00_py27_64bits
![](https://github.com/amabdallah/draftWaMDaM/blob/master/SqliteDDL_hooks_path.PNG)
