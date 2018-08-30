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

class dlg_Publish ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 90, title = u"Publish a WaMDaM SQLite to HydroShare", pos = wx.DefaultPosition, size = wx.Size( 686,307 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"UserName", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gSizer5.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.m_textCtrl7 = wx.TextCtrl( self, 111, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl7, 0, wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		gSizer5.Add( self.m_staticText24, 0, wx.ALL, 5 )
		
		self.m_textCtrl8 = wx.TextCtrl( self, 11112, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl8, 0, wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		gSizer5.Add( self.m_staticText25, 0, wx.ALL, 5 )
		
		self.m_textCtrl9 = wx.TextCtrl( self, 1231, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl9, 0, wx.ALL, 5 )
		
		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		gSizer5.Add( self.m_staticText26, 0, wx.ALL, 5 )
		
		self.m_textCtrl10 = wx.TextCtrl( self, 12121, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl10, 0, wx.ALL, 5 )
		
		gSizer12 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_Publish = wx.Button( self, 121, u"Publish", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer12.Add( self.btn_Publish, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_cancel = wx.Button( self, 123, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer12.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gSizer5.Add( gSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( gSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btn_Publish.Bind( wx.EVT_BUTTON, self.btn_PublishOnButtonClick )
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btn_PublishOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cancelOnButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class dlg_VisulaizeWaMDaM
###########################################################################

class dlg_VisulaizeWaMDaM ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = 91, title = u"Visualize WaMDaM Network in OpenAgua", pos = wx.DefaultPosition, size = wx.Size( 686,429 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Upload a WaMDaM network to OpenAgua ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gSizer5.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"User Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		gSizer5.Add( self.m_staticText27, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self, 332, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
		
		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		gSizer5.Add( self.m_staticText28, 0, wx.ALL, 5 )
		
		self.m_textCtrl12 = wx.TextCtrl( self, 3232, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_textCtrl12, 0, wx.ALL, 5 )
		
		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"Select Model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		gSizer5.Add( self.m_staticText30, 0, wx.ALL, 5 )
		
		m_SelectModelChoices = []
		self.m_SelectModel = wx.ComboBox( self, 32322, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_SelectModelChoices, 0 )
		gSizer5.Add( self.m_SelectModel, 0, wx.ALL, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"Select Network", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		gSizer5.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		m_SelectNetworkChoices = []
		self.m_SelectNetwork = wx.ComboBox( self, 32121, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_SelectNetworkChoices, 0 )
		gSizer5.Add( self.m_SelectNetwork, 0, wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"Select Scenario", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		gSizer5.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		SelectScenarioChoices = []
		self.SelectScenario = wx.ComboBox( self, 1234, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, SelectScenarioChoices, 0 )
		gSizer5.Add( self.SelectScenario, 0, wx.ALL, 5 )
		
		gSizer51 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.btn_UploadToOpenAgua = wx.Button( self, 96, u"Upload To Open Agua", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer51.Add( self.btn_UploadToOpenAgua, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_cancel = wx.Button( self, 99, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer51.Add( self.btn_cancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gSizer5.Add( gSizer51, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( gSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btn_UploadToOpenAgua.Bind( wx.EVT_BUTTON, self.btn_UploadToOpenAguaOnButtonClick )
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btn_UploadToOpenAguaOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cancelOnButtonClick( self, event ):
		event.Skip()
	

