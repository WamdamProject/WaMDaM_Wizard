import WaMDaMWizard
from controller.wamdamAPI.GetResourceStructure import GetResourceStructure
from controller.wamdamAPI.GetMetadataByScenario import GetMetadataByScenario
from controller.wamdamAPI.GetInstancesByScenario import GetInstancesBySenario
from controller.wamdamAPI.GetAllValuesByScenario import GetAllValuesByScenario
from controller.WriteWaMDaMToExcel.ExportTemplate import ExportTemplate
# from xlutils.copy import copy
from Messages_forms.msg_somethigWrong import msg_somethigWrong
# This library is used here to write data to an excel file
from controller.ConnectDB_ParseExcel import DB_Setup

import pandas as pd

# Implementing dlg_ExportScenarioDataToExcel
class dlg_ExportScenarioDataToExcel( WaMDaMWizard.dlg_ExportScenarioDataToExcel ):
    def __init__( self, parent ):
        WaMDaMWizard.dlg_ExportScenarioDataToExcel.__init__( self, parent )
        self.path = ''
        try:
            if not DB_Setup().get_session():
                msg = "\n\nWarning: Please connect to sqlite first."
                raise Exception(msg)
            ''' init combo model'''
            self.dataStructure = GetResourceStructure()
            self.datasets = self.dataStructure.GetResourceType()
            list_acromy = list()
            for index, row in self.datasets.iterrows():
                list_acromy.append(row[0])
            if list_acromy.__len__() > 0:
                self.comboBox_selectModel.SetItems(list_acromy)
        except Exception as e:
            message = msg_somethigWrong(None, msg=e.message)
            message.Show()
            self.Destroy()

    # Handlers for dlg_ExportScenarioDataToExcel events.
    def comboBox_selectModelOnCombobox( self, event ):
        selectedDataset = self.comboBox_selectModel.Value
        result = GetInstancesBySenario()
        datas = result.GetMasterNetworks(selectedDataset)
        GotMasterNetworkNames = []
        for index, row in datas.iterrows():
            GotMasterNetworkNames.append(row[0])
        self.comboBox_selectNetwork.SetItems(GotMasterNetworkNames)

    def comboBox_selectNetworkOnCombobox( self, event ):
        selectedMasterNetworkName = self.comboBox_selectNetwork.Value
        result = GetInstancesBySenario()
        datas = result.GetScenarios(self.comboBox_selectModel.Value, selectedMasterNetworkName)
        GotScenarioNames = []
        for index, row in datas.iterrows():
            GotScenarioNames.append(row[0])
        self.comboBox_selectScenario.SetItems(GotScenarioNames)


    def comboBox_selectScenarioOnCombobox( self, event ):
        # TODO: Implement comboBox_selectScenarioOnCombobox
        pass

    def DirectoryPicker_ExportToExcelOnFileChanged( self, event ):
        valid_extension = ['xls','xlsx']
        self.path = self.DirectoryPicker_ExportToExcel.GetPath()

        # Because use directory picker dialog, add file name.
        # Create file name to export containing "ResourceTypeAcronum" and "NetworkName".
        selectedDataset = self.comboBox_selectModel.Value
        selectedMasterNetworkName = self.comboBox_selectNetwork.Value
        file_name_to_export = "{}_{}".format(selectedDataset, selectedMasterNetworkName)
        self.path = "{}/{}.xlsx".format(self.path, file_name_to_export)


        print 'This is working just fine...'
        print self.path

    def btn_Export_ScenarioDataOnButtonClick( self, event ):
        selectedDataset = self.comboBox_selectModel.Value
        selectedMasterNetworkName = self.comboBox_selectNetwork.Value
        selectedScenarioName = self.comboBox_selectScenario.Value


        # Check whether user select needed items correctly
        message = ''
        if (selectedDataset == None or selectedDataset == ''):
            message = 'Select the resource type (e.g, model name) in WamDam.'
        elif selectedMasterNetworkName == None or selectedMasterNetworkName == '':
            message = 'Select the MasterNetworkName.'
        elif selectedScenarioName == None or selectedScenarioName == '':
            message = 'Select the ScenarioName.'
        elif not ['xls', 'xlsx', 'xlsm', 'xls'].__contains__(self.path.split('.')[-1]):
            message = 'Please provide a directory for the output excel file.'
        if message != '':
            messageDlg = msg_somethigWrong(None, msg=message)
            messageDlg.ShowModal()
            return

        print 'this is done'

        try:
            self.btn_Export_ScenarioData.Enabled = False
            exportTemplate = ExportTemplate(self.path)



            ####################################################

            # Rescour Type structure

            ####################################################

            ResourceType_Result_df = GetResourceStructure()
            ObjectTypes_Result_df = GetResourceStructure()
            Attributes_Result_df = GetResourceStructure()


            resources_result = ResourceType_Result_df.GetResourceType(selectedDataset)
            data_result = ObjectTypes_Result_df.GetObjectTypesByResource(selectedDataset)
            exportTemplate.exportResourcesType(resources_result, data_result)

            # data_result = ObjectTypes_Result_df.GetObjectTypesByResource(selectedDataset)
            # exportTemplate.exportObjecttypes(data_result)

            attributes_result = Attributes_Result_df.GetAttributesByResource(selectedDataset)
            print "Count of attrs data: {}".format(str(len(attributes_result)))
            exportTemplate.exportAttributes(attributes_result)



            ####################################################

            # Metadata

            ####################################################

            Organizations_Result_df = GetMetadataByScenario()
            People_Result_df = GetMetadataByScenario()
            Sources_Result_df = GetMetadataByScenario()
            Methods_Result_df = GetMetadataByScenario()


            organization_result = Organizations_Result_df.GetOrganizationsByScenario(selectedDataset,selectedMasterNetworkName,selectedScenarioName)
            exportTemplate.exportOrganizations(organization_result)

            people_result = People_Result_df.GetPeopleByScenario(selectedDataset,selectedMasterNetworkName,selectedScenarioName)
            exportTemplate.exportPeople(people_result)

            source_result = Sources_Result_df.GetSourcesByScenario(selectedDataset,selectedMasterNetworkName,selectedScenarioName)
            exportTemplate.exportSources(source_result)

            method_result = Methods_Result_df.GetMethodsByScenario(selectedDataset,selectedMasterNetworkName,selectedScenarioName)
            exportTemplate.exportMethods(method_result)

            ####################################################

            # Instances

            ####################################################
            Network_Result_df = GetInstancesBySenario()
            Scenarios_Result_df = GetInstancesBySenario()
            Nodes_Result_df = GetInstancesBySenario()
            Links_Result_df = GetInstancesBySenario()



            network_data_result = Network_Result_df.GetMasterNetworks(selectedDataset)
            exportTemplate.exportMasterNetwork(network_data_result)

            scenarios_data_result = Scenarios_Result_df.GetScenarios(selectedDataset, selectedMasterNetworkName)
            exportTemplate.exportScenario(scenarios_data_result)

            nodes_data_result = Nodes_Result_df.GetNodesByScenario(selectedDataset, selectedMasterNetworkName,selectedScenarioName)
            print "Count of Nodes data: {}".format(str(len(nodes_data_result)))
            exportTemplate.exportNodes(nodes_data_result)

            links_data_result = Links_Result_df.GetLinksByScenario(selectedDataset, selectedMasterNetworkName,selectedScenarioName)
            print "Count of links data: {}".format(str(len(links_data_result)))
            exportTemplate.exportLinkes(links_data_result)

            print 'Good'
            ####################################################

            # Data Values

            ####################################################

            NumericValues_Result_df = GetAllValuesByScenario()
            CategoricalValues_Result_df = GetAllValuesByScenario()
            TextFreeValues_Result_df = GetAllValuesByScenario()
            SeasonalNumericValues_Result_df = GetAllValuesByScenario()
            TimeSeries_Result_df = GetAllValuesByScenario()
            TimeSeriesValues_Result_df = GetAllValuesByScenario()
            MultiColumns_Result_df = GetAllValuesByScenario()

            Numeric_result_list = NumericValues_Result_df.GetAllNumericValues(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            print "Count of Numeric data: {}".format(str(len(Numeric_result_list)))
            exportTemplate.exportNumericValue(Numeric_result_list)


            result_list = CategoricalValues_Result_df.GetAllCategoricalValues(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            print "Count of Categorical data: {}".format(str(len(result_list)))
            exportTemplate.exportCategoricalValues(result_list)


            result_list = TextFreeValues_Result_df.GetAllTextFree(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            print "Count of TextFree data: {}".format(str(len(result_list)))
            exportTemplate.exportFreeText(result_list)



            result_list = SeasonalNumericValues_Result_df.GetAllSeasonalNumericValues(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            print "Count of SeasonalNumeric data: {}".format(str(len(result_list)))
            exportTemplate.exportSeasonal(result_list)


            result_list = TimeSeries_Result_df.GetAllTimeSeries(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            print "Count of Timeseries data: {}".format(str(len(result_list)))
            exportTemplate.exportTimeSeries(result_list)

            result_list = TimeSeriesValues_Result_df.GetAllTimeSeriesValues(selectedDataset, selectedMasterNetworkName, selectedScenarioName)

            result_list['DateTimeStamp'] = pd.to_datetime(
                result_list.DateTimeStamp).apply(lambda x: x.strftime('%m/%d/%Y'))

            print "Count of Timeseriesvalues data: {}".format(str(len(result_list)))
            exportTemplate.exportTimeSeriesValues(result_list)

            # multiple columns

            up_table_column_result, bottom_table_result = MultiColumns_Result_df.GetAllMultiAttributeSeries(selectedDataset, selectedMasterNetworkName, selectedScenarioName)
            exportTemplate.exportMulti(up_table_column_result, bottom_table_result)

            from Messages_forms.msg_successLoadDatabase import msg_successLoadDatabase
            instance = msg_successLoadDatabase(None)
            instance.m_staticText1.SetLabel("Successfully exported the data into the Excel template")
            instance.ShowModal()
            self.btn_Export_ScenarioData.Enabled = True
            self.Destroy()
        except Exception as e:
            messageDlg = msg_somethigWrong(None, msg=e.message)
            messageDlg.Show()
            self.btn_Export_ScenarioData.Enabled = True
            # raise Exception(e.message)

    def write2excel(self, resutl_list, startRow, sheet):
        try:
            for row_id, row in enumerate(resutl_list):
                for col_id, cell in enumerate(row):
                    sheet.cell(row=row_id + startRow, column=col_id + 1, value=cell)


        except Exception as e:
            print e
            messageDlg = msg_somethigWrong(None, msg=e.message)
            messageDlg.Show()
            raise Exception(e.message)
    def btn_cancelOnButtonClick( self, event ):
        # TODO: Implement btn_cancelOnButtonClick
        self.Close()


