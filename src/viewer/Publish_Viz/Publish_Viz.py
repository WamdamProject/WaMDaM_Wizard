# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class dlg_Publish
###########################################################################

class dlg_Publish(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=90, title=u"Publish a WaMDaM SQLite to HydroShare", pos=wx.DefaultPosition,
						   size=wx.Size(740, 596), style=wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

		gSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText20 = wx.StaticText(self, 564,
											u"Publish a WaMDaM 1.03 SQLite file as a new HydroShare Resource (Composite Resource Type) at \n                                                                            https://www.hydroshare.org\n\nWaMDaM Wizard automatically extracts most of the metadata and uploads the SQLite file\nbut you only need to provide the following items:\n ",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText20.Wrap(-1)
		gSizer5.Add(self.m_staticText20, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

		self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		gSizer5.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

		self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"Provide your HydroShare User Name", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText14.Wrap(-1)
		gSizer5.Add(self.m_staticText14, 0, wx.ALL, 5)

		self.m_textCtrl7 = wx.TextCtrl(self, 111, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer5.Add(self.m_textCtrl7, 0, wx.ALL, 5)

		self.m_staticText24 = wx.StaticText(self, wx.ID_ANY, u"Provide your HydroShare Password", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText24.Wrap(-1)
		gSizer5.Add(self.m_staticText24, 0, wx.ALL, 5)

		self.m_textCtrl8 = wx.TextCtrl(self, 11112, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, -1), wx.TE_PASSWORD)
		gSizer5.Add(self.m_textCtrl8, 0, wx.ALL, 5)

		self.m_staticText25 = wx.StaticText(self, wx.ID_ANY,
											u"Provide a title for the HydroShare new resource to be created",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText25.Wrap(-1)
		gSizer5.Add(self.m_staticText25, 0, wx.ALL, 5)

		self.m_textCtrl9 = wx.TextCtrl(self, 1231, wx.EmptyString, wx.DefaultPosition, wx.Size(500, -1), 0)
		gSizer5.Add(self.m_textCtrl9, 0, wx.ALL, 5)

		self.m_staticText26 = wx.StaticText(self, wx.ID_ANY,
											u"Provide an abstract to this HydroShare new resource (optional)",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText26.Wrap(-1)
		gSizer5.Add(self.m_staticText26, 0, wx.ALL, 5)

		self.m_textCtrl10 = wx.TextCtrl(self, 12121, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrl10.SetMinSize(wx.Size(700, 100))

		gSizer5.Add(self.m_textCtrl10, 0, wx.ALL, 5)

		self.m_staticText12 = wx.StaticText(self, wx.ID_ANY,
											u"Provide the author or creator name(s) of this new HydroShare resource. \nSeperate multiple names with \";\" (e.g., Adel Abdallahl; David Rosenberg) ",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText12.Wrap(-1)
		gSizer5.Add(self.m_staticText12, 0, wx.ALL, 5)

		self.m_textCtrl81 = wx.TextCtrl(self, 5645, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrl81.SetMinSize(wx.Size(300, -1))

		gSizer5.Add(self.m_textCtrl81, 0, wx.ALL, 5)

		gSizer12 = wx.GridSizer(0, 2, 0, 0)

		self.btn_Publish = wx.Button(self, 121, u"Publish", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer12.Add(self.btn_Publish, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

		self.btn_cancel = wx.Button(self, 123, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer12.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		gSizer5.Add(gSizer12, 1, wx.EXPAND, 5)

		self.SetSizer(gSizer5)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.btn_Publish.Bind(wx.EVT_BUTTON, self.btn_PublishOnButtonClick)
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

	def __del__(self):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btn_PublishOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cancelOnButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class dlg_VisulaizeWaMDaM
###########################################################################

class dlg_VisulaizeWaMDaM(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=91, title=u"Visualize WaMDaM Networks and data in OpenAgua",
						   pos=wx.DefaultPosition, size=wx.Size(686, 600), style=wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

		gSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText20 = wx.StaticText(self, wx.ID_ANY,
											u"Upload a WaMDaM network to OpenAgua @ https://www.openagua.org/ using Hydra Platform web services http://hydraplatform.org/",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText20.Wrap(-1)
		gSizer5.Add(self.m_staticText20, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

		self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		gSizer5.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

		self.m_staticText27 = wx.StaticText(self, wx.ID_ANY, u"Provide your OpenAgua User Name", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText27.Wrap(-1)
		gSizer5.Add(self.m_staticText27, 0, wx.ALL, 5)

		self.m_textCtrl11 = wx.TextCtrl(self, 332, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
		gSizer5.Add(self.m_textCtrl11, 0, wx.ALL, 5)

		self.m_staticText28 = wx.StaticText(self, wx.ID_ANY, u"Provide your OpenAgua Password", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText28.Wrap(-1)
		gSizer5.Add(self.m_staticText28, 0, wx.ALL, 5)

		self.m_textCtrl12 = wx.TextCtrl(self, 3232, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										wx.TE_PASSWORD)
		gSizer5.Add(self.m_textCtrl12, 0, wx.ALL, 5)

		gSizer52 = wx.GridSizer(2, 2, 0, 0)

		self.m_staticText25 = wx.StaticText(self, wx.ID_ANY, u"Either Select an existing Project name, OR",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText25.Wrap(-1)
		gSizer52.Add(self.m_staticText25, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)

		self.m_staticText26 = wx.StaticText(self, wx.ID_ANY,
											u"Provide a new project name for OpenAgua (e.g., Bear River)  ",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText26.Wrap(-1)
		gSizer52.Add(self.m_staticText26, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

		m_SelectProjectChoices = []
		self.m_SelectProject = wx.ComboBox(self, 879, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										   m_SelectProjectChoices, 0)
		gSizer52.Add(self.m_SelectProject, 0, wx.ALL, 5)

		self.m_textCtrl7 = wx.TextCtrl(self, 4527, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
		gSizer52.Add(self.m_textCtrl7, 0, wx.ALL, 5)

		gSizer5.Add(gSizer52, 1, wx.EXPAND, 5)

		self.m_staticText30 = wx.StaticText(self, wx.ID_ANY, u"Select Model in WaMDaM database", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText30.Wrap(-1)
		gSizer5.Add(self.m_staticText30, 0, wx.ALL, 5)

		m_SelectModelChoices = []
		self.m_SelectModel = wx.ComboBox(self, 3234, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										 m_SelectModelChoices, 0)
		gSizer5.Add(self.m_SelectModel, 0, wx.ALL, 5)

		self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, u"Select Network", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText31.Wrap(-1)
		gSizer5.Add(self.m_staticText31, 0, wx.ALL, 5)

		m_SelectNetworkChoices = []
		self.m_SelectNetwork = wx.ComboBox(self, 4434, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										   m_SelectNetworkChoices, 0)
		gSizer5.Add(self.m_SelectNetwork, 0, wx.ALL, 5)

		self.m_staticText32 = wx.StaticText(self, wx.ID_ANY, u"Select one or many scenarios", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText32.Wrap(-1)
		gSizer5.Add(self.m_staticText32, 0, wx.ALL, 5)

		self.SelectScenario = wx.ListCtrl(self, 456, wx.DefaultPosition, wx.Size(300, -1), wx.LC_LIST)
		gSizer5.Add(self.SelectScenario, 0, wx.ALL, 5)

		gSizer51 = wx.GridSizer(0, 2, 0, 0)

		self.btn_UploadToOpenAgua = wx.Button(self, 96, u"Upload To Open Agua", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_UploadToOpenAgua, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

		self.btn_cancel = wx.Button(self, 99, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		gSizer5.Add(gSizer51, 1, wx.EXPAND, 5)

		self.SetSizer(gSizer5)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.m_SelectProject.Bind(wx.EVT_COMBOBOX, self.m_SelectProjectOnCombobox)
		self.m_SelectModel.Bind(wx.EVT_COMBOBOX, self.m_SelectModelOnCombobox)
		self.m_SelectNetwork.Bind(wx.EVT_COMBOBOX, self.m_SelectNetworkOnCombobox)
		self.SelectScenario.Bind(wx.EVT_LIST_BEGIN_DRAG, self.SelectScenarioOnListBeginDrag)
		self.SelectScenario.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.SelectScenarioOnListBeginLabelEdit)
		self.SelectScenario.Bind(wx.EVT_LIST_BEGIN_RDRAG, self.SelectScenarioOnListBeginRDrag)
		self.SelectScenario.Bind(wx.EVT_LIST_CACHE_HINT, self.SelectScenarioOnListCacheHint)
		self.SelectScenario.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.SelectScenarioOnListColBeginDrag)
		self.SelectScenario.Bind(wx.EVT_LIST_COL_CLICK, self.SelectScenarioOnListColClick)
		self.SelectScenario.Bind(wx.EVT_LIST_COL_DRAGGING, self.SelectScenarioOnListColDragging)
		self.SelectScenario.Bind(wx.EVT_LIST_COL_END_DRAG, self.SelectScenarioOnListColEndDrag)
		self.SelectScenario.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.SelectScenarioOnListColRightClick)
		self.SelectScenario.Bind(wx.EVT_LIST_DELETE_ITEM, self.SelectScenarioOnListDeleteItem)
		self.SelectScenario.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.SelectScenarioOnListEndLabelEdit)
		self.SelectScenario.Bind(wx.EVT_LIST_INSERT_ITEM, self.SelectScenarioOnListInsertItem)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectScenarioOnListItemActivated)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.SelectScenarioOnListItemDeselected)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.SelectScenarioOnListItemFocused)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_MIDDLE_CLICK, self.SelectScenarioOnListItemMiddleClick)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.SelectScenarioOnListItemRightClick)
		self.SelectScenario.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectScenarioOnListItemSelected)
		self.SelectScenario.Bind(wx.EVT_LIST_KEY_DOWN, self.SelectScenarioOnListKeyDown)
		self.btn_UploadToOpenAgua.Bind(wx.EVT_BUTTON, self.btn_UploadToOpenAguaOnButtonClick)
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def m_SelectProjectOnCombobox(self, event):
		event.Skip()

	def m_SelectModelOnCombobox(self, event):
		event.Skip()

	def m_SelectNetworkOnCombobox(self, event):
		event.Skip()

	def SelectScenarioOnListBeginDrag(self, event):
		event.Skip()

	def SelectScenarioOnListBeginLabelEdit(self, event):
		event.Skip()

	def SelectScenarioOnListBeginRDrag(self, event):
		event.Skip()

	def SelectScenarioOnListCacheHint(self, event):
		event.Skip()

	def SelectScenarioOnListColBeginDrag(self, event):
		event.Skip()

	def SelectScenarioOnListColClick(self, event):
		event.Skip()

	def SelectScenarioOnListColDragging(self, event):
		event.Skip()

	def SelectScenarioOnListColEndDrag(self, event):
		event.Skip()

	def SelectScenarioOnListColRightClick(self, event):
		event.Skip()

	def SelectScenarioOnListDeleteAllItems(self, event):
		event.Skip()

	def SelectScenarioOnListDeleteItem(self, event):
		event.Skip()

	def SelectScenarioOnListEndLabelEdit(self, event):
		event.Skip()

	def SelectScenarioOnListInsertItem(self, event):
		event.Skip()

	def SelectScenarioOnListItemActivated(self, event):
		event.Skip()

	def SelectScenarioOnListItemDeselected(self, event):
		event.Skip()

	def SelectScenarioOnListItemFocused(self, event):
		event.Skip()

	def SelectScenarioOnListItemMiddleClick(self, event):
		event.Skip()

	def SelectScenarioOnListItemRightClick(self, event):
		event.Skip()

	def SelectScenarioOnListItemSelected(self, event):
		event.Skip()

	def SelectScenarioOnListKeyDown(self, event):
		event.Skip()

	def btn_UploadToOpenAguaOnButtonClick(self, event):
		event.Skip()

	def btn_cancelOnButtonClick(self, event):
		event.Skip()


###########################################################################
## Class dlg_ImportFromOpenAgua
###########################################################################

class dlg_ImportFromOpenAgua(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=881,
						   title=u"Import Networks and Data from OpenAgua into a WaMDaM WorkBook template ",
						   pos=wx.DefaultPosition, size=wx.Size(686, 615), style=wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

		gSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText20 = wx.StaticText(self, wx.ID_ANY,
											u"Import a network and its data from  Hydra Server within OpenAgua at https://www.openagua.org/ \nYou need to have an account with OpenAgua",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText20.Wrap(-1)
		gSizer5.Add(self.m_staticText20, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

		self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		gSizer5.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

		self.m_staticText27 = wx.StaticText(self, wx.ID_ANY, u"Provide your OpenAgua User Name", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText27.Wrap(-1)
		gSizer5.Add(self.m_staticText27, 0, wx.ALL, 5)

		self.m_textCtr_username = wx.TextCtrl(self, 882, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
		gSizer5.Add(self.m_textCtr_username, 0, wx.ALL, 5)

		self.m_staticText28 = wx.StaticText(self, wx.ID_ANY, u"Provide your OpenAgua Password", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText28.Wrap(-1)
		gSizer5.Add(self.m_staticText28, 0, wx.ALL, 5)

		self.m_textCtrl_pass = wx.TextCtrl(self, 883, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										   wx.TE_PASSWORD)
		gSizer5.Add(self.m_textCtrl_pass, 0, wx.ALL, 5)

		self.m_staticText22 = wx.StaticText(self, wx.ID_ANY, u"Connec to the Hydra Server on OpenAgua",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText22.Wrap(-1)
		gSizer5.Add(self.m_staticText22, 0, wx.ALL, 5)

		self.m_connect = wx.Button(self, 1230, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer5.Add(self.m_connect, 0, wx.ALL, 5)

		self.m_staticText30 = wx.StaticText(self, wx.ID_ANY,
											u"Select a Project in OpenAgua to Import into WaMDaM WorkBook template",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText30.Wrap(-1)
		gSizer5.Add(self.m_staticText30, 0, wx.ALL, 5)

		m_SelectProjectChoices = []
		self.m_SelectProject = wx.ComboBox(self, 884, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										   m_SelectProjectChoices, 0)
		gSizer5.Add(self.m_SelectProject, 0, wx.ALL, 5)

		self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"Select a Model template (Resource Type)",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText21.Wrap(-1)
		gSizer5.Add(self.m_staticText21, 0, wx.ALL, 5)

		m_SelectModelChoices = []
		self.m_SelectModel = wx.ComboBox(self, 8884, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										 m_SelectModelChoices, 0)
		gSizer5.Add(self.m_SelectModel, 0, wx.ALL, 5)

		self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, u"Select Network", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText31.Wrap(-1)
		gSizer5.Add(self.m_staticText31, 0, wx.ALL, 5)

		m_SelectNetworkChoices = []
		self.m_SelectNetwork = wx.ComboBox(self, 885, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
										   m_SelectNetworkChoices, 0)
		gSizer5.Add(self.m_SelectNetwork, 0, wx.ALL, 5)

		self.m_staticText32 = wx.StaticText(self, wx.ID_ANY, u"Select a scenario to import", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText32.Wrap(-1)
		gSizer5.Add(self.m_staticText32, 0, wx.ALL, 5)

		m_selectScenarioChoices = []
		self.m_selectScenario = wx.ComboBox(self, 886, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1),
											m_selectScenarioChoices, 0)
		gSizer5.Add(self.m_selectScenario, 0, wx.ALL, 5)

		self.m_staticText281 = wx.StaticText(self, wx.ID_ANY,
											 u"Provide the directory on your local machine where you want to save the WaMDaM Excel Workbook template",
											 wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText281.Wrap(-1)
		gSizer5.Add(self.m_staticText281, 0, wx.ALL, 5)

		self.m_dirPicker_export = wx.DirPickerCtrl(self, 901, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
												   wx.Size(300, -1), wx.DIRP_DEFAULT_STYLE)
		gSizer5.Add(self.m_dirPicker_export, 0, wx.ALL | wx.EXPAND, 5)

		gSizer51 = wx.GridSizer(0, 2, 0, 0)

		self.btn_Import = wx.Button(self, 887, u"Import", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_Import, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

		self.btn_cancel = wx.Button(self, 889, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		gSizer5.Add(gSizer51, 1, wx.EXPAND, 5)

		self.SetSizer(gSizer5)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.m_connect.Bind(wx.EVT_BUTTON, self.m_connectOnButtonClick)
		self.m_SelectProject.Bind(wx.EVT_COMBOBOX, self.m_SelectProjectOnCombobox)
		self.m_SelectModel.Bind(wx.EVT_COMBOBOX, self.m_SelectModelOnCombobox)
		self.m_SelectNetwork.Bind(wx.EVT_COMBOBOX, self.m_SelectNetworkOnCombobox)
		self.m_selectScenario.Bind(wx.EVT_COMBOBOX, self.m_selectScenarioOnCombobox)
		self.m_dirPicker_export.Bind(wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker_exportOnDirChanged)
		self.btn_Import.Bind(wx.EVT_BUTTON, self.btn_ImportOnButtonClick)
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def m_connectOnButtonClick(self, event):
		event.Skip()

	def m_SelectProjectOnCombobox(self, event):
		event.Skip()

	def m_SelectModelOnCombobox(self, event):
		event.Skip()

	def m_SelectNetworkOnCombobox(self, event):
		event.Skip()

	def m_selectScenarioOnCombobox(self, event):
		event.Skip()

	def m_dirPicker_exportOnDirChanged(self, event):
		event.Skip()

	def btn_ImportOnButtonClick(self, event):
		event.Skip()

	def btn_cancelOnButtonClick(self, event):
		event.Skip()
