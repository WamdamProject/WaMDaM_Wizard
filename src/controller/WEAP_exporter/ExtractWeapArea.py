
import win32com.client
from controller.ConnectDB_ParseExcel import DB_Setup
from controller.ConnectDB_ParseExcel import SqlAlchemy as sq
from datetime import datetime
from sqlalchemy.orm import aliased
# 1. Connect to WEAP

# Function to create the connection with WEAP
class WEAP_export():

    WEAP = None
    # NodesSheetList = None
    # LinksSheetList = None
    def __init__(self, textCtrl_AreaNameOnText,fileDir):
        self.textCtrl_AreaNameOnText = textCtrl_AreaNameOnText
        self.fileDir = fileDir
        self.ConnectWEAP()
        self.NodesSheetList = None
        self.NodesSheetList = None
        self.LinksSheetList = None
        self.unique_object_types_value_list = None
        # self.Result_list = None
        # self.TimeSeries_ExpressValue_list = None
        self.extarct_network()
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
        self.excel_pointer = None

    def ConnectWEAP(self):

        self.WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")

        # self.WEAP.ActiveArea = "BearRiverFeb2018_V1"
        # user input value
        WEAPAreaProvided=self.textCtrl_AreaNameOnText
        # self.WEAP.ActiveArea = "WeberOgdenRiversLab-3"
        self.WEAP.ActiveArea = self.textCtrl_AreaNameOnText

        # excel_filename = self.fileDir + self.textCtrl_AreaNameOnText

        # WEAP.AreasDirectory: this one is read as input here and we cannot set it
        ActiveArea=self.WEAP.ActiveArea.Name
        Scenario=self.WEAP.ActiveScenario.Name

        WEAPAreasDirectory= self.WEAP.AreasDirectory

        print ActiveArea
        print Scenario
        print WEAPAreasDirectory
        SourceName=self.WEAP.ActiveArea.Name

    # 2. Extract the WEAP Network

    def extarct_network(self):
        from Extract_Network import Extract_Network

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list,self.BranchesNew_list = Extract_Network(self.WEAP)

    # here we need to pass the parameters above into the next functions
    # Paramters: SourceName, WEAP.Branches:

    def GetWEAPValues(self):
        # def SaveToExcel(self):
        from GetValues import GetValues_WEAP
        return GetValues_WEAP(self.WEAP, self.BranchesNew_list, self.unique_object_types_value_list)


    def SaveToExcel(self, result_list,UniqObjectAtt_list):
        from SaveToExcel import SaveExcel
        #add dir here?
        DateStamp= datetime.now().strftime('%m-%d-%Y')
        excel_filename = self.fileDir +  '/' + self.textCtrl_AreaNameOnText +'_'+DateStamp + '.xlsx'
        SaveExcel(self.NodesSheetList, self.LinksSheetList, result_list,UniqObjectAtt_list, self.WEAP, excel_filename)


if __name__ == '__main__':
    weap_export = WEAP_export()
    result_list = weap_export.GetWEAPValues()
    weap_export.SaveToExcel(result_list)

# so here I want to run Extract_Network function and get back its resutls


