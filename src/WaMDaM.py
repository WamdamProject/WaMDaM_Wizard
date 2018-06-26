#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# Wamdam.py
""""""

"""
WaMDaM: The Water Management Data Model Version 1.02 
See the schema at http://schema.wamdam.org/diagrams/01_WaMDaM.html
Instructions at http://docs.wamdam.org/Getting_started/Steps

Adel M. Abdallah
email: amabdallah@aggiemail.usu.edu
website: http://adelmabdallah.com/

June 2018
"""


"""
Wamdam.py is the calling/initializing function for the Wizard. 

Before you start, make sure to install all the required Python libraries listed in 
requirements.md text file/


Wamdam.py calls the GUI homepage wxform in the viewer folder which calls frm_Home.py. In the GUI homepage,
users can mainly connect to a WaMDaM SQLite database and import data from multiple sources
into the database using interactive buttons (events: 
1. WaMDaM spreadsheet template (generic to any dataset or model)  
2. Time series data from the WaterOneFlow Web Services by CUAHSI-HIS
3. Water use data from the Water Data Exchange (WaDE) portal by the Western States Water Council
4. Time-series water data form the Reclamation Water Information System (RWIS)

When a user clicks at a button in the GUI, the homepage frm_Home.py calls the
corresponding specific dialog box from the viewer folder for that button. Then buttons in
the dialog box call another dialog box and then its python function that exist in the controller
folder. For example, clicking at the button "From Excel" under the GUI homepage tab
"Import Data into WaMDaM" calls the form or dialog box called
dlg_ImportSpreadsheetBasic.py which exist in the viewer Folder. Then when the user
clicks at "load Data" in this dialog box, a function calls one or all the sub-data importers
for the checked boxes from the controller folder: 
stp0_loadCVs.py, stp1_loadMetadata.py,
stp2_loadDataStructure.py,
stp3_loadNetworks.py,
and stp4_loadDataValues.py

stp0_loadCVs.py, load_step_1.py, load_step_2.py, load_step_3.py, stp4_loadDataValues.py
It's important to note that the controlled vocabulary (CV) data in the stp0_loadCVs.py
are called from the online registry http://vocabulary.wamdam.org/
while the data for the rest of the steps are obtained form the provided spreadsheet template or other source of data.

The Wizard implements dozens of validations and checks on the imported data
to make sure it complies with WaMDaM business rules

The Wizard either loads all the dataset and it's metadata etc or nothing.

See the software architecture in a flowchart @ https://github.com/WamdamProject/WaMDaM_Wizard
"""

import wx, os


class pyWamdam(wx.App):

    def OnInit(self):

        self.Start()
        return True

    def Start(self):
        import viewer.frm_Home as fMain
        mn = fMain.frm_Home(None)

        mn.Show()

    def OnExit(self):
        wx.App.ExitMainLoop(self)

def main():
    application = pyWamdam()
    application.MainLoop()

if __name__ == '__main__':
    main()
