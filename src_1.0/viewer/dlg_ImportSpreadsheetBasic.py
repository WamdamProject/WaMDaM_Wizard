"""Subclass of dlg_ImportSpreadsheetBasic, which is generated by wxFormBuilder."""

import wx
import WaMDaMWizard
import xlrd as excel
import threading
import time
from controller.stp1_loadMetadata import LoadMetaData
from controller.stp2_loadDataStructure import Load_Struct_To_DB
from controller.stp3_loadNetworks import Load_Networks_Data
from controller.stp0_loadCVs import Load_CV_To_DB
# from controller.stp4_loadDataValues import *
from controller.stp4_loadDataValue import *
from controller.ReadWorkbook_SheetsNames import *
from Messages_forms.msg_somethigWrong import msg_somethigWrong
from Messages_forms.msg_loading import msg_loading
from Messages_forms.msg_loadingToExit import msg_sureToExit

import define
# msgDlg = msg_loading(None)

# Implementing dlg_ImportSpreadsheetBasic
class dlg_ImportSpreadsheetBasic(WaMDaMWizard.dlg_ImportSpreadsheetBasic):
    def __init__(self, parent):
        WaMDaMWizard.dlg_ImportSpreadsheetBasic.__init__(self, parent)
        self.path = None
        self.active = [True, True, True, True]
        self.our_thread = None
        self.selectedExcelFileName = ""
        self.data_pushed_to_db = []

    # Handlers for dlg_ImportSpreadsheetBasic events.
    def FilePicker_SpreadsheetOnFileChanged(self, event):
        valid_extension = ['xlsx','xlsm']
        self.path = self.FilePicker_Spreadsheet.GetPath()
        self.selectedExcelFileName = self.path.split('\\')[-1]

        if not (self.path.split('.')[-1] in valid_extension):
            self.Destroy()
            if define.logger != None:
                define.logger.error("A non excel file was selected, \n\n"
                                                  " Please select a valid Excel File")
            message = msg_somethigWrong(None, msg="A non excel file was selected, \n\n"
                                                  " Please select a valid Excel File")
            message.Show()
        else:
            if define.logger != None:
                define.logger.info("'" + self.selectedExcelFileName + "'was selected.\n")


    def checkBox_CVsOnCheckBox(self, event):
        # TODO: Implement checkBox_CVsOnCheckBox
        pass

    def checkBox_MetadataGOnCheckBox(self, event):
        # TODO: Implement checkBox_MetadataGOnCheckBox
        cb = event.GetEventObject()
        self.active[0] = cb.GetValue()

    def checkBox_DataStructureGOnCheckBox(self, event):
        # TODO: Implement checkBox_DataStructureGOnCheckBox
        cb = event.GetEventObject()
        self.active[1] = cb.GetValue()

    def checkBox_NetworksGOnCheckBox(self, event):
        # TODO: Implement checkBox_NetworksGOnCheckBox
        cb = event.GetEventObject()
        self.active[2] = cb.GetValue()

    def checkBox_DataValuesGOnCheckBox(self, event):
        # TODO: Implement checkBox_DataValuesGOnCheckBox
        cb = event.GetEventObject()
        self.active[3] = cb.GetValue()

    def btn_advancedOnButtonClick(self, event):
        import dlg_ImportSpreadsheetAdvanced as fAdv

        Adv = fAdv.dlg_ImportSpreadsheetAdvanced(None)
        Adv.Show()

    def load_data(self):
        def metaData(msgDlg):
            define.logger.info("Start metaData load.")
            try:
                instance = LoadMetaData(obj)
                instance.load_data()
                msgDlg.guage.SetValue(3)
                define.logger.info("MetaData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed metaData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle("Sorry: something went wrong")
                # message.setMessage('{} \n\n [*] Could not Load MetaData'.format(e))
                # message.Show()
                raise Exception(e.message)

        def cvData(msgDlg):
            define.logger.info("Start cvData load.")
            try:
                instance = Load_CV_To_DB(obj)
                instance.load_data()
                msgDlg.guage.SetValue(2)
                define.logger.info("CvData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed cvData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load DataValues Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def structData(msgDlg):
            define.logger.info("Start structData load.")
            try:
                instance = Load_Struct_To_DB(obj)
                instance.load_data(struct_sheets_ordered)
                msgDlg.guage.SetValue(4)
                define.logger.info("StructData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed structData load.\n' + e.message)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load Structure Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def networksData(msgDlg):
            define.logger.info("Start networksData load.")
            try:
                instance = Load_Networks_Data(obj)
                instance.load_data()
                msgDlg.guage.SetValue(5)
                define.logger.info("NetworksData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed networksData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load Network Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def descriptorValues(msgDlg):
            define.logger.info("Start textFreeData load.")
            try:
                instance = LoadDescriptorValues(obj)
                instance.load_data()
                msgDlg.guage.SetValue(6)
                define.logger.info("TextFreeData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed textFreeData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load TextFree Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def numericValues(msgDlg):
            define.logger.info("Start paramsData load.")
            try:
                instance = LoadNumericValues(obj)
                instance.load_data()
                msgDlg.guage.SetValue(7)
                define.logger.info("ParamsData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed paramsData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load Parameters Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def seasonalNumericValues(msgDlg):
            define.logger.info("Start seasonParamsData load.")
            try:
                instance = LoadSeasonalNumericValues(obj)
                instance.load_data()
                msgDlg.guage.SetValue(8)
                define.logger.info("SeasonParamsData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed seasonParamsData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load SeasonalParameters Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def timeSeriesData(msgDlg):
            define.logger.info("Start timeSeriesData load.")
            try:
                instance = LoadTimeSeries(obj)
                instance.load_data()
                msgDlg.guage.SetValue(9)
                define.logger.info("TimeSeriesData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed timeSeriesData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load TimeSeriesData Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def timeSeriesValueData(msgDlg):
            define.logger.info("Start timeSeriesValueData load.")
            try:
                instance = LoadTimeSeriesValue(obj)
                instance.load_data()
                msgDlg.guage.SetValue(10)
                define.logger.info("TimeSeriesValueData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed TimeSeriesValueData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load TimeSeriesValueData Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def dualValues(msgDlg):
            define.logger.info("Start booleanData load.")
            try:
                instance = LoadDualValues(obj)
                instance.load_data()
                msgDlg.guage.SetValue(11)
                define.logger.info("BooleanData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed booleanData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load Boolean Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def multiColumnArrayData(msgDlg):
            define.logger.info("Start MultiAttributeSeriesData load.")
            try:
                instance = LoadMultiCulumnArray(obj)
                instance.load_data()
                msgDlg.guage.SetValue(14)
                define.logger.info("MultiAttributeSeriesData load was finished successfully.\n\n")
                return instance
            except Exception as e:
                define.logger.error('Failed MultiAttributeSeriesData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load MultiAttributeSeries Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        def electronicFiles(msgDlg):
            define.logger.info("Start fileData load.")
            try:
                instance = LoadElectronicFiles(obj)
                instance.load_data()
                msgDlg.guage.SetValue(12)
                define.logger.info("FileData load was finished successfully.")
                return instance
            except Exception as e:
                define.logger.error('Failed fileData load.\n' + e.message)
                print(e)
                # message = messageDlg(None)
                # message.SetTitle(u"Sorry: something went wrong")
                # message.setMessage(u'{} \n\n [*] Could not Load File Data'.format(e))
                # message.Show()
                raise Exception(e.message)

        if self.path:
            obj = excel.open_workbook(self.path)
            # Write various data form db to excel file
            try:
                instance_cvData = cvData(self.msgDlg)
                instance_cvData.add_data()
                self.data_pushed_to_db.append(instance_cvData)

                if all(value is True for value in self.active):
                    instance_metaData = metaData(self.msgDlg)
                    instance_structData = structData(self.msgDlg)
                    instance_networksData = networksData(self.msgDlg)
                    instance_DescriptorValuesData = descriptorValues(self.msgDlg)
                    instance_paramsData = numericValues(self.msgDlg)
                    instance_seasonParamsData = seasonalNumericValues(self.msgDlg)
                    instance_timeSeriesData = timeSeriesData(self.msgDlg)
                    instance_timeSeriesValueData = timeSeriesValueData(self.msgDlg)
                    instance_booleanData = dualValues(self.msgDlg)
                    instance_fileData = electronicFiles(self.msgDlg)
                    instance_multiColumnArrayData = multiColumnArrayData(self.msgDlg)
                    pass

                elif self.active[0] and all(value is False for value in self.active[1:]):
                    instance_metaData = metaData()

                elif self.active[1] and all(value is False for value in self.active[2:]):
                    if self.active[0]:
                        instance_structData = structData(self.msgDlg)
                    else:
                        message = msg_somethigWrong(None, msg='Error, Structure Data Depends on MetaData, \n\n Please '
                                                              'check MetaData box')
                        message.Show()
                        raise Exception

                elif self.active[2] and self.active[1] is False and self.active[3] is False:
                    if self.active[0]:
                        instance_networksData = networksData(self.msgDlg)
                    else:
                        message = msg_somethigWrong(None, msg='Error, Network Data Depends on MetaData, \n\n Please '
                                                              'check MetaData box')
                        message.Show()
                        raise Exception()

                elif self.active[3] and all(value is False for value in self.active[:3]):
                    # textFreeData()
                    instance_DescriptorValuesData = descriptorValues(self.msgDlg)
                    instance_paramsData = numericValues(self.msgDlg)
                    instance_seasonParamsData = seasonalNumericValues(self.msgDlg)
                    instance_timeSeriesData = timeSeriesData(self.msgDlg)
                    instance_timeSeriesValueData = timeSeriesValueData(self.msgDlg)
                    instance_booleanData = dualValues(self.msgDlg)
                    instance_fileData = electronicFiles(self.msgDlg)
                    instance_multiColumnArrayData = multiColumnArrayData(self.msgDlg)


                # instance_cvData.add_data()

                if all(value is True for value in self.active):
                    instance_metaData.add_data()
                    instance_structData.add_data()
                    instance_networksData.add_data()
                    instance_DescriptorValuesData.add_data()
                    instance_paramsData.add_data()
                    instance_seasonParamsData.add_data()
                    instance_timeSeriesData.add_data()
                    instance_timeSeriesValueData.add_data()
                    instance_booleanData.add_data()
                    instance_fileData.add_data()
                    instance_multiColumnArrayData.add_data()
                    pass

                elif self.active[0] and all(value is False for value in self.active[1:]):
                    instance_metaData.add_data()

                elif self.active[1] and all(value is False for value in self.active[2:]):
                    if self.active[0]:
                        instance_structData.add_data()
                    else:
                        message = msg_somethigWrong(None, msg='Error, Structure Data Depends on MetaData, \n\n Please '
                                                              'check MetaData box')
                        message.Show()
                        raise Exception

                elif self.active[2] and self.active[1] is False and self.active[3] is False:
                    if self.active[0]:
                        instance_networksData.add_data()
                    else:
                        message = msg_somethigWrong(None, msg='Error, Network Data Depends on MetaData, \n\n Please '
                                                              'check MetaData box')
                        message.Show()
                        raise Exception()

                elif self.active[3] and all(value is False for value in self.active[:3]):
                    # textFreeData()
                    instance_paramsData.add_data()
                    instance_seasonParamsData.add_data()
                    instance_timeSeriesData.add_data()
                    instance_timeSeriesValueData.add_data()
                    instance_booleanData.add_data()
                    instance_fileData.add_data()
                    instance_DescriptorValuesData.add_data()
                    instance_multiColumnArrayData.add_data()
                # printing success message
                self.msgDlg.guage.SetValue(14)
                define.logger.info("All load was finished successfully.")
                wx.CallAfter(self.allDone)
                self.msgDlg.btn_ok.Enabled = True
                self.msgDlg.Close()



            except Exception as e:
                if e.message.startswith("The C++ part"):   # Terminate thread.
                    # Restore the Database first.
                    define.logger.info("Data loading terminated, restoring \
                        the previous database backup.")
                    DB_Setup().restore_db()
                    return
                else:                           # Another exception happened
                    define.logger.error('Failed data load.\n' + e.message +
                        '\nThe loading of all data has been reverted, Please fix the error and load the file again.')
                    self.errorMsg = e
                    self.occuredError()
                    return


    def occuredError(self):
        from viewer.Messages_forms.generalMsgDlg import messageDlg
        instance = messageDlg(None)
        instance.setMessage(self.errorMsg.message)
        result = instance.ShowModal()
        instance.Destroy()
        self.msgDlg.Destroy()
        self.btn_LoadDataGroups.Enabled = True
    def allDone(self):
        from Messages_forms.msg_successLoadDatabase import msg_successLoadDatabase

        instance = msg_successLoadDatabase(None)
        instance.setMessageText(u"\n\nYou successfully loaded the data in '" + self.selectedExcelFileName + u"' into " + define.dbName + u". \nYou can view the data by using: SQLite Manager: Add-ons for\nFirefox web browser")
        result = instance.ShowModal()
        instance.Destroy()
        self.msgDlg.Destroy()
        self.Destroy()

    def successDlgShow(self):
        from Messages_forms.msg_successLoadDatabase import msg_successLoadDatabase

        instance = msg_successLoadDatabase(None)
        instance.Show()

    def test_db_conn(self):
        setup = DB_Setup()
        if not setup.get_session():
            message = msg_somethigWrong(None, msg='\n\n\nError, No Database Found, Please first connect to a Database.')
            message.Show()
            return False
        return True

    def test_excel_file(self):
        if not self.path:
            from Messages_forms.msg_selectWorkbokFirst import msg_selectWorkbokFirst

            instance = msg_selectWorkbokFirst(None)
            instance.Show()
            return False
        return True

    def btn_LoadDataGroupsOnButtonClick(self, event):
        # TODO: Implement btn_LoadDataGroupsOnButtonClick

        # Test DB connection
        if not self.test_db_conn():
            return

        if not self.test_excel_file():
            return
            
        # Backup the Database before loading any new data into it.
        DB_Setup().backup_db()
        define.logger.info("Backing up the database before starting to \
                                    load new data into it.")

        myobject = event.GetEventObject()
        myobject.Disable()

        self.msgDlg = msg_loading(None)
        self.msgDlg.guage.SetRange(14)
        self.msgDlg.guage.SetValue(1)
        self.msgDlg.btn_ok.Enabled = False
        self.msgDlg.btn_cancel.Bind(wx.EVT_BUTTON, self.stop_loading)

        define.logger.name = __name__
        define.logger.info('Start data load')

        self.msgDlg.Show()

        ''' thread start: it is needed to show text in the Data loading window
        while the progress bar reports back the status of data loading steps'''
        # Will ask the thread to terminate itself, so the thread should always
        # check a condition if it should terminate itself and return
        self.our_thread = threading.Thread(None, self.load_data)
        self.our_thread.start()


    def stop_loading(self, event):
        self.sure_dlg = msg_sureToExit(self.msgDlg, "Are you sure you want to cancel/stop data loading?")
        self.sure_dlg.btn_ok.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)
        self.sure_dlg.Show()

    def btn_cancelOnButtonClick(self, event):

        try:
            if self.our_thread != None and self.our_thread.isAlive():
                print ' ****************** '
            if self.sure_dlg != None:
                self.sure_dlg.Destroy()
                define.logger.error('the user canceled data loading and the Wizard reverted everything. Please load the file again.')
            self.Destroy()      # Will destroy dlg_ImportSpreadsheetBasic
                                # which will raise an exception to thread
                                # the exception starts with "The C++ part"
                                # the thread will handle this exception by
                                # terminating itself.
        except Exception as e:
            print("error encountered closting thread %s: %s" % (self.our_thread.name, e))
