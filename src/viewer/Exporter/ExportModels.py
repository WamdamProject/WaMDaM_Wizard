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
## Class dlg_SelectModel
###########################################################################

class dlg_SelectModel ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 1, title = u"Select Model", pos = wx.DefaultPosition, size = wx.Size( 602,249 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Select the destination model (e.g., WEAP, WASH) ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		comboBox_SelectModelChoices = [ u"Water Evaluation and Planning system (WEAP)", u"Watershed Area of Suitable Habitat (WASH)- GAMS" ]
		self.comboBox_SelectModel = wx.ComboBox( self, 10, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_SelectModelChoices, 0 )
		bSizer2.Add( self.comboBox_SelectModel, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.btn_addmodel = wx.Button( self, 11, u"How to add a new model?", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btn_addmodel, 0, wx.ALL, 5 )
		
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_cancel = wx.Button( self, 12, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_next = wx.Button( self, 13, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.Add( gSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.comboBox_SelectModel.Bind( wx.EVT_COMBOBOX, self.comboBox_SelectModelOnCombobox )
		self.btn_addmodel.Bind( wx.EVT_BUTTON, self.btn_addmodelOnButtonClick )
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )
		self.btn_next.Bind( wx.EVT_BUTTON, self.btn_nextOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def comboBox_SelectModelOnCombobox( self, event ):
		event.Skip()
	
	def btn_addmodelOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cancelOnButtonClick( self, event ):
		event.Skip()
	
	def btn_nextOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class dlg_ProvideNetwork
###########################################################################

class dlg_ProvideNetwork ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 2, title = u"Provide Network", pos = wx.DefaultPosition, size = wx.Size( 602,465 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Provide the network and scenario from a spreadsheet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.FilePicker_ProvideNetwork = wx.FilePickerCtrl( self, 14, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer3.Add( self.FilePicker_ProvideNetwork, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Or ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial Black" ) )
		
		bSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Select an existing network in the WaMDaM database ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		comboBox_SelectNetChoices = []
		self.comboBox_SelectNet = wx.ComboBox( self, 15, u"Combo!", wx.DefaultPosition, wx.DefaultSize, comboBox_SelectNetChoices, 0 )
		bSizer3.Add( self.comboBox_SelectNet, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Select a scenario", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		comboBox_SelectScenChoices = []
		self.comboBox_SelectScen = wx.ComboBox( self, 16, u"Combo!", wx.DefaultPosition, wx.DefaultSize, comboBox_SelectScenChoices, 0 )
		bSizer3.Add( self.comboBox_SelectScen, 0, wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Provide Temporal extent and steps", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Model time step", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		comboBox_timStpChoices = []
		self.comboBox_timStp = wx.ComboBox( self, 17, u"Combo!", wx.DefaultPosition, wx.DefaultSize, comboBox_timStpChoices, 0 )
		gSizer1.Add( self.comboBox_timStp, 0, wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Start date (mm/dd/yyyy)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gSizer1.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.StartDt = wx.TextCtrl( self, 18, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.StartDt, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"End date (mm/dd/yyyy)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gSizer1.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.EndDt = wx.TextCtrl( self, 19, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.EndDt, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline6, 0, wx.ALL|wx.EXPAND, 5 )
		
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_back = wx.Button( self, 20, u"Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_next = wx.Button( self, 21, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.Add( gSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.FilePicker_ProvideNetwork.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_ProvideNetworkOnFileChanged )
		self.comboBox_SelectNet.Bind( wx.EVT_COMBOBOX, self.comboBox_SelectNetOnCombobox )
		self.comboBox_SelectScen.Bind( wx.EVT_COMBOBOX, self.comboBox_SelectScenOnCombobox )
		self.comboBox_timStp.Bind( wx.EVT_COMBOBOX, self.comboBox_timStpOnCombobox )
		self.StartDt.Bind( wx.EVT_TEXT, self.StartDtOnText )
		self.EndDt.Bind( wx.EVT_TEXT_ENTER, self.EndDtOnTextEnter )
		self.btn_back.Bind( wx.EVT_BUTTON, self.btn_backOnButtonClick )
		self.btn_next.Bind( wx.EVT_BUTTON, self.btn_nextOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def FilePicker_ProvideNetworkOnFileChanged( self, event ):
		event.Skip()
	
	def comboBox_SelectNetOnCombobox( self, event ):
		event.Skip()
	
	def comboBox_SelectScenOnCombobox( self, event ):
		event.Skip()
	
	def comboBox_timStpOnCombobox( self, event ):
		event.Skip()
	
	def StartDtOnText( self, event ):
		event.Skip()
	
	def EndDtOnTextEnter( self, event ):
		event.Skip()
	
	def btn_backOnButtonClick( self, event ):
		event.Skip()
	
	def btn_nextOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class dlg_SpecifyBoundary
###########################################################################

class dlg_SpecifyBoundary ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 3, title = u"Specify Boundary", pos = wx.DefaultPosition, size = wx.Size( 602,327 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Specify the search spatial boundary (optional)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer4.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Longitude (x) (-180 to +180 degrees) ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gSizer2.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		gSizer3 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"Minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer3.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		self.textCtrl_LongMin = wx.TextCtrl( self, 22, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.textCtrl_LongMin, 0, wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Maximum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		gSizer3.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.textCtrl_LongMax = wx.TextCtrl( self, 23, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.textCtrl_LongMax, 0, wx.ALL, 5 )
		
		
		gSizer2.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"latitude  (y) (-90° to +90° degrees)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		gSizer2.Add( self.m_staticText25, 0, wx.ALL, 5 )
		
		gSizer4 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Minimum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer4.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.textCtrl_LatMin = wx.TextCtrl( self, 24, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.textCtrl_LatMin, 0, wx.ALL, 5 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Maximum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		gSizer4.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.textCtrl_LatMax = wx.TextCtrl( self, 27, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.textCtrl_LatMax, 0, wx.ALL, 5 )
		
		
		gSizer2.Add( gSizer4, 0, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.EXPAND, 5 )
		
		
		bSizer4.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_back = wx.Button( self, 28, u"Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_next = wx.Button( self, 29, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( gSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.textCtrl_LongMin.Bind( wx.EVT_TEXT, self.textCtrl_LongMinOnText )
		self.textCtrl_LongMax.Bind( wx.EVT_TEXT, self.textCtrl_LongMaxOnText )
		self.textCtrl_LatMin.Bind( wx.EVT_TEXT_ENTER, self.textCtrl_LatMinOnTextEnter )
		self.textCtrl_LatMax.Bind( wx.EVT_TEXT, self.textCtrl_LatMaxOnText )
		self.btn_back.Bind( wx.EVT_BUTTON, self.btn_backOnButtonClick )
		self.btn_next.Bind( wx.EVT_BUTTON, self.btn_nextOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def textCtrl_LongMinOnText( self, event ):
		event.Skip()
	
	def textCtrl_LongMaxOnText( self, event ):
		event.Skip()
	
	def textCtrl_LatMinOnTextEnter( self, event ):
		event.Skip()
	
	def textCtrl_LatMaxOnText( self, event ):
		event.Skip()
	
	def btn_backOnButtonClick( self, event ):
		event.Skip()
	
	def btn_nextOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class dlg_SelectRules
###########################################################################

class dlg_SelectRules ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 4, title = u"Select Rules", pos = wx.DefaultPosition, size = wx.Size( 602,346 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Select or add rules for handling mismatches between data in WaMDaM and models", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		self.m_staticText26.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		bSizer4.Add( self.m_staticText26, 0, wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Multiple sources provide data for an attribute", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		bSizer4.Add( self.m_staticText27, 0, wx.ALL, 5 )
		
		comboBox_ruleChoices = []
		self.comboBox_rule = wx.ComboBox( self, 30, u"Verified", wx.DefaultPosition, wx.DefaultSize, comboBox_ruleChoices, 0 )
		bSizer4.Add( self.comboBox_rule, 0, wx.ALL, 5 )
		
		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"The exporter will automatically convert the unit from the source \nto the destination (model) and data format as pre-defined. \nFor time series , the exporter will aggregate data (e.g., daily to monthly). It will not disaggregate.\nThe script will skip any time series data if it has missing values", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer4.Add( self.m_staticText28, 0, wx.ALL, 5 )
		
		self.m_button20 = wx.Button( self, 31, u"How to add a new rule?", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button20, 0, wx.ALL, 5 )
		
		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText261 = wx.StaticText( self, wx.ID_ANY, u"Choose where to save the python script that records this expor session to re-run it again for reproducability", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText261.Wrap( -1 )
		bSizer4.Add( self.m_staticText261, 0, wx.ALL, 5 )
		
		self.dirPicker_python_output = wx.DirPickerCtrl( self, 170, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer4.Add( self.dirPicker_python_output, 0, wx.ALL|wx.EXPAND, 5 )
		
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_back = wx.Button( self, 32, u"Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_back, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_export = wx.Button( self, 33, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.btn_export, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( gSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.comboBox_rule.Bind( wx.EVT_COMBOBOX, self.comboBox_ruleOnCombobox )
		self.m_button20.Bind( wx.EVT_BUTTON, self.m_button20OnButtonClick )
		self.btn_back.Bind( wx.EVT_BUTTON, self.btn_backOnButtonClick )
		self.btn_export.Bind( wx.EVT_BUTTON, self.btn_exportOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def comboBox_ruleOnCombobox( self, event ):
		event.Skip()
	
	def m_button20OnButtonClick( self, event ):
		event.Skip()
	
	def btn_backOnButtonClick( self, event ):
		event.Skip()
	
	def btn_exportOnButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class dlg_ExtractWeapArea
###########################################################################

class dlg_ExtractWeapArea(wx.Dialog):

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=90, title=u"Extract Network and data of a WEAP Area ",
						   pos=wx.DefaultPosition, size=wx.Size(686, 438), style=wx.DEFAULT_DIALOG_STYLE)

		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

		gSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText20 = wx.StaticText(self, wx.ID_ANY, u"Select the WEAP Area name", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText20.Wrap(-1)
		gSizer5.Add(self.m_staticText20, 0, wx.ALL, 5)

		comboBox_WEAPAreaChoices = []
		self.comboBox_WEAPArea = wx.ComboBox(self, 576, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
											 comboBox_WEAPAreaChoices, 0)
		gSizer5.Add(self.comboBox_WEAPArea, 0, wx.ALL | wx.EXPAND, 5)

		self.m_staticText24 = wx.StaticText(self, wx.ID_ANY, u"Seclect a WEAP Scenario", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText24.Wrap(-1)
		gSizer5.Add(self.m_staticText24, 0, wx.ALL, 5)

		Combo_WEAP_scenarioChoices = []
		self.Combo_WEAP_scenario = wx.ComboBox(self, 987, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
											   Combo_WEAP_scenarioChoices, 0)
		gSizer5.Add(self.Combo_WEAP_scenario, 0, wx.ALL | wx.EXPAND, 5)

		self.m_staticText25 = wx.StaticText(self, wx.ID_ANY,
											u"Provide the current WEAP projection using the EPSG Codes in this format: EPSG:26912 \n "
											u"Leave it empty if the current projection is the global WGS84 ",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText25.Wrap(-1)
		gSizer5.Add(self.m_staticText25, 0, wx.ALL, 5)

		self.m_staticText26 = wx.StaticText(self, wx.ID_ANY,
											u"e.g., NAD83 / UTM zone 12N is EPSG:26912 so enter: EPSG:26912",
											wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText26.Wrap(-1)
		gSizer5.Add(self.m_staticText26, 0, wx.ALL, 5)

		self.ProjectionText = wx.TextCtrl(self, 4554, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer5.Add(self.ProjectionText, 0, wx.ALL | wx.EXPAND, 5)

		self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"Select output directory", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText21.Wrap(-1)
		gSizer5.Add(self.m_staticText21, 0, wx.ALL, 5)

		self.dirPicker_output = wx.DirPickerCtrl(self, 120, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
												 wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
		gSizer5.Add(self.dirPicker_output, 0, wx.ALL | wx.EXPAND, 5)

		gSizer51 = wx.GridSizer(0, 2, 0, 0)

		self.btn_extract = wx.Button(self, 121, u"Extract", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_extract, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

		self.btn_cancel = wx.Button(self, 123, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
		gSizer51.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		gSizer5.Add(gSizer51, 1, wx.EXPAND, 5)

		self.SetSizer(gSizer5)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.comboBox_WEAPArea.Bind(wx.EVT_COMBOBOX, self.comboBox_WEAPAreaOnCombobox)
		self.Combo_WEAP_scenario.Bind(wx.EVT_COMBOBOX, self.Combo_WEAP_scenarioOnCombobox)
		self.ProjectionText.Bind(wx.EVT_TEXT, self.ProjectionTextOnText)
		self.dirPicker_output.Bind(wx.EVT_DIRPICKER_CHANGED, self.dirPicker_outputOnDirChanged)
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)
		self.btn_extract.Bind(wx.EVT_BUTTON, self.btn_extractOnButtonClick)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def comboBox_WEAPAreaOnCombobox(self, event):
		event.Skip()

	def Combo_WEAP_scenarioOnCombobox(self, event):
		event.Skip()

	def ProjectionTextOnText(self, event):
		event.Skip()

	def dirPicker_outputOnDirChanged(self, event):
		event.Skip()

	def btn_cancelOnButtonClick(self, event):
		event.Skip()

	def btn_extractOnButtonClick(self, event):
		event.Skip()


###########################################################################
## Class dlg_re_run_export
###########################################################################

class dlg_re_run_export ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 91, title = u"Re-run a script use to export data to a model", pos = wx.DefaultPosition, size = wx.Size( 686,307 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Provide the python script that was used to export data from WaMDaM to a model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gSizer5.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.filePicker_py_rerun = wx.FilePickerCtrl( self, 95, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gSizer5.Add( self.filePicker_py_rerun, 0, wx.ALL|wx.EXPAND, 5 )
		
		gSizer51 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_cancel = wx.Button( self, 96, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer51.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_export = wx.Button( self, 99, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer51.Add( self.btn_export, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gSizer5.Add( gSizer51, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( gSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_backOnButtonClick )
		self.btn_export.Bind( wx.EVT_BUTTON, self.btn_exportOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btn_backOnButtonClick( self, event ):
		event.Skip()
	
	def btn_exportOnButtonClick( self, event ):
		event.Skip()
	

