# WaMDaM_Wizard V 1.03
WaMDaM Wizard is a desktop data loader from a spreadsheet template to a SQLite database. The SQLite database is built based on a data model called WaMDaM. The data model is designed to organize and integrate different water management datasets.
Here is the schema that the Wizard works within: [WaMDaM Schema](https://wamdamproject.github.io/WaMDaM_Information_Model/diagrams/01_WaMDaM.html)  

The Wizard is built using Python 2.7 and the [wxPython](https://www.wxpython.org/) GUI library with the help of [wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder).  

# Instructions to use WaMDaM software  
The Wizard also provides modelers with automated detailed and summary comparisons of network topology, metadata, and data between Scenarios in the same master network. 
https://github.com/WamdamProject/WaMDaM_Wizard/blob/master/README.md


## [Download the WaMDaM Excel Workbook Templates for Input Data]
1. Excel Workbook template to prepare your data into it. Each dataset into one workbook
https://github.com/WamdamProject/WaMDaM_UseCases/tree/master/0_WorkbookTemplates/InputData_Template

## [Download the Wizard GUI for Windows [7 and 10] 64 bit operating systems]
Download and install the latest release. Choose one of these two options. 
https://github.com/WamdamProject/WaMDaM_Wizard/releases/


* **Windows executable .exe (No-Installer)**
Allows the user to run WaMDaM_Wizard without installing it on your local machine.   
* **[Windows Installer .msi]**

Install on your pc, get an icon shortcut on your desktop and run WaMDaM Wizard As **Admin**  





## Run WaMDaM_Wizard from Source Code 
1. Install the [dependences][7]  
2. Run wamdam.py in the src folder. The connect to an empty SQLite db (it will create a new one for you) 
3. Click at ImportData to WaMDaM tab, and then "From Excel" choose a dataset like: WEAP.xlsm
4. In the view in (3) above, browse for the folder src_v0.1/Test_Data and select the excel file WEAP_April4.xlsm 
the Wizard should load all the data and give you a message of successful loading. You're set now! 

<p align="center">
  <img width="449" height="352" src="/Wizard.PNG">
</p>

[7]:https://github.com/WamdamProject/WaMDaM_Wizard/blob/master/src/requirements.md

## Built With
* Python 2.7 
* wxpython cross-platform GUI toolkit
* sqlAlchemy


## Why WaMDaM Wizard?   
The WaMDaM Wizard is an open-source, cross-platform, Python-based graphical user software to interact with WaMDaM database. By using the Wizard, users are not expected to understand the underlying WaMDaM database of schema. Users just need to understand how to fit their data into these concepts: ObjectType, Attribute, Instance, Network, and Scenario. 
The Wizard mainly allows users to automatically:    
**i)**   Read, validate, and load data from a spreadsheet template in SQLite  
**ii)**  Use data preparation tools to help manipulate and transform users data to fit into the spreadsheet template.  
**iii)** Import data directly from supported web-services (e.g., time series data from CUAHSI)  
**iv)**  Use pre-defined functions to query and compare scenario data from multiple datasets loaded in WaMDaM   
**v)**   Export data loaded into WaMDaM to multiple supported models (in-progress)  


## WaMDaM_Wizard Architecture

WaMDaM Wizard software follows the Model–View–Controller (MVC) architecture. The Model represents the data access layer and the select, update queries to database. The View represents the GUI presentation with buttons and renders the Model data. The Controller represents the business logic that defines the application behavior based on the user interactions in the View layer. Separating the three layers from each other allows for flexibility to update each layer without major changes in the other layers.


**Wamdam.py** is the key calling/initializing function for the Wizard. Before you start, make sure to install all the required Python libraries listed in requirements.md text file/ Wamdam.py calls the GUI homepage wxform in the viewer folder called frm_Home.py. In the GUI homepage, users can mainly connect to a WaMDaM SQLite database and import data from multiple sources into the database using interactive buttons (events):    
**a.** WaMDaM spreadsheet template (generic to any dataset or model)   
**b.** Time series data from the WaterOneFlow Web Services by CUAHSI-HIS   
**c.** Water use data from the Water Data Exchange (WaDE) portal by the Western States Water Council  
**d.** Time-series water data form the Reclamation Water Information System (RWIS)  

When a user clicks at a button in the GUI, the homepage frm_Home.py calls the corresponding specific dialog box from the viewer folder for that button. Then buttons in the dialog box call another dialog box and then its python function that exist in the controller folder. For example, clicking at the button "From Excel" under the GUI homepage tab "Import Data into WaMDaM" calls the form or dialog box called dlg_ImportSpreadsheetBasic.py which exist in the viewer Folder. Then when the user clicks at "load Data" in this dialog box, a function calls one or all the sub-data importers for the checked boxes from the controller folder:   
* stp0_loadCVs.py  
* load_step_1.py  
* load_step_2.py  
* load_step_3.py  
* stp4_loadDataValues.py  
 
It's important to note that the controlled vocabulary (CV) data in the stp0_loadCVs.py are called from the online registry http://vocabulary.wamdam.org/ while the data for the rest of the steps are obtained form the provided spreadsheet template or other source of data. The Wizard implements dozens of validations and checks on the imported data to make sure it complies with WaMDaM business rules The Wizard either loads all the dataset and it's metadata etc or nothing.


<p align="center">
  <img src="/Wizard_flowchart.jpg">
</p>



### Licensing  
WaM-DaM and materials in this GitHub repository are disturbed under a BSD 3-Clause [LICENSE](/LICENSE). 
For alternative licensing arrangements, contact Adel M. Abdallah or David E. Rosenberg directly.    


### Sponsors and Credit  
WaMDaM and related software development have been developed under funding from several different sources. It was primarily supported by the National Science Foundation <a href="http://www.nsf.gov/awardsearch/showAward?AWD_ID=1135482" target="_blank">CI-Water Project</a> and later from the <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=1208732" target="_blank">iUtah Project</a>. 
Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.    

WaMDaM has been developed at and also additionally funded by the Utah Water Research Lab at Utah State University, Logan Utah during the period of August, 2012-2018. Thanks Stephanie Reeder, Larry Kevin, and Kwang Yingjien for their help to design this Wizard and intensively test it. Thanks to Dr. Steven Burian at the University of Utah, Salt Lake City Utah for hosting Adel Abdallah as a visiting scholar 2014-2017 during WaMDaM's development.  
