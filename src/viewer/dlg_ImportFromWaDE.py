"""Subclass of dlg_ImportFromWaDE, which is generated by wxFormBuilder."""

import wx
import WaMDaMWizard
import urllib2, define, threading
import xml.etree.ElementTree as ET
from Messages_forms.msg_somethigWrong import msg_somethigWrong
from controller.ConnectDB_ParseExcel import DB_Setup

from controller.WaDE_importer import WaDE_importer

# Implementing dlg_ImportFromWaDE
class dlg_ImportFromWaDE( WaMDaMWizard.dlg_ImportFromWaDE ):
    def __init__( self, parent ):
        WaMDaMWizard.dlg_ImportFromWaDE.__init__( self, parent )
        self.stateList = ["Utah", "Wyoming"]
        self.comboBox_State.SetItems(self.stateList)
        self.utah = {}
        self.year_utah_name = {}
        self.data_xml = []
        url = 'https://water.utah.gov/DWRE/WADE/v0.2/GetCatalog/GetCatalog_GetAll.php?orgid=utwre'
        try:
            # Load data from specific urls
            url = 'https://water.utah.gov/DWRE/WADE/v0.2/GetCatalog/GetCatalog_GetAll.php?orgid=utwre'
            # url = 'https://water.utah.gov/DWRE/WADE/v0.2/GetMethod/GetMethod.php?'
            response = urllib2.urlopen(url)
            tree = ET.parse(response)
            root = tree.getroot()
            self.ReportingUnitName_utah = list()
            self.year_utah= list()
            for elem in root:
                self.utah[elem[6].text] = elem[7].text
                # self.ReportingUnitName_utah.append(elem[7].text)
                if not elem[7].text in self.ReportingUnitName_utah:
                    self.ReportingUnitName_utah.append(elem[7].text)
                yearVal = elem[2].text.split("_")[0]
                if not yearVal in self.year_utah:
                    self.year_utah.append(yearVal)
                    self.year_utah_name.__setitem__(yearVal, elem[2].text)
            self.ReportingUnitName_utah.sort()

            self.wywdc = {}
            url = 'http://www.westernstateswater.org/Wyoming/WADE/v0.2/GetCatalog/GetCatalog_GetAll.php?orgid=WYWDC'
            response = urllib2.urlopen(url)
            tree = ET.parse(response)
            root = tree.getroot()
            self.ReportingUnitName_wywdc = list()
            self.year_wywdc= list()
            for elem in root:
                self.wywdc[elem[6].text] = elem[7].text
                # self.ReportingUnitName_wywdc.append(elem[6].text)
                if not elem[7].text in self.ReportingUnitName_wywdc:
                    self.ReportingUnitName_wywdc.append(elem[7].text)
                if not elem[2].text in self.year_wywdc:
                    self.year_wywdc.append(elem[2].text)
            self.ReportingUnitName_wywdc.sort()

            self.btn_Load.Enabled = False

        except Exception as e:
            raise Exception(e.message)

    # Handlers for dlg_ImportFromWaDE events.
    def btn_RetrieveDataOnButtonClick( self, event ):
        # TODO: Implement btn_RetrieveDataOnButtonClick

        validation_check = self.check_validation()
        if not validation_check:
            return

        strBasin = self.get_identifier_by_selected_name(self.comboBox_State.Value)
        url = ''
        begining_year = int(self.comboBox_year1.Value)
        end_year = int(self.comboBox_year2.Value)
        # Get data by year value
        for i in range(end_year - begining_year + 1):
            year_value_str = str(begining_year + i)

            if (self.comboBox_State.Value == self.stateList[0]):
                url = 'https://water.utah.gov/DWRE/WADE/v0.2/GetSummary/GetSummary.php?loctype=REPORTUNIT&loctxt=' \
                      + strBasin + '&orgid=utwre&reportid=' + self.year_utah_name[year_value_str] +'&datatype=USE'
            else:
                url = 'http://www.westernstateswater.org/Wyoming/WADE/v0.2/GetSummary/GetSummary.php?loctype=REPORTUNIT&loctxt=' \
                  + strBasin+ '&orgid=WYWDC&reportid='\
                  + year_value_str + '&datatype=USE'
            response = urllib2.urlopen(url)
            print response
            tree = ET.parse(response)
            root = tree.getroot()
            xmlstr = ET.tostring(root, encoding='utf8', method='xml')
            self.data_xml.append(xmlstr)
            print xmlstr
        if self.data_xml.__len__() > 0:
            self.btn_Load.Enabled = True
        # root = tree.getroot()
        # for item in root:
        # 	print item

    def btn_LoadOnButtonClick( self, event ):
        # TODO: Implement btn_LoadOnButtonClick
        validation_check = self.check_validation()
        if not validation_check:
            return
    # Check whether WaDE data to load
        if self.data_xml.__len__() <= 0:
            from viewer.Messages_forms.generalMsgDlg import messageDlg
            msg = "Warning!\n'Please click at the 'Retrieve Data' button."
            instance = messageDlg(None)
            instance.setMessage(msg)
            instance.ShowModal()
            instance.Destroy()
            return False
    #///////////////////////////////////////////////////////////////////////#
        self.btn_RetrieveData.Enabled = False
        self.btn_Load.Enabled = False

    # Show a msg to tell the user to wait.
        from viewer.Messages_forms.generalMsgDlg import messageDlg
        self.waiting_dlg = messageDlg(None)
        self.waiting_dlg.btn_OK.Shown = False
        self.waiting_dlg.Title = "Loading Data..."
        self.waiting_dlg.setMessage("Please wait for Wizard to call and retrieve WaDE portal.\n It might take seconds to several minutes depending on the \n\tsize of the data")
        self.waiting_dlg.Show()
    #///////////////////////////////////////////////////////////////////////#

    # Start thread to load data
        our_thread = threading.Thread(None, self.load_data)
        our_thread.start()
    #///////////////////////////////////////////////////////////////////////#

    def load_data(self):
    # Add WaDE data within Sqlite db.
        wade_importer = WaDE_importer()

        while self.data_xml.__len__() > 0:
            xml_data = self.data_xml[0]
            wade_importer.load_data(xml_data, {'State': self.comboBox_State.Value})
            self.data_xml.pop(0)
    #/////////////////////////////////////////////////////////////#
    # Once our_thread is done, allone method is called
        wx.CallAfter(self.allDone)
    #///////////////////////////////////////////////////////////////////////#

    def allDone(self):
        self.waiting_dlg.Destroy()

    # Popup success message if loading WaDE data within Sqlite db.
        from Messages_forms.msg_successLoadDatabase import msg_successLoadDatabase
        instance = msg_successLoadDatabase(None)
        instance.setMessageText(u"\n\nYou successfully loaded the WaDE data into " + define.dbName + u". \nYou can view the data by using: SQLite Manager: Add-ons for\nFirefox web browser")
        instance.ShowModal()
        instance.Destroy()
    #/////////////////////////////////////////////////////////////#
        self.btn_RetrieveData.Enabled = True


    def btn_cancelOnButtonClick( self, event ):
        # TODO: Implement btn_cancelOnButtonClick
        self.Close();
    def comboBox_stateOnCombobox(self, event):
        if (self.comboBox_State.Value == self.stateList[0]):
            self.comboBox_PlanningBasin.SetItems(self.ReportingUnitName_utah)
            self.comboBox_year1.SetItems(self.year_utah)
            self.comboBox_year1.SetValue(min(self.year_utah))
            self.comboBox_year2.SetItems(self.year_utah)
            self.comboBox_year2.SetValue(max(self.year_utah))
        else:
            self.comboBox_PlanningBasin.SetItems(self.ReportingUnitName_wywdc)
            self.comboBox_year1.SetItems(self.year_wywdc)
            self.comboBox_year1.SetValue(min(self.year_wywdc))
            self.comboBox_year2.SetItems(self.year_wywdc)
            self.comboBox_year2.SetValue(max(self.year_wywdc))
        self.Show()

    def check_validation(self):
    # Check whether user select needed items correctly
        from viewer.Messages_forms.generalMsgDlg import messageDlg
        msg = ""
        if self.comboBox_State.Value == None or self.comboBox_State.Value == "":
            msg = "Warning!\n'State' field can not be empty. Please select a state."
        elif self.comboBox_PlanningBasin.Value == None or self.comboBox_PlanningBasin.Value == "":
            msg = "Warning!\n'Planing Basin' field can not be empty. Please select a planing basin."
        elif self.comboBox_year1.Value == None or self.comboBox_year1.Value == "":
            msg = "Warning!\n'Year' field can not be empty. Please select begining year."
        elif self.comboBox_year2.Value == None or self.comboBox_year2.Value == "":
            msg = "Warning!\n'Year' field can not be empty. Please select end year."
        elif int(self.comboBox_year1.Value) > int(self.comboBox_year2.Value):
            msg = "Warning!\n'End Year' must be more than 'Begining Year'. Please select again."
        if msg != "":
            instance = messageDlg(None)
            instance.setMessage(msg)
            instance.ShowModal()
            instance.Destroy()
            return False
    #///////////////////////////////////////////////////////////////////////#

    # Check whether Sqlite db is connected.
        setup = DB_Setup()
        if not setup.get_session():
            message = msg_somethigWrong(None, msg='\n\n\nError, No Database connection found, Please first connect to a database.')
            message.ShowModal()
            return False
    #///////////////////////////////////////////////////////////////////////#

        return True

    def get_identifier_by_selected_name(self, selected_state):
        if selected_state == "Utah":
            for key in self.utah.keys():
                if self.utah[key] == self.comboBox_PlanningBasin.Value:
                    return key
        elif selected_state == "Wyoming":
            for key in self.wywdc.keys():
                if self.wywdc[key] == self.comboBox_PlanningBasin.Value:
                    return key
        return None

