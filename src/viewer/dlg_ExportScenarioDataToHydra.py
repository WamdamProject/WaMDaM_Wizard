
import wx
import WaMDaMWizard
from controller.wamdamAPI.GetDataStructure import GetDataStructure
from controller.wamdamAPI.GetDataValues import GetDataValues
from xlrd import open_workbook
# from xlutils.copy import copy
from Messages_forms.msg_somethigWrong import msg_somethigWrong
# This library is used here to write data to an excel file
from openpyxl import load_workbook

# Implementing dlg_ExportScenarioDataToRwise
class dlg_ExportScenarioDataToHydra( WaMDaMWizard.dlg_ExportScenarioDataToHydra ):
	def __init__( self, parent ):
		WaMDaMWizard.dlg_ExportScenarioDataToHydra.__init__( self, parent )
		self.sheetNames = ['1.1_Organiz&People', '1.2_Sources&Methods',
						   '2.1_ResourceTypes&ObjectTypes', '2.2_Attributes', '3.1_Networks&Scenarios',
						   '3.2_Nodes', '3.3_Links', '4_CategoricalValues', '4_NumericVaules', '4_FreeText',
						   '4_SeasonalNumericValues', '4_ElectronicFiles', '4_TimeSeries', '4_MultiAttributeSeries']
		self.path = ''
		try:
			''' init combo model'''
			self.dataStructure = GetDataStructure()
			self.datasets = self.dataStructure.getResourceType()
			list_acromy = list()
			for row in self.datasets:
				list_acromy.append(row.ResourceTypeAcronym)
			if list_acromy.__len__() > 0:
				self.comboBox_selectModel.SetItems(list_acromy)
		except Exception as e:
			message = msg_somethigWrong(None, msg=e.message)
			message.Show()
			self.Destroy()

	# Handlers for dlg_ExportScenarioDataToRwise events.
	def comboBox_selectModelOnCombobox( self, event ):
		selectedDataset = self.comboBox_selectModel.Value
		result = GetDataStructure()
		gettedMasterNetworkNames, data = result.getMasterNetwork(selectedDataset)
		if gettedMasterNetworkNames.__len__() <= 0:
			return
		self.comboBox_selectNetwork.SetItems(gettedMasterNetworkNames)
	
	def comboBox_selectNetworkOnCombobox( self, event ):
		selectedMasterNetworkName = self.comboBox_selectNetwork.Value
		result = GetDataStructure()
		gettedScenarioNames, data = result.getScenario(self.comboBox_selectModel.Value, selectedMasterNetworkName)
		if gettedScenarioNames.__len__() <= 0:
			return
		self.comboBox_selectScenario.SetItems(gettedScenarioNames)

	
	def comboBox_selectScenarioOnCombobox( self, event ):
		# TODO: Implement comboBox_selectScenarioOnCombobox
		pass
	
	def FilePicker_ExportToRwiseOnFileChanged( self, event ):
		valid_extension = ['xls','xlsx']
		self.path = self.FilePicker_ExportToRwise.GetPath()
		if not (self.path.split('.')[-1] in valid_extension):
			message = msg_somethigWrong(None, msg="Please select a valid Excel File")
			message.Show()
			return
		print 'This is working just fine...'
		print self.path
	
	def btn_Export_ScenarioDataOnButtonClick( self, event ):
		selectedDataset = self.comboBox_selectModel.Value
		selectedMasterNetworkName = self.comboBox_selectNetwork.Value
		selectedScenarioName = self.comboBox_selectScenario.Value


		# Check whether user select needed items correctly
		message = ''
		if (selectedDataset == None or selectedDataset == ''):
			message = 'Select the model name in WamDam.'
		elif selectedMasterNetworkName == None or selectedMasterNetworkName == '':
			message = 'Select the MasterNetworkName.'
		elif selectedScenarioName == None or selectedScenarioName == '':
			message = 'Select the ScenarioName.'
		elif not ['xls', 'xlsx', 'xlsm', 'xls'].__contains__(self.path.split('.')[-1]):
			message = 'Please select a valid excel file.'

		if message != '':
			messageDlg = msg_somethigWrong(None, msg=message)
			messageDlg.ShowModal()
			return

		print 'this is done'

		try:
			if self.path.split('.')[-1] == 'xls':
				wb = open_workbook(self.path)
				# self.workbook = copy(wb)
				self.workbook = wb
			else:
				self.workbook = load_workbook(self.path)

			# write data in excel file.
			result = GetDataStructure()
			organization_list = result.GetOrganizations(selectedDataset)
			self.write2excel(organization_list, 8, 2)
			people_list = result.GetPeople(selectedDataset)
			self.write2excel(people_list, 19, 2)
			source_list = result.GetSources(selectedDataset)
			self.write2excel(source_list, 8, 3)
			method_list = result.GetMethods(selectedDataset)
			self.write2excel(method_list, 19, 3)

			names, network_data_result = result.getMasterNetwork(selectedDataset)
			self.write2excel(network_data_result, 10, 6)
			names, scenarios_data_result = result.getScenario(selectedDataset, selectedMasterNetworkName)
			self.write2excel(scenarios_data_result, 20, 6)
			names, nodes_data_result = result.getNodes(selectedDataset, selectedMasterNetworkName,selectedScenarioName)
			self.write2excel(nodes_data_result, 11, 7)
			links_data_result = result.getLinkes(selectedDataset, selectedMasterNetworkName,selectedScenarioName)
			self.write2excel(links_data_result, 11, 8)

			data_result = result.getObjecttypes(selectedDataset)
			self.write2excel(data_result, 18, 4)
			attributes_result = result.getAttributes(selectedDataset)
			self.write2excel(attributes_result, 11, 5)
			dataset_result = result.getDatasetType(selectedDataset)
			self.write2excel(dataset_result, 10, 4)

			self.workbook.save(self.path)

			getDataValues = GetDataValues()
			# getDataValues.check_validation()
			getDataValues.exportDualValuesSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportTextConrolledSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportNumericValuesheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportElectronicFilesSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportSeasonalSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportTimeSeriesSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)
			getDataValues.exportMultiSheet1(selectedDataset, selectedMasterNetworkName, selectedScenarioName, self.path)

			from Messages_forms.msg_successLoadDatabase import msg_successLoadDatabase
			instance = msg_successLoadDatabase(None)
			instance.m_staticText1.SetLabel("Success export excel file")
			instance.ShowModal()
		except Exception as e:
			messageDlg = msg_somethigWrong(None, msg=e.message)
			messageDlg.Show()
			# raise Exception(e.message)

	def write2excel(self, resutl_list, startRow, sheetNumber):
		try:
			if self.path.split('.')[-1] == 'xls':
				try:
					sheet = self.workbook.get_sheet(sheetNumber)
				except:
					# message = msg_somethigWrong(None, msg="Please select a valid Excel File")
					# message.ShowModal()
					raise Exception("Please select a valid Excel File")
				for row_id, row in enumerate(resutl_list):
					for col_id, cell in enumerate(row):
						sheet.write(row_id + startRow - 1, col_id + 0, cell)
				# self.workbook.save(self.path)
			else:
				''' Validate sheet in excel'''
				try:
					sheet = self.workbook.get_sheet_by_name(self.sheetNames[sheetNumber])
				except:
					# message = msg_somethigWrong(None, msg="Please select a valid Excel File")
					# message.ShowModal()
					# return
					raise Exception("Please select a valid Excel File")
				for row_id, row in enumerate(resutl_list):
					for col_id, cell in enumerate(row):
						sheet.cell(row=row_id + startRow, column=col_id + 1, value=cell)

				# self.save(self.path)

		except Exception as e:
			print e
			messageDlg = msg_somethigWrong(None, msg=e.message)
			messageDlg.Show()
			raise Exception(e.message)
	def btn_cancelOnButtonClick( self, event ):
		# TODO: Implement btn_cancelOnButtonClick
		self.Close()
	
	
