
import win32com.client
from controller.ConnectDB_ParseExcel import DB_Setup
from datetime import datetime

# 1. Connect to WEAP

# Function to create the connection with WEAP
class WEAP_export():

    WEAP = None

    def __init__(self, textCtrl_AreaNameOnText, SelectedScenarioName,fileDir):
        self.textCtrl_AreaNameOnText = textCtrl_AreaNameOnText
        self.SelectedScenarioName = SelectedScenarioName
        self.fileDir = fileDir
        self.ConnectWEAP()
        self.NodesSheetList = None
        self.NodesSheetList = None
        self.LinksSheetList = None
        self.unique_object_types_value_list = None
        self.extract_network()
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
        self.excel_pointer = None


    def ConnectWEAP(self):

        self.WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")


        self.WEAP.ActiveArea = self.textCtrl_AreaNameOnText


        ActiveArea=self.WEAP.ActiveArea.Name
        Scenario=self.WEAP.ActiveScenario.Name

        WEAPAreasDirectory= self.WEAP.AreasDirectory

        print ActiveArea
        print Scenario
        print WEAPAreasDirectory
        SourceName=self.WEAP.ActiveArea.Name

    # 2. Extract the WEAP Network

    def extract_network(self):
        from Extract_Network import Extract_Network

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list,self.BranchesNew_list = Extract_Network(self.WEAP, self.SelectedScenarioName)

    def GetWEAPValues(self):
        from GetValues import GetValues_WEAP
        return GetValues_WEAP(self.WEAP, self.BranchesNew_list, self.unique_object_types_value_list)

    def SaveToExcel(self, result_list, UniqObjectAtt_list, Projection_source=''):
        from SaveWEAPToExcel import SaveExcel

        DateStamp = datetime.now().strftime('%m-%d-%Y')
        excel_filename = self.fileDir + '/' + self.textCtrl_AreaNameOnText + '_' + DateStamp + '.xlsx'
        SaveExcel(self.NodesSheetList, self.LinksSheetList, result_list, UniqObjectAtt_list, self.WEAP,
                  excel_filename, Projection_source)

if __name__ == '__main__':
    weap_export = WEAP_export()
    result_list = weap_export.GetWEAPValues()
    weap_export.SaveToExcel(result_list)

