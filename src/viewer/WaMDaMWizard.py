# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

# A few changes were made to this file to map the icons to their Python bit definition
# instead of the JPEG or PNG extensions. The reason why is because the WaMDaM executable
# does not work with JPEG or PNG extensions and instead it required the bit versions of the images.
# See the file img2py.py inside the icons folder. it was used to convert the images from PNG to python bits
# The python bit version of the images are stored in the icons.py file inside the icons folder.
###########################################################################


import wx, os, define
import wx.xrc
import wx.lib.agw.ribbon as rb



from icons.icons import *


###########################################################################
## Class frm_Home
###########################################################################
def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

class frm_Home ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = 1, title = u"WaMDaM Wizard 1.04", pos = wx.DefaultPosition, size = wx.Size( 1000,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        # self.SetWindowStyle(wx.STAY_ON_TOP)

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.Main_ribbonBar = rb.RibbonBar( self , wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_BAR_DEFAULT_STYLE )
        self.rtab_ConnDB = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"Connect to SQLite" , wx.NullBitmap , 0 )
        self.Main_ribbonBar.SetActivePage( self.rtab_ConnDB )
        self.rpnl_Conn = rb.RibbonPanel( self.rtab_ConnDB, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.rbarPnlConnDB = rb.RibbonButtonBar( self.rpnl_Conn, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.rbarPnlConnDB.AddSimpleButton( 2, u"Connect to a blank SQLite WaMDaM Database", sqlite.GetBitmap(), wx.EmptyString)
        self.rbarPnlConnDB.AddSimpleButton( 3, u"Connect to an Existing SQLite Database", sqlite1.GetBitmap(), wx.EmptyString)
        self.rbarPnlConnDB.AddSimpleButton( 6007, u"Connect to an Existing MySQL", mysql.GetBitmap(), wx.EmptyString)
        self.rbarPnlConnDB.AddSimpleButton( 4, u"CLose DB Connection", dissconnetDB.GetBitmap(), wx.EmptyString)
        self.rbarPnlConnDB.AddSimpleButton( 5, u"Exit WaMDaM Wizard", Exit.GetBitmap(), wx.EmptyString)
        self.rtab_PrepareDataServices = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"Prepare Your Data to WaMDaM" , wx.NullBitmap , 0 )
        self.rpnlPrepare = rb.RibbonPanel( self.rtab_PrepareDataServices, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.rbarImport1 = rb.RibbonButtonBar( self.rpnlPrepare, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.rbarImport1.AddSimpleButton( 6, u"From Shapefile To WaMDaM", ShapeFileToExcel.GetBitmap(), wx.EmptyString)
        self.rbarImport1.AddSimpleButton( 7, u"Cross Tab Seasonal To WaMDaM", Seasonal.GetBitmap(), wx.EmptyString)
        self.rbarImport1.AddSimpleButton( 8, u"Cross Tab Time Series to WaMDaM",TimeSeries.GetBitmap(), wx.EmptyString)
        self.rtab_Import = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"Import Data to WaMDaM" , wx.NullBitmap , 0 )
        self.rpnlImport = rb.RibbonPanel( self.rtab_Import, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.rbarImport = rb.RibbonButtonBar( self.rpnlImport, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.rbarImport.AddSimpleButton( 9, u"From Excel", ImportExcel.GetBitmap(), wx.EmptyString)
        self.rbarImport.AddSimpleButton( 5000, u"From CUAHSI", cuahsi.GetBitmap(), wx.EmptyString)
        self.rbarImport.AddSimpleButton( 5001, u"From WaDE", Wade.GetBitmap(), wx.EmptyString)
        self.rbarImport.AddSimpleButton( 10, u"From Bureau of Reclamation", ImportRwise.GetBitmap(), wx.EmptyString)
        self.rbarImport.AddSimpleButton( 11, u"WEAP Model (Area)", WEAP.GetBitmap(), wx.EmptyString)
        self.rbarImport.AddSimpleButton( 4357, u"Import From OpenAgua", OpenAgua.GetBitmap(), wx.EmptyString)

        self.rtab_Query = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"Query WaMDaM" , wx.NullBitmap , 0 )
        self.m_ribbonPanel7 = rb.RibbonPanel( self.rtab_Query, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.m_ribbonButtonBar6 = rb.RibbonButtonBar( self.m_ribbonPanel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonButtonBar6.AddSimpleButton( 610, u"Find metadata: Organiz., People, Sources, and Methods ", Query.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar6.AddSimpleButton( 12, u"Find Data requirement by a model", Query.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar6.AddSimpleButton( 13, u"Find Network of a model", Query.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar6.AddSimpleButton( 14, u"Compare Scenarios of a Network",  Query.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar6.AddSimpleButton( 15, u"Search for nodes and links",  Query.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar6.AddSimpleButton( 16, u"Search for Data Values",  Query.GetBitmap(), wx.EmptyString)


        self.rtab_Export = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"Export Data to Models" , wx.NullBitmap , 0 )
        self.rtab_Export = rb.RibbonPanel( self.rtab_Export, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.m_ribbonButtonBar7 = rb.RibbonButtonBar( self.rtab_Export, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ribbonButtonBar7.AddSimpleButton( 17, u"First time", WEAP.GetBitmap(), wx.EmptyString)

        self.m_ribbonButtonBar7.AddSimpleButton( 18, u"Re-run a previous export", rerun.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar7.AddSimpleButton( 19, u"Export WaMDaM to Excel Template", ImportExcel.GetBitmap(), wx.EmptyString)


        self.rtab_Publish_Viz = rb.RibbonPage(self.Main_ribbonBar, wx.ID_ANY, u"Visualize and Publish", wx.NullBitmap, 0)
        self.rtab_Publish_Viz = rb.RibbonPanel( self.rtab_Publish_Viz, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )

        self.Main_ribbonBar.SetActivePage(self.rtab_Publish_Viz)

        self.m_ribbonButtonBar71 = rb.RibbonButtonBar(self.rtab_Publish_Viz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                      0)
        self.m_ribbonButtonBar71.AddSimpleButton(4444, u"OpenAgua", OpenAgua.GetBitmap(), wx.EmptyString)
        self.m_ribbonButtonBar71.AddSimpleButton(4443, u"HydroShare", HydroShare.GetBitmap(), wx.EmptyString)


        self.rtab_About = rb.RibbonPage( self.Main_ribbonBar, wx.ID_ANY, u"About" , wx.NullBitmap , 0 )
        self.rpnl_About = rb.RibbonPanel( self.rtab_About, wx.ID_ANY, wx.EmptyString , wx.NullBitmap , wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
        self.rbarAbout = rb.RibbonButtonBar( self.rpnl_About, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.rbarAbout.AddSimpleButton( 20, u"About WaMDaM", about.GetBitmap(), wx.EmptyString)
        self.rbarAbout.AddSimpleButton( 21, u"License", licence.GetBitmap(), wx.EmptyString)
        self.rbarAbout.AddSimpleButton( 22, u"Help", Help.GetBitmap(), wx.EmptyString)
        self.Main_ribbonBar.Realize()

        bSizer1.Add( self.Main_ribbonBar, 0, wx.EXPAND|wx.ALL, 5 )

    # Add logos on interface
        bSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        # Add WaMDaM_Logo
        gSizer7 = wx.GridSizer(1, 1, 0, 0)
        img = WaMDaM_Logo.GetImage().Rescale(600, 200)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer7.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        bSizer1.Add(gSizer7, 0, wx.EXPAND | wx.ALL, 5)

        gSizer5 = wx.GridSizer(1, 3, 0, 0)

        # Add uwrl logo
        img = uwrl.GetImage().Rescale(157, 100)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer5.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # Add nsf logo
        img = nsf.GetImage().Rescale(99, 100)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer5.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # Add usu logo
        img = usu.GetImage().Rescale(266, 100)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer5.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        bSizer1.Add( gSizer5, 1, wx.EXPAND, 5 )
        bSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        gSizer6 = wx.GridSizer(1, 2, 0, 0)
        # Add iUTAH logo
        img = iUTAH.GetImage().Rescale(240, 100)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer6.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # Add CI_WATER logo
        img = CI_WATER.GetImage().Rescale(270, 100)
        img = img.ConvertToBitmap()
        control = wx.StaticBitmap(self, -1, img)
        gSizer6.Add(control, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)


        bSizer1.Add( gSizer6, 2, wx.EXPAND, 5 )
        bSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        #//////////////////////////////////////////////////

        self.SetSizer(bSizer1)
        self.Layout()
        self.StatusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, 23)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ConnNewDBOnRibbonButtonClicked, id = 2 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ConnExistingSQLiteOnRibbonButtonClicked, id = 3 )
        self.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ConnExistingMySQLOnRibbonButtonClicked, id=6007)
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_CloseConnectionOnRibbonButtonClicked, id = 4 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ExistWaMDaMOnRibbonButtonClicked, id = 5 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ShapefileToWaMDaMOnRibbonButtonClicked, id = 6 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbnCrossTabSeasonalToWaMDaMOnRibbonButtonClicked, id = 7 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_CrossTabTimeSeriesToWaMDaMOnRibbonButtonClicked, id = 8 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ImportExcelOnRibbonButtonClicked, id = 9 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ImportOpenAguaOnRibbonButtonClicked, id = 4357 )

        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ImportRwiseOnRibbonButtonClicked, id = 10 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_AddNewSourceOnRibbonButtonClicked, id = 11 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_query_metadataOnRibbonButtonClicked, id = 610 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_query_modelOnRibbonButtonClicked, id = 12 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_query_netwokOnRibbonButtonClicked, id = 13 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_compareScenariosOnRibbonButtonClicked, id = 14 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_SearchNodesLinksOnRibbonButtonClicked, id = 15 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btn_SearchDataValuesOnRibbonButtonClicked, id = 16 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_WEAPOnRibbonButtonClicked, id = 17 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_WASHOnRibbonButtonClicked, id = 18 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ExportToExcelOnRibbonButtonClicked, id = 19 )

        self.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_OpenAguaOnRibbonButtonClicked, id=4444)
        self.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_HydroShareOnRibbonButtonClicked, id=4443)
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btnAboutWaMDaMOnRibbonButtonClicked, id = 20 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btnLicenseOnRibbonButtonClicked, id = 21 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.btnHelpOnRibbonButtonClicked, id = 22 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ImportCUAHSIOnRibbonButtonClicked, id = 5000 )
        self.Bind( rb.EVT_RIBBONBUTTONBAR_CLICKED, self.rtbn_ImportWadeOnRibbonButtonClicked, id = 5001 )
    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def rtbn_ConnNewDBOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ConnExistingSQLiteOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_CloseConnectionOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ConnExistingMySQLOnRibbonButtonClicked(self, event):
        event.Skip()

    def rtbn_ExistWaMDaMOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ShapefileToWaMDaMOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbnCrossTabSeasonalToWaMDaMOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_CrossTabTimeSeriesToWaMDaMOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ImportExcelOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ImportRwiseOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_AddNewSourceOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_query_metadataOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_query_modelOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_query_netwokOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_compareScenariosOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_SearchNodesLinksOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btn_SearchDataValuesOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_WEAPOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_WASHOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_OpenAguaOnRibbonButtonClicked(self, event):
        event.Skip()

    def rtbn_HydroShareOnRibbonButtonClicked(self, event):
        event.Skip()

    def rtbn_AddModelOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rpnl_AboutOnRibbonPanelExtbuttonActivated( self, event ):
        event.Skip()

    def btnAboutWaMDaMOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btnLicenseOnRibbonButtonClicked( self, event ):
        event.Skip()

    def btnHelpOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ImportCUAHSIOnRibbonButtonClicked( self, event ):
        event.Skip()

    def rtbn_ImportWadeOnRibbonButtonClicked( self, event ):
        event.Skip()


###########################################################################
## Class dlg_ConnectNewDatabaseSQLite
###########################################################################

class dlg_ConnectNewDatabaseSQLite ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 24, title = u"Create a New blank WaMDaM SQLite Database and connect to it ", pos = wx.DefaultPosition, size = wx.Size( 446,241 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer57 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Provide the name of the new WaMDaM SQLite database file \n (Do not add an extension)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer57.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer57.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText171111 = wx.StaticText( self, wx.ID_ANY, u"Browse the directory where you want to place the new WaMDaM SQLite database file", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171111.Wrap( -1 )
        bSizer57.Add( self.m_staticText171111, 0, wx.ALL, 5 )

        self.dirPicker_newDB = wx.DirPickerCtrl( self, 15, os.getcwdu(), u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        ctrl = self.dirPicker_newDB.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer57.Add( self.dirPicker_newDB, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_connect = wx.Button( self, 26, u"Create and Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_connect, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )

        self.btn_cancel = wx.Button( self, 27, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer57.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer57 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.dirPicker_newDB.Bind( wx.EVT_FILEPICKER_CHANGED, self.dirPicker_newDBOnDirChanged )
        self.btn_connect.Bind( wx.EVT_BUTTON, self.btn_connectOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def dirPicker_newDBOnDirChanged( self, event ):
        event.Skip()

    def btn_connectOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_ConnectExistingDatabaseSQLite
###########################################################################

class dlg_ConnectExistingDatabaseSQLite ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 28, title = u"Connect to WaMDaM SQLite Database", pos = wx.DefaultPosition, size = wx.Size( 452,201 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer57 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Select the existing SQLite WaMDaM database on your pc", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer57.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        self.FilePicker_ConnectSQLite = wx.FilePickerCtrl( self, 29, os.getcwdu(), u"Select a file", u"Sqlite files (*.sqlite)|*.sqlite|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_ConnectSQLite.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer57.Add( self.FilePicker_ConnectSQLite, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_connect = wx.Button( self, 30, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_connect, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 31, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # self.btn_publish = wx.Button(self, 32, u"Publish", wx.DefaultPosition, wx.DefaultSize, 0)
        # gSizer111.Add(self.btn_publish, 2, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)


        bSizer57.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer57 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_ConnectSQLite.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_ConnectSQLiteOnFileChanged )
        self.btn_connect.Bind( wx.EVT_BUTTON, self.btn_connectOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )
        # self.btn_publish.Bind(wx.EVT_BUTTON, self.btn_publishOnButtonClick)

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_ConnectSQLiteOnFileChanged( self, event ):
        event.Skip()

    def btn_connectOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()

    def btn_publishOnButtonClick( self, event ):
        event.Skip()

class dlg_ExitDB ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 28, title = u"Exit WaMDaM SQLite Database", pos = wx.DefaultPosition, size = wx.Size( 452,201 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer57 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"\n\nAre you sure you wish to disconnect '" + define.dbName + u"' ?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer57.Add( self.m_staticText17111, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_connect = wx.Button( self, 30, u"Yes", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_connect, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 31, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer57.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer57 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.btn_connect.Bind( wx.EVT_BUTTON, self.btn_yesOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class

    def btn_yesOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()



###########################################################################
## Class dlg_ImportSpreadsheetBasic
###########################################################################

class dlg_ImportSpreadsheetBasic ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 32, title = u"Import WaMDaM spreadsheet data", pos = wx.DefaultPosition, size = wx.Size( 491,391 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Select the WaMDaM spreadsheet", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        self.FilePicker_Spreadsheet = wx.FilePickerCtrl( self, 33, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_Spreadsheet.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer15.Add( self.FilePicker_Spreadsheet, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Check the WaMDaM data group to import in the numeric order", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        gSizer441 = wx.GridSizer( 6, 1, 0, 0 )

        self.checkBox_CVs = wx.CheckBox( self, 34, u"1. Controlled Vocabulary", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_CVs.SetValue(True)
        gSizer441.Add( self.checkBox_CVs, 0, wx.ALL, 5 )

        self.checkBox_MetadataG = wx.CheckBox( self, 35, u"1. Metadata", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_MetadataG.SetValue(True)
        gSizer441.Add( self.checkBox_MetadataG, 0, wx.ALL, 5 )

        self.checkBox_DataStructureG = wx.CheckBox( self, 36, u"2. Data Structure", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_DataStructureG.SetValue(True)
        gSizer441.Add( self.checkBox_DataStructureG, 0, wx.ALL, 5 )

        self.checkBox_NetworksG = wx.CheckBox( self, 37, u"3. Networks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_NetworksG.SetValue(True)
        gSizer441.Add( self.checkBox_NetworksG, 0, wx.ALL, 5 )

        self.checkBox_DataValuesG = wx.CheckBox( self, 38, u"4. Data_Values", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_DataValuesG.SetValue(True)
        gSizer441.Add( self.checkBox_DataValuesG, 0, wx.ALL, 5 )

        self.checkBox_CVs.Enabled = False
        self.checkBox_MetadataG.Enabled = False
        self.checkBox_DataStructureG.Enabled = False
        self.checkBox_NetworksG.Enabled = False
        self.checkBox_DataValuesG.Enabled = False

        gSizer19 = wx.GridSizer( 1, 1, 0, 0 )

        self.btn_advanced = wx.Button( self, 39, u"Advanced", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer19.Add( self.btn_advanced, 0, wx.ALL, 5 )


        gSizer441.Add( gSizer19, 1, wx.EXPAND, 5 )


        bSizer15.Add( gSizer441, 0, 0, 5 )

        self.m_staticline251 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline251, 0, wx.EXPAND |wx.ALL, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_LoadDataGroups = wx.Button( self, 40, u"Load data", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_LoadDataGroups, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 41, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_Spreadsheet.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_SpreadsheetOnFileChanged )
        self.checkBox_CVs.Bind( wx.EVT_CHECKBOX, self.checkBox_MetadataGOnCheckBox )
        self.checkBox_MetadataG.Bind( wx.EVT_CHECKBOX, self.checkBox_MetadataGOnCheckBox )
        self.checkBox_DataStructureG.Bind( wx.EVT_CHECKBOX, self.checkBox_DataStructureGOnCheckBox )
        self.checkBox_NetworksG.Bind( wx.EVT_CHECKBOX, self.checkBox_NetworksGOnCheckBox )
        self.checkBox_DataValuesG.Bind( wx.EVT_CHECKBOX, self.checkBox_DataValuesGOnCheckBox )
        self.btn_advanced.Bind( wx.EVT_BUTTON, self.btn_advancedOnButtonClick )
        self.btn_LoadDataGroups.Bind( wx.EVT_BUTTON, self.btn_LoadDataGroupsOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_SpreadsheetOnFileChanged( self, event ):
        event.Skip()

    def checkBox_MetadataGOnCheckBox( self, event ):
        event.Skip()


    def checkBox_DataStructureGOnCheckBox( self, event ):
        event.Skip()

    def checkBox_NetworksGOnCheckBox( self, event ):
        event.Skip()

    def checkBox_DataValuesGOnCheckBox( self, event ):
        event.Skip()

    def btn_advancedOnButtonClick( self, event ):
        event.Skip()

    def btn_LoadDataGroupsOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()

    ###########################################################################
    ## Class dlg_ConnectExistingDatabaseMySQL
    ###########################################################################

class dlg_ConnectExistingDatabaseMySQL(wx.Dialog):
        def __init__(self, parent):
            wx.Dialog.__init__(self, parent, id=6000, title=u"Connect to WaMDaM MySQL Database", pos=wx.DefaultPosition,
                               size=wx.Size(453, 248), style=wx.DEFAULT_DIALOG_STYLE)

            self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

            bSizer57 = wx.BoxSizer(wx.VERTICAL)

            sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Select the existing MySQL WaMDaM database"),
                                         wx.VERTICAL)

            fgSizer1 = wx.FlexGridSizer(4, 2, 0, 14)
            fgSizer1.SetFlexibleDirection(wx.BOTH)
            fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

            self.m_staticText64 = wx.StaticText(self, wx.ID_ANY, u"Server:", wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_staticText64.Wrap(-1)
            fgSizer1.Add(self.m_staticText64, 0, wx.ALL, 5)

            self.Server = wx.TextCtrl(self, 6001, u"localhost", wx.DefaultPosition, (300, -1),
                                        0)
            fgSizer1.Add(self.Server, 1, wx.ALL | wx.ALIGN_BOTTOM | wx.EXPAND, 5)

            self.m_staticText65 = wx.StaticText(self, wx.ID_ANY, u"Database Name:",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_staticText65.Wrap(-1)
            fgSizer1.Add(self.m_staticText65, 0, wx.ALL, 5)

            self.dbName = wx.TextCtrl(self, 6002, u"Wamdam", wx.DefaultPosition, (300, -1),
                                      0)
            fgSizer1.Add(self.dbName, 1, wx.ALL, 5)

            self.m_staticText66 = wx.StaticText(self, wx.ID_ANY, u"User Name:", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
            self.m_staticText66.Wrap(-1)
            fgSizer1.Add(self.m_staticText66, 0, wx.ALL, 5)

            self.username = wx.TextCtrl(self, 6003, u"root", wx.DefaultPosition,
                                         (300, -1), 0)
            fgSizer1.Add(self.username, 1, wx.ALL | wx.EXPAND, 5)

            self.m_staticText67 = wx.StaticText(self, wx.ID_ANY, u"Password:", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
            self.m_staticText67.Wrap(-1)
            fgSizer1.Add(self.m_staticText67, 0, wx.ALL, 5)

            self.password = wx.TextCtrl(self, 6004, wx.EmptyString, wx.DefaultPosition,
                                        (300, -1), wx.TE_PASSWORD)
            fgSizer1.Add(self.password, 0, wx.ALL, 5 )


            sbSizer1.Add(fgSizer1, 1, wx.EXPAND, 5)

            bSizer57.Add(sbSizer1, 1, wx.EXPAND, 5)

            gSizer111 = wx.GridSizer(1, 3, 1, 1)

            self.btn_test = wx.Button(self, 6005, u"Test Connection", wx.DefaultPosition, wx.DefaultSize, 0)
            gSizer111.Add(self.btn_test, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

            self.btn_connect = wx.Button(self, 30, u"Connect and Save connection", wx.DefaultPosition, wx.DefaultSize,
                                         0)
            gSizer111.Add(self.btn_connect, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)

            self.btn_cancel = wx.Button(self, 31, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
            gSizer111.Add(self.btn_cancel, 1, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)

            bSizer57.Add(gSizer111, 1, wx.EXPAND, 5)

            self.SetSizer(bSizer57)
            self.Layout()

            self.Centre(wx.BOTH)

            # Connect Events
            self.btn_test.Bind(wx.EVT_BUTTON, self.btn_testOnButtonClick)
            self.btn_connect.Bind(wx.EVT_BUTTON, self.btn_connectOnButtonClick)
            self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

        def __del__(self):
            pass

        # Virtual event handlers, overide them in your derived class
        def btn_testOnButtonClick(self, event):
            event.Skip()

        def btn_connectOnButtonClick(self, event):
            event.Skip()

        def btn_cancelOnButtonClick(self, event):
            event.Skip()


###########################################################################
## Class dlg_query_metadata
###########################################################################

class dlg_query_metadata ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 605, title = u"Find Metadata in the database: Organizations, People, Sources, and Methods ", pos = wx.DefaultPosition, size = wx.Size( 491,300 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Select the excel workbook template to export results to", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        self.FilePicker_queryModel = wx.FilePickerCtrl( self, 500, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer15.Add( self.FilePicker_queryModel, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_find_metadata = wx.Button( self, 606, u"Find", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_find_metadata, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )

        self.btn_cancel = wx.Button( self, 607, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_queryModel.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_queryModelOnFileChanged )
        self.btn_find_metadata.Bind( wx.EVT_BUTTON, self.btn_find_metadataOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_queryModelOnFileChanged( self, event ):
        event.Skip()

    def btn_find_metadataOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()






###########################################################################
## Class dlg_query_model
###########################################################################

class dlg_query_model ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 42, title = u"Find Data requirement by a model", pos = wx.DefaultPosition, size = wx.Size( 491,300 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Select the Model name in WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        comboBox_selectModelChoices = []
        self.comboBox_selectModel = wx.ComboBox( self, 43, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectModelChoices, 0 )
        bSizer15.Add( self.comboBox_selectModel, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Select the excel workbook template to export results to", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        self.FilePicker_queryModel = wx.FilePickerCtrl( self, 500, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_queryModel.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer15.Add( self.FilePicker_queryModel, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_find_model_reqs = wx.Button( self, 44, u"Find", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_find_model_reqs, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )

        self.btn_cancel = wx.Button( self, 45, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.comboBox_selectModel.Bind( wx.EVT_COMBOBOX, self.comboBox_selectModelOnCombobox )
        self.FilePicker_queryModel.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_queryModelOnFileChanged )
        self.btn_find_model_reqs.Bind( wx.EVT_BUTTON, self.btn_find_model_reqsOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def comboBox_selectModelOnCombobox( self, event ):
        event.Skip()

    def FilePicker_queryModelOnFileChanged( self, event ):
        event.Skip()

    def btn_find_model_reqsOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_query_network
###########################################################################

class dlg_query_network ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 46, title = u"Find network nodes and links", pos = wx.DefaultPosition, size = wx.Size( 491,400 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Select the Model name in WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        comboBox_selectModelChoices = []
        self.comboBox_selectModel = wx.ComboBox( self, 47, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectModelChoices, 0 )
        bSizer15.Add( self.comboBox_selectModel, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline252 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline252, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17112 = wx.StaticText( self, wx.ID_ANY, u"Select the network name in selected model above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17112.Wrap( -1 )
        bSizer15.Add( self.m_staticText17112, 0, wx.ALL, 5 )

        comboBox_selectNetworkChoices = []
        self.comboBox_selectNetwork = wx.ComboBox( self, 48, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectNetworkChoices, 0 )
        bSizer15.Add( self.comboBox_selectNetwork, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline2521 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline2521, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline25211 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25211, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText171121 = wx.StaticText( self, wx.ID_ANY, u"Select the scenario name in selected network above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171121.Wrap( -1 )
        bSizer15.Add( self.m_staticText171121, 0, wx.ALL, 5 )

        comboBox_selectScenarioChoices = []
        self.comboBox_selectScenario = wx.ComboBox( self, 49, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectScenarioChoices, 0 )
        bSizer15.Add( self.comboBox_selectScenario, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Select the excel workbook template to export results to", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        self.FilePicker_QueryNetwork = wx.FilePickerCtrl( self, 501, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_QueryNetwork.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer15.Add( self.FilePicker_QueryNetwork, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_find_network_nodesLinks = wx.Button( self, 50, u"Find", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_find_network_nodesLinks, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 51, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.comboBox_selectModel.Bind( wx.EVT_COMBOBOX, self.comboBox_selectModelOnCombobox )
        self.comboBox_selectNetwork.Bind( wx.EVT_COMBOBOX, self.comboBox_selectNetworkOnCombobox )
        self.comboBox_selectScenario.Bind( wx.EVT_COMBOBOX, self.comboBox_selectScenarioOnCombobox )
        self.FilePicker_QueryNetwork.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_QueryNetworkOnFileChanged )
        self.btn_find_network_nodesLinks.Bind( wx.EVT_BUTTON, self.btn_find_network_nodesLinksOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def comboBox_selectModelOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectNetworkOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectScenarioOnCombobox( self, event ):
        event.Skip()

    def FilePicker_QueryNetworkOnFileChanged( self, event ):
        event.Skip()

    def btn_find_network_nodesLinksOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_compare_scenarios
###########################################################################

class dlg_compare_scenarios ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 62, title = u"Compare differences between scenarios of a network", pos = wx.DefaultPosition, size = wx.Size( 491,400 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Select the Model name in WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        comboBox_selectModelChoices = []
        self.comboBox_selectModel = wx.ComboBox( self, 53, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectModelChoices, 0 )
        bSizer15.Add( self.comboBox_selectModel, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17112 = wx.StaticText( self, wx.ID_ANY, u"Select the network name in selected model above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17112.Wrap( -1 )
        bSizer15.Add( self.m_staticText17112, 0, wx.ALL, 5 )

        comboBox_selectNetworkChoices = []
        self.comboBox_selectNetwork = wx.ComboBox( self, 54, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectNetworkChoices, 0 )
        bSizer15.Add( self.comboBox_selectNetwork, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25211 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25211, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText171121 = wx.StaticText( self, wx.ID_ANY, u"Select the first scenario name in selected network above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171121.Wrap( -1 )
        bSizer15.Add( self.m_staticText171121, 0, wx.ALL, 5 )

        comboBox_selectScenario1Choices = []
        self.comboBox_selectScenario1 = wx.ComboBox( self, 55, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectScenario1Choices, 0 )
        bSizer15.Add( self.comboBox_selectScenario1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline252111 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline252111, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText1711211 = wx.StaticText( self, wx.ID_ANY, u"Select the second scenario name in selected network above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711211.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711211, 0, wx.ALL, 5 )

        comboBox_selectScenario2Choices = []
        self.comboBox_selectScenario2 = wx.ComboBox( self, 56, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectScenario2Choices, 0 )
        bSizer15.Add( self.comboBox_selectScenario2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Select the excel workbook template to export results to", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        gSizer25 = wx.GridSizer( 1, 1, 0, 0 )

        self.FilePicker_compareScenarios = wx.FilePickerCtrl( self, 505, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_compareScenarios.GetTextCtrl()
        ctrl.SetLabel("")
        gSizer25.Add( self.FilePicker_compareScenarios, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer15.Add( gSizer25, 1, wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_compare_scenarios = wx.Button( self, 57, u"Compare", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_compare_scenarios, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 58, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.comboBox_selectModel.Bind( wx.EVT_COMBOBOX, self.comboBox_selectModelOnCombobox )
        self.comboBox_selectNetwork.Bind( wx.EVT_COMBOBOX, self.comboBox_selectNetworkOnCombobox )
        self.comboBox_selectScenario1.Bind( wx.EVT_COMBOBOX, self.comboBox_selectScenario1OnCombobox )
        self.comboBox_selectScenario2.Bind( wx.EVT_COMBOBOX, self.comboBox_selectScenario2OnCombobox )
        self.FilePicker_compareScenarios.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_compareScenariosOnFileChanged )
        self.btn_compare_scenarios.Bind( wx.EVT_BUTTON, self.btn_compare_scenariosOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def comboBox_selectModelOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectNetworkOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectScenario1OnCombobox( self, event ):
        event.Skip()

    def comboBox_selectScenario2OnCombobox( self, event ):
        event.Skip()

    def FilePicker_compareScenariosOnFileChanged( self, event ):
        event.Skip()

    def btn_compare_scenariosOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_ExportScenarioDataToExcel
###########################################################################

class dlg_ExportScenarioDataToExcel ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 7000, title = u"Export a Scenario Data to Excel Template", pos = wx.DefaultPosition, size = wx.Size( 491,400 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Select the Model name in WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        comboBox_selectModelChoices = []
        self.comboBox_selectModel = wx.ComboBox( self, 7001, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectModelChoices, 0 )
        bSizer15.Add( self.comboBox_selectModel, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline252 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline252, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17112 = wx.StaticText( self, wx.ID_ANY, u"Select the network name in selected model above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17112.Wrap( -1 )
        bSizer15.Add( self.m_staticText17112, 0, wx.ALL, 5 )

        comboBox_selectNetworkChoices = []
        self.comboBox_selectNetwork = wx.ComboBox( self, 7002, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectNetworkChoices, 0 )
        bSizer15.Add( self.comboBox_selectNetwork, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline2521 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline2521, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline25211 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25211, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText171121 = wx.StaticText( self, wx.ID_ANY, u"Select the scenario name in selected network above", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171121.Wrap( -1 )
        bSizer15.Add( self.m_staticText171121, 0, wx.ALL, 5 )

        comboBox_selectScenarioChoices = []
        self.comboBox_selectScenario = wx.ComboBox( self, 7003, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_selectScenarioChoices, 0 )
        bSizer15.Add( self.comboBox_selectScenario, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText17111 = wx.StaticText( self, wx.ID_ANY, u"Choose the folder where you want to export the excel file", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17111.Wrap( -1 )
        bSizer15.Add( self.m_staticText17111, 0, wx.ALL, 5 )

        # change this one to directory pickup
        self.DirectoryPicker_ExportToExcel = wx.DirPickerCtrl( self, 7006, wx.EmptyString, u"Select a directory", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer15.Add( self.DirectoryPicker_ExportToExcel, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_Export_ScenarioData = wx.Button( self, 7004, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_Export_ScenarioData, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 7005, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.comboBox_selectModel.Bind( wx.EVT_COMBOBOX, self.comboBox_selectModelOnCombobox )
        self.comboBox_selectNetwork.Bind( wx.EVT_COMBOBOX, self.comboBox_selectNetworkOnCombobox )
        self.comboBox_selectScenario.Bind( wx.EVT_COMBOBOX, self.comboBox_selectScenarioOnCombobox )
        self.DirectoryPicker_ExportToExcel.Bind( wx.EVT_DIRPICKER_CHANGED, self.DirectoryPicker_ExportToExcelOnFileChanged )
        self.btn_Export_ScenarioData.Bind( wx.EVT_BUTTON, self.btn_Export_ScenarioDataOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def comboBox_selectModelOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectNetworkOnCombobox( self, event ):
        event.Skip()

    def comboBox_selectScenarioOnCombobox( self, event ):
        event.Skip()

    def DirectoryPicker_ExportToRwiseOnFileChanged( self, event ):
        event.Skip()

    def btn_Export_ScenarioDataOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()



###########################################################################
## Class dlg_SearchNodesLinks
###########################################################################

class dlg_SearchNodesLinks(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=59,
                           title=u"Search for nodes and links within a spatial boundary of interest",
                           pos=wx.DefaultPosition, size=wx.Size(585, 456), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer15 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1711 = wx.StaticText(self, wx.ID_ANY,
                                              u"Select the Typology of the ObjectType you want to search for",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1711.Wrap(-1)
        bSizer15.Add(self.m_staticText1711, 0, wx.ALL, 5)

        self.checkBox_Nodes = wx.CheckBox(self, 900, u"Nodes", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.checkBox_Nodes, 0, wx.ALL, 5)

        self.checkBox_Links = wx.CheckBox(self, 901, u"Links", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.checkBox_Links, 0, wx.ALL, 5)

        self.m_staticline25 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer15.Add(self.m_staticline25, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText17112 = wx.StaticText(self, wx.ID_ANY,
                                               u"Select the Controlled Object Type to search for its node or link instances within a boundary in space",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17112.Wrap(-1)
        bSizer15.Add(self.m_staticText17112, 0, wx.ALL, 5)

        comboBox_selectObjectTypeChoices = []
        self.comboBox_selectObjectType = wx.ComboBox(self, 905, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                     comboBox_selectObjectTypeChoices, 0)
        bSizer15.Add(self.comboBox_selectObjectType, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticline25211 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer15.Add(self.m_staticline25211, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText17111 = wx.StaticText(self, wx.ID_ANY, u"Specify the search spatial boundary ",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17111.Wrap(-1)
        self.m_staticText17111.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))

        bSizer15.Add(self.m_staticText17111, 0, wx.ALL, 5)

        gSizer34 = wx.GridSizer(2, 2, 0, 0)

        self.m_staticText48 = wx.StaticText(self, wx.ID_ANY, u"Longitude (x) (-180 to +180 degrees) ",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText48.Wrap(-1)
        gSizer34.Add(self.m_staticText48, 0, wx.ALL, 5)

        gSizer36 = wx.GridSizer(2, 2, 0, 0)

        self.m_staticText50 = wx.StaticText(self, wx.ID_ANY, u"Minimum (East)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText50.Wrap(-1)
        gSizer36.Add(self.m_staticText50, 0, wx.ALL, 5)

        self.textCtrl_X_min = wx.TextCtrl(self, 110, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer36.Add(self.textCtrl_X_min, 0, wx.ALL, 5)

        self.m_staticText501 = wx.StaticText(self, wx.ID_ANY, u"Maximum (West)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText501.Wrap(-1)
        gSizer36.Add(self.m_staticText501, 0, wx.ALL, 5)

        self.textCtrl_X_Max = wx.TextCtrl(self, 111, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer36.Add(self.textCtrl_X_Max, 0, wx.ALL, 5)

        gSizer34.Add(gSizer36, 1, wx.EXPAND, 5)

        self.m_staticText49 = wx.StaticText(self, wx.ID_ANY, u"latitude  (y) (-90° to +90° degrees)",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText49.Wrap(-1)
        gSizer34.Add(self.m_staticText49, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        gSizer39 = wx.GridSizer(2, 2, 0, 0)

        self.m_staticText66 = wx.StaticText(self, wx.ID_ANY, u"Minimum (South)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText66.Wrap(-1)
        gSizer39.Add(self.m_staticText66, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.textCtrl_y_min = wx.TextCtrl(self, 112, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer39.Add(self.textCtrl_y_min, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.m_staticText67 = wx.StaticText(self, wx.ID_ANY, u"Maximum (North)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText67.Wrap(-1)
        gSizer39.Add(self.m_staticText67, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.textCtrl_y_max = wx.TextCtrl(self, 113, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer39.Add(self.textCtrl_y_max, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        gSizer34.Add(gSizer39, 1, wx.EXPAND, 5)

        bSizer15.Add(gSizer34, 1, wx.EXPAND, 5)

        gSizer23 = wx.GridSizer(2, 1, 0, 0)

        self.m_staticText45 = wx.StaticText(self, wx.ID_ANY, u"Select the excel workbook template to export results to",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText45.Wrap(-1)
        gSizer23.Add(self.m_staticText45, 0, wx.ALL, 5)

        self.FilePicker_searchNodesLinks = wx.FilePickerCtrl(self, 506, wx.EmptyString, u"Select a file", u"*.*",
                                                             wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        gSizer23.Add(self.FilePicker_searchNodesLinks, 1, wx.ALL | wx.EXPAND, 5)

        bSizer15.Add(gSizer23, 1, wx.EXPAND, 5)

        gSizer11 = wx.GridSizer(1, 2, 1, 1)

        self.btn_Search_nodesLinks = wx.Button(self, 64, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer11.Add(self.btn_Search_nodesLinks, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)

        self.btn_cancel = wx.Button(self, 65, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer11.Add(self.btn_cancel, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        bSizer15.Add(gSizer11, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer15)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.checkBox_Nodes.Bind(wx.EVT_CHECKBOX, self.checkBox_NodesOnCheckBox)
        self.comboBox_selectObjectType.Bind(wx.EVT_COMBOBOX, self.comboBox_selectObjectTypeOnCombobox)
        self.textCtrl_X_min.Bind(wx.EVT_TEXT, self.textCtrl_X_minOnText)
        self.textCtrl_X_Max.Bind(wx.EVT_TEXT, self.textCtrl_X_MaxOnText)
        self.textCtrl_y_min.Bind(wx.EVT_TEXT, self.textCtrl_y_minOnText)
        self.textCtrl_y_max.Bind(wx.EVT_TEXT, self.textCtrl_y_maxOnText)
        self.FilePicker_searchNodesLinks.Bind(wx.EVT_FILEPICKER_CHANGED, self.FilePicker_searchNodesLinksOnFileChanged)
        self.btn_Search_nodesLinks.Bind(wx.EVT_BUTTON, self.btn_Search_nodesLinksOnButtonClick)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def checkBox_NodesOnCheckBox(self, event):
        event.Skip()

    def comboBox_selectObjectTypeOnCombobox(self, event):
        event.Skip()

    def textCtrl_X_minOnText(self, event):
        event.Skip()

    def textCtrl_X_MaxOnText(self, event):
        event.Skip()

    def textCtrl_y_minOnText(self, event):
        event.Skip()

    def textCtrl_y_maxOnText(self, event):
        event.Skip()

    def FilePicker_searchNodesLinksOnFileChanged(self, event):
        event.Skip()

    def btn_Search_nodesLinksOnButtonClick(self, event):
        event.Skip()

    def btn_cancelOnButtonClick(self, event):
        event.Skip()


###########################################################################
## Class dlg_ImportFromCUAHS
###########################################################################

class dlg_ImportFromCUAHS ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 600, title = u"Import Time Series Data From CUAHSI", pos = wx.DefaultPosition, size = wx.Size( 586,500 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17112 = wx.StaticText( self, wx.ID_ANY, u"Provide CUAHSI Site Code", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17112.Wrap( -1 )
        bSizer15.Add( self.m_staticText17112, 0, wx.ALL, 5 )

        # self.m_textCtrl22 = wx.TextCtrl( self, 601, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        # bSizer15.Add( self.m_textCtrl22, 0, wx.ALL|wx.EXPAND, 5 )

        comboBox_StateChoices = []
        self.comboBox_Code = wx.ComboBox( self, 2001, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_StateChoices, 0 )
        bSizer15.Add( self.comboBox_Code, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText83 = wx.StaticText( self, wx.ID_ANY, u"Provide CUAHSI Variable Code", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText83.Wrap( -1 )
        bSizer15.Add( self.m_staticText83, 0, wx.ALL, 5 )

        # self.m_textCtrl23 = wx.TextCtrl( self, 602, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        # bSizer15.Add( self.m_textCtrl23, 0, wx.ALL|wx.EXPAND, 5 )

        comboBox_StateChoices = []
        self.comboBox_VariableCode = wx.ComboBox( self, 2001, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_StateChoices, 0 )
        bSizer15.Add( self.comboBox_VariableCode, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText84 = wx.StaticText( self, wx.ID_ANY, u"Provide Time Series Begin Date [yyyy-mm-dd]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText84.Wrap( -1 )
        bSizer15.Add( self.m_staticText84, 0, wx.ALL, 5 )

        self.m_textCtrl24 = wx.TextCtrl( self, 603, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.m_textCtrl24, 0, wx.ALL, 5 )

        self.m_staticText85 = wx.StaticText( self, wx.ID_ANY, u"Provide Time Series End Date [yyyy-mm-dd]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText85.Wrap( -1 )
        bSizer15.Add( self.m_staticText85, 0, wx.ALL, 5 )

        self.m_textCtrl25 = wx.TextCtrl( self, 604, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.m_textCtrl25, 0, wx.ALL, 5 )

        self.btn_RetrieveData = wx.Button( self, 605, u"Retrieve Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.btn_RetrieveData, 0, wx.ALL, 5 )

        gSizer23 = wx.GridSizer( 5, 1, 0, 0 )

        self.m_staticText88 = wx.StaticText( self, wx.ID_ANY, u"The time series data will be loaded into WaMDaM database under the following:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText88.Wrap( -1 )
        self.m_staticText88.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )

        gSizer23.Add( self.m_staticText88, 0, wx.ALL, 5 )

        self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, u"DatasetName: CUAHSI \nObjectType: Site\nAttributeDataTypeCV:  TimeSeries\n\nMasterNetworkName: CUAHSI Sites Network\nScenarioName: Historic Data\n", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText86.Wrap( -1 )
        gSizer23.Add( self.m_staticText86, 0, wx.ALL, 5 )


        bSizer15.Add( gSizer23, 1, wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_Load = wx.Button( self, 606, u"Load into WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_Load, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 607, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.btn_RetrieveData.Bind( wx.EVT_BUTTON, self.btn_RetrieveDataOnButtonClick )
        self.btn_Load.Bind( wx.EVT_BUTTON, self.btn_LoadOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def btn_RetrieveDataOnButtonClick( self, event ):
        event.Skip()

    def btn_LoadOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()

    ###########################################################################
    ## Class dlg_ImportFromWaDE
    ###########################################################################

class dlg_ImportFromWaDE ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 2000, title = u"Import Water Use Data From WaDE: Water Data Exchange-Western States Water Council", pos = wx.DefaultPosition, size = wx.Size( 586,500 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText17112 = wx.StaticText( self, wx.ID_ANY, u"Select a State", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17112.Wrap( -1 )
        bSizer15.Add( self.m_staticText17112, 0, wx.ALL, 5 )

        comboBox_StateChoices = []
        self.comboBox_State = wx.ComboBox( self, 2001, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_StateChoices, 0 )
        bSizer15.Add( self.comboBox_State, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText83 = wx.StaticText( self, wx.ID_ANY, u"Select a Planning Basin", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText83.Wrap( -1 )
        bSizer15.Add( self.m_staticText83, 0, wx.ALL, 5 )

        comboBox_PlanningBasinChoices = []
        self.comboBox_PlanningBasin = wx.ComboBox( self, 2002, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_PlanningBasinChoices, 0 )
        bSizer15.Add( self.comboBox_PlanningBasin, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText841 = wx.StaticText( self, wx.ID_ANY, u"Select a Begining Year", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText841.Wrap( -1 )
        bSizer15.Add( self.m_staticText841, 0, wx.ALL, 5 )

        comboBox_year1Choices = []
        self.comboBox_year1 = wx.ComboBox( self, 9005, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_year1Choices, 0 )
        bSizer15.Add( self.comboBox_year1, 0, wx.ALL, 5 )

        self.m_staticText84 = wx.StaticText( self, wx.ID_ANY, u"Select an End Year", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText84.Wrap( -1 )
        bSizer15.Add( self.m_staticText84, 0, wx.ALL, 5 )

        comboBox_year2Choices = []
        self.comboBox_year2 = wx.ComboBox( self, 2003, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboBox_year2Choices, 0 )
        bSizer15.Add( self.comboBox_year2, 0, wx.ALL, 5 )

        self.btn_RetrieveData = wx.Button( self, 2004, u"Retrieve Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.btn_RetrieveData, 0, wx.ALL, 5 )

        gSizer23 = wx.GridSizer( 5, 1, 0, 0 )

        self.m_staticText88 = wx.StaticText( self, wx.ID_ANY, u"The time series data will be loaded into WaMDaM database under the following:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText88.Wrap( -1 )
        self.m_staticText88.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )

        gSizer23.Add( self.m_staticText88, 0, wx.ALL, 5 )

        self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, u"DatasetName: WaDE\nObjectType: Area\nAttributeDataTypeCV:  TimeSeries\n\nMasterNetworkName: WaDE Network\nScenarioName: Historic Data\n", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText86.Wrap( -1 )
        gSizer23.Add( self.m_staticText86, 0, wx.ALL, 5 )


        bSizer15.Add( gSizer23, 1, wx.EXPAND, 5 )

        gSizer11 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_Load = wx.Button( self, 2006, u"Load into WaMDaM", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_Load, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 2007, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer11.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


        bSizer15.Add( gSizer11, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.comboBox_year1.Bind( wx.EVT_COMBOBOX, self.comboBox_year1OnCombobox )
        self.comboBox_year2.Bind( wx.EVT_COMBOBOX, self.comboBox_year2OnCombobox )
        self.comboBox_State.Bind( wx.EVT_COMBOBOX, self.comboBox_stateOnCombobox )
        self.btn_RetrieveData.Bind( wx.EVT_BUTTON, self.btn_RetrieveDataOnButtonClick )
        self.btn_Load.Bind( wx.EVT_BUTTON, self.btn_LoadOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def comboBox_year1OnCombobox( self, event ):
        event.Skip()

    def comboBox_year2OnCombobox( self, event ):
        event.Skip()

    def comboBox_stateOnCombobox( self, event ):
        event.Skip()

    def btn_RetrieveDataOnButtonClick( self, event ):
        event.Skip()

    def btn_LoadOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_SearchDataValues
###########################################################################

class dlg_SearchDataValues(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=300, title=u"Search for Data Values", pos=wx.DefaultPosition,
                           size=wx.Size(661, 519), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer15 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText17113 = wx.StaticText(self, wx.ID_ANY,
                                               u"Select the Typology of the ObjectType you want to search for",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17113.Wrap(-1)
        bSizer15.Add(self.m_staticText17113, 0, wx.ALL, 5)

        self.checkBox_Nodes = wx.CheckBox(self, 1100, u"Nodes", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.checkBox_Nodes, 0, wx.ALL, 5)

        self.checkBox_Links = wx.CheckBox(self, 1101, u"Links", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.checkBox_Links, 0, wx.ALL, 5)

        self.m_staticText17112 = wx.StaticText(self, wx.ID_ANY,
                                               u"Select the Controlled Object Type available in the WaMDaM database to search for Data Values of its Attributes ",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17112.Wrap(-1)
        bSizer15.Add(self.m_staticText17112, 0, wx.ALL, 5)

        comboBox_ctrObjectTypeChoices = []
        self.comboBox_ctrObjectType = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                  comboBox_ctrObjectTypeChoices, 0)
        bSizer15.Add(self.comboBox_ctrObjectType, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticline25211 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer15.Add(self.m_staticline25211, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText171121 = wx.StaticText(self, wx.ID_ANY, u"Select the Controlled Attribute ",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText171121.Wrap(-1)
        bSizer15.Add(self.m_staticText171121, 0, wx.ALL, 5)

        comboBox_ctrAttributeChoices = []
        self.comboBox_ctrAttribute = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                 comboBox_ctrAttributeChoices, 0)
        bSizer15.Add(self.comboBox_ctrAttribute, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText1711212 = wx.StaticText(self, wx.ID_ANY, u"Select the Controlled Attribute Data Type",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1711212.Wrap(-1)
        bSizer15.Add(self.m_staticText1711212, 0, wx.ALL, 5)

        gSizer29 = wx.GridSizer(2, 4, 0, 0)

        self.checkBox_All = wx.CheckBox(self, 1203, u"All", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_All, 0, wx.ALL, 5)

        self.checkBox_DualValues = wx.CheckBox(self, 1200, u"DualValues", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_DualValues, 0, wx.ALL, 5)

        self.checkBox_NumericValues = wx.CheckBox(self, 1201, u"Numeric Values", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_NumericValues, 0, wx.ALL, 5)

        self.checkBox_SeasonalNumericValues = wx.CheckBox(self, 1202, u"Seasonal Numeric Values", wx.DefaultPosition,
                                                          wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_SeasonalNumericValues, 0, wx.ALL, 5)

        self.checkBox_DescriptorValues = wx.CheckBox(self, 1204, u"Descriptor Values", wx.DefaultPosition,
                                                     wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_DescriptorValues, 0, wx.ALL, 5)

        self.checkBox_ElectronicFiles = wx.CheckBox(self, 1205, u"Electronic Files", wx.DefaultPosition, wx.DefaultSize,
                                                    0)
        gSizer29.Add(self.checkBox_ElectronicFiles, 0, wx.ALL, 5)

        self.checkBox_TimeSeries = wx.CheckBox(self, 1206, u"TimeSeries", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_TimeSeries, 0, wx.ALL, 5)

        self.checkBox_MultiAttributeSeries = wx.CheckBox(self, 1207, u"Multi Attribute Series", wx.DefaultPosition,
                                                         wx.DefaultSize, 0)
        gSizer29.Add(self.checkBox_MultiAttributeSeries, 0, wx.ALL, 5)

        bSizer15.Add(gSizer29, 1, wx.EXPAND, 5)

        self.m_staticText1711211 = wx.StaticText(self, wx.ID_ANY, u"Select the Controlled Instance Name",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1711211.Wrap(-1)
        bSizer15.Add(self.m_staticText1711211, 0, wx.ALL, 5)

        comboBox_ctrlInstanceChoices = []
        self.comboBox_ctrlInstance = wx.ComboBox(self, 1209, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                 comboBox_ctrlInstanceChoices, 0)
        bSizer15.Add(self.comboBox_ctrlInstance, 0, wx.ALL | wx.EXPAND, 5)

        gSizer24 = wx.GridSizer(2, 1, 0, 0)

        self.m_staticText46 = wx.StaticText(self, wx.ID_ANY, u"Select the excel workbook template to export results to",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText46.Wrap(-1)
        gSizer24.Add(self.m_staticText46, 0, wx.ALL, 5)

        self.FilePicker_searchDataValues = wx.FilePickerCtrl(self, 507, wx.EmptyString, u"Select a file", u"*.*",
                                                             wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        gSizer24.Add(self.FilePicker_searchDataValues, 0, wx.ALL | wx.EXPAND, 5)

        bSizer15.Add(gSizer24, 1, wx.EXPAND, 5)

        gSizer11 = wx.GridSizer(1, 2, 1, 1)

        self.btn_Search_nodesLinks = wx.Button(self, 305, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer11.Add(self.btn_Search_nodesLinks, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)

        self.btn_cancel = wx.Button(self, 306, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer11.Add(self.btn_cancel, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        bSizer15.Add(gSizer11, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer15)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_INIT_DIALOG, self.dlg_SearchDataValuesOnInitDialog)
        self.checkBox_Nodes.Bind(wx.EVT_CHECKBOX, self.checkBox_NodesOnCheckBox)
        self.checkBox_Links.Bind(wx.EVT_CHECKBOX, self.checkBox_LinksOnCheckBox)
        self.comboBox_ctrObjectType.Bind(wx.EVT_COMBOBOX, self.comboBox_ctrObjectTypeOnCombobox)
        self.comboBox_ctrAttribute.Bind(wx.EVT_COMBOBOX, self.comboBox_ctrAttributeOnCombobox)
        self.checkBox_All.Bind(wx.EVT_CHECKBOX, self.checkBox_AllOnCheckBox)
        self.checkBox_DualValues.Bind(wx.EVT_CHECKBOX, self.checkBox_DualValuesOnCheckBox)
        self.checkBox_NumericValues.Bind(wx.EVT_CHECKBOX, self.checkBox_NumericValuesOnCheckBox)
        self.checkBox_SeasonalNumericValues.Bind(wx.EVT_CHECKBOX, self.checkBox_SeasonalNumericValuesOnCheckBox)
        self.checkBox_DescriptorValues.Bind(wx.EVT_CHECKBOX, self.checkBox_DescriptorValuesOnCheckBox)
        self.checkBox_ElectronicFiles.Bind(wx.EVT_CHECKBOX, self.checkBox_ElectronicFilesOnCheckBox)
        self.checkBox_TimeSeries.Bind(wx.EVT_CHECKBOX, self.checkBox_TimeSeriesOnCheckBox)
        self.checkBox_MultiAttributeSeries.Bind(wx.EVT_CHECKBOX, self.checkBox_MultiAttributeSeriesOnCheckBox)
        self.comboBox_ctrlInstance.Bind(wx.EVT_COMBOBOX, self.comboBox_NetworkOnCombobox)
        self.FilePicker_searchDataValues.Bind(wx.EVT_FILEPICKER_CHANGED, self.FilePicker_searchDataValuesOnFileChanged)
        self.btn_Search_nodesLinks.Bind(wx.EVT_BUTTON, self.btn_Search_nodesLinksOnButtonClick)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.btn_cancelOnButtonClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def dlg_SearchDataValuesOnInitDialog(self, event):
        event.Skip()

    def checkBox_NodesOnCheckBox(self, event):
        event.Skip()

    def checkBox_LinksOnCheckBox(self, event):
        event.Skip()

    def comboBox_ctrObjectTypeOnCombobox(self, event):
        event.Skip()

    def comboBox_ctrAttributeOnCombobox(self, event):
        event.Skip()

    def checkBox_AllOnCheckBox(self, event):
        event.Skip()

    def checkBox_DualValuesOnCheckBox(self, event):
        event.Skip()

    def checkBox_NumericValuesOnCheckBox(self, event):
        event.Skip()

    def checkBox_SeasonalNumericValuesOnCheckBox(self, event):
        event.Skip()

    def checkBox_DescriptorValuesOnCheckBox(self, event):
        event.Skip()

    def checkBox_ElectronicFilesOnCheckBox(self, event):
        event.Skip()

    def checkBox_TimeSeriesOnCheckBox(self, event):
        event.Skip()

    def checkBox_MultiAttributeSeriesOnCheckBox(self, event):
        event.Skip()

    def comboBox_NetworkOnCombobox(self, event):
        event.Skip()

    def FilePicker_searchDataValuesOnFileChanged(self, event):
        event.Skip()

    def btn_Search_nodesLinksOnButtonClick(self, event):
        event.Skip()

    def btn_cancelOnButtonClick(self, event):
        event.Skip()


###########################################################################
## Class dlg_ImportSpreadsheetAdvanced
###########################################################################

class dlg_ImportSpreadsheetAdvanced ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 66, title = u"Advanced: Import a select of tables", pos = wx.DefaultPosition, size = wx.Size( 620,434 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1711 = wx.StaticText( self, wx.ID_ANY, u"Check one or many boxes in numeric order to import data for any of the main WaMDaM tables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711.Wrap( -1 )
        bSizer15.Add( self.m_staticText1711, 0, wx.ALL, 5 )

        self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer15.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

        SizerMetadata = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3311 = wx.StaticText( self, wx.ID_ANY, u"1. Metadata tables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3311.Wrap( -1 )
        SizerMetadata.Add( self.m_staticText3311, 0, wx.ALL, 5 )

        gSizer44111 = wx.GridSizer( 1, 3, 0, 0 )

        self.checkBox_OrganizationsPeopleT = wx.CheckBox( self, 67, u"1.1 Organizations and People", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_OrganizationsPeopleT.SetValue(True)
        gSizer44111.Add( self.checkBox_OrganizationsPeopleT, 1, wx.ALL, 5 )

        self.checkBox_MethodsT = wx.CheckBox( self, 68, u"1.2 Methods", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_MethodsT.SetValue(True)
        gSizer44111.Add( self.checkBox_MethodsT, 0, wx.ALL, 5 )

        self.checkBox_SourcesT = wx.CheckBox( self, 69, u"1.3 Sources", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_SourcesT.SetValue(True)
        gSizer44111.Add( self.checkBox_SourcesT, 0, wx.ALL, 5 )


        SizerMetadata.Add( gSizer44111, 1, wx.EXPAND, 5 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerMetadata.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerMetadata.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText171111 = wx.StaticText( self, wx.ID_ANY, u"2. Data Structure tables ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171111.Wrap( -1 )
        SizerMetadata.Add( self.m_staticText171111, 0, wx.ALL, 5 )


        bSizer15.Add( SizerMetadata, 1, wx.EXPAND, 5 )

        SizerDataStructure = wx.GridSizer( 1, 4, 0, 0 )

        self.checkBox_DatasetT = wx.CheckBox( self, 70, u"2.1 Dataset", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_DatasetT.SetValue(True)
        SizerDataStructure.Add( self.checkBox_DatasetT, 1, wx.ALL, 5 )

        self.checkBox_ObjectTypesT = wx.CheckBox( self, 71, u"2.2 ObjectTypes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_ObjectTypesT.SetValue(True)
        SizerDataStructure.Add( self.checkBox_ObjectTypesT, 0, wx.ALL, 5 )

        self.checkBox_AttributesT = wx.CheckBox( self, 72, u"2.3 Attributes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_AttributesT.SetValue(True)
        SizerDataStructure.Add( self.checkBox_AttributesT, 0, wx.ALL, 5 )


        bSizer15.Add( SizerDataStructure, 1, wx.EXPAND, 5 )

        SizerNetworks = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerNetworks.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerNetworks.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText171112 = wx.StaticText( self, wx.ID_ANY, u"3. Network tables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText171112.Wrap( -1 )
        SizerNetworks.Add( self.m_staticText171112, 0, wx.ALL, 5 )

        gSizer4412 = wx.GridSizer( 1, 4, 0, 0 )

        self.checkBox_NetworksT = wx.CheckBox( self, 73, u"3.1 Networks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_NetworksT.SetValue(True)
        gSizer4412.Add( self.checkBox_NetworksT, 1, wx.ALL, 5 )

        self.checkBox_ScenariosT = wx.CheckBox( self, 74, u"3.2 Scenarios", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_ScenariosT.SetValue(True)
        gSizer4412.Add( self.checkBox_ScenariosT, 0, wx.ALL, 5 )

        self.checkBox_NodesT = wx.CheckBox( self, 75, u"3.3 Nodes", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_NodesT.SetValue(True)
        gSizer4412.Add( self.checkBox_NodesT, 0, wx.ALL, 5 )

        self.checkBox_LinksT = wx.CheckBox( self, 76, u"3.4 Links", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_LinksT.SetValue(True)
        gSizer4412.Add( self.checkBox_LinksT, 0, wx.ALL, 5 )


        SizerNetworks.Add( gSizer4412, 1, wx.EXPAND, 5 )


        bSizer15.Add( SizerNetworks, 1, wx.EXPAND, 5 )

        SizerDataValues = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline15 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerDataValues.Add( self.m_staticline15, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline151 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerDataValues.Add( self.m_staticline151, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText1711112 = wx.StaticText( self, wx.ID_ANY, u"4. Data Values tables ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1711112.Wrap( -1 )
        SizerDataValues.Add( self.m_staticText1711112, 0, wx.ALL, 5 )

        gSizer44113 = wx.GridSizer( 2, 4, 0, 0 )

        self.checkBox_BinaryT = wx.CheckBox( self, 78, u"4. Boolean", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_BinaryT.SetValue(True)
        gSizer44113.Add( self.checkBox_BinaryT, 0, wx.ALL, 5 )

        self.checkBox_ParametersT = wx.CheckBox( self, 79, u"4. Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_ParametersT.SetValue(True)
        gSizer44113.Add( self.checkBox_ParametersT, 0, wx.ALL, 5 )

        self.checkBox_SeasonalParametersT = wx.CheckBox( self, 80, u"4. SeasonalParameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_SeasonalParametersT.SetValue(True)
        gSizer44113.Add( self.checkBox_SeasonalParametersT, 0, wx.ALL, 5 )

        self.checkBox_DescriptorValuesT = wx.CheckBox( self, 81, u"4. DescriptorValues", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_DescriptorValuesT.SetValue(True)
        gSizer44113.Add( self.checkBox_DescriptorValuesT, 0, wx.ALL, 5 )

        self.checkBox_TextFreeT = wx.CheckBox( self, 82, u"4. TextFree", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_TextFreeT.SetValue(True)
        gSizer44113.Add( self.checkBox_TextFreeT, 0, wx.ALL, 5 )

        self.checkBox_FilesT = wx.CheckBox( self, 83, u"4. Files", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_FilesT.SetValue(True)
        gSizer44113.Add( self.checkBox_FilesT, 0, wx.ALL, 5 )

        self.checkBox_TimeSereisT = wx.CheckBox( self, 84, u"4. TimeSeriesData", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_TimeSereisT.SetValue(True)
        gSizer44113.Add( self.checkBox_TimeSereisT, 0, wx.ALL, 5 )

        self.checkBox_MultiColumnsArraysT = wx.CheckBox( self, 85, u"4. MultiVariableSeries", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkBox_MultiColumnsArraysT.SetValue(True)
        gSizer44113.Add( self.checkBox_MultiColumnsArraysT, 0, wx.ALL, 5 )


        SizerDataValues.Add( gSizer44113, 0, 0, 5 )

        self.m_staticline14 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        SizerDataValues.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer15.Add( SizerDataValues, 1, wx.EXPAND, 5 )

        Sizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_LoadTables = wx.Button( self, 86, u"Load data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_LoadTables.Enable( False )

        Sizer111.Add( self.btn_LoadTables, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_done = wx.Button( self, 87, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        Sizer111.Add( self.btn_done, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer15.Add( Sizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer15 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.checkBox_OrganizationsPeopleT.Bind( wx.EVT_CHECKBOX, self.checkBox_OrganizationsPeopleTOnCheckBox )
        self.checkBox_MethodsT.Bind( wx.EVT_CHECKBOX, self.checkBox_MethodsTOnCheckBox )
        self.checkBox_SourcesT.Bind( wx.EVT_CHECKBOX, self.checkBox_SourcesTOnCheckBox )
        self.checkBox_DatasetT.Bind( wx.EVT_CHECKBOX, self.checkBox_DatasetTOnCheckBox )
        self.checkBox_ObjectTypesT.Bind( wx.EVT_CHECKBOX, self.checkBox_ObjectTypesTOnCheckBox )
        self.checkBox_AttributesT.Bind( wx.EVT_CHECKBOX, self.checkBox_AttributesTOnCheckBox )
        self.checkBox_NetworksT.Bind( wx.EVT_CHECKBOX, self.checkBox_NetworksTOnCheckBox )
        self.checkBox_ScenariosT.Bind( wx.EVT_CHECKBOX, self.checkBox_ScenariosTOnCheckBox )
        self.checkBox_NodesT.Bind( wx.EVT_CHECKBOX, self.checkBox_NodesTOnCheckBox )
        self.checkBox_LinksT.Bind( wx.EVT_CHECKBOX, self.checkBox_LinksTOnCheckBox )
        self.checkBox_BinaryT.Bind( wx.EVT_CHECKBOX, self.checkBox_BinaryTOnCheckBox )
        self.checkBox_ParametersT.Bind( wx.EVT_CHECKBOX, self.checkBox_ParametersTOnCheckBox )
        self.checkBox_SeasonalParametersT.Bind( wx.EVT_CHECKBOX, self.checkBox_SeasonalParametersTOnCheckBox )
        self.checkBox_DescriptorValuesT.Bind( wx.EVT_CHECKBOX, self.checkBox_DescriptorValuesTOnCheckBox )
        self.checkBox_TextFreeT.Bind( wx.EVT_CHECKBOX, self.checkBox_TextFreeTOnCheckBox )
        self.checkBox_FilesT.Bind( wx.EVT_CHECKBOX, self.checkBox_FileBasedTOnCheckBox )
        self.checkBox_TimeSereisT.Bind( wx.EVT_CHECKBOX, self.checkBox_TimeSereisTOnCheckBox )
        self.checkBox_MultiColumnsArraysT.Bind( wx.EVT_CHECKBOX, self.checkBox_MultiColumnsArraysTOnCheckBox )
        self.btn_LoadTables.Bind( wx.EVT_BUTTON, self.btn_LoadTablesOnButtonClick )
        self.btn_done.Bind( wx.EVT_BUTTON, self.btn_doneOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def checkBox_OrganizationsPeopleTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_MethodsTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_SourcesTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_DatasetTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_ObjectTypesTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_AttributesTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_NetworksTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_ScenariosTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_NodesTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_LinksTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_BinaryTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_ParametersTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_SeasonalParametersTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_DescriptorValuesTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_TextFreeTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_FileBasedTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_TimeSereisTOnCheckBox( self, event ):
        event.Skip()

    def checkBox_MultiColumnsArraysTOnCheckBox( self, event ):
        event.Skip()

    def btn_LoadTablesOnButtonClick( self, event ):
        event.Skip()

    def btn_doneOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_ImportRwise
###########################################################################

class dlg_ImportRwise ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 88, title = u"Import a Rwise data", pos = wx.DefaultPosition, size = wx.Size( 554,321 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Select the Rwise file", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer14.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.FilePicker_RwiseFile = wx.FilePickerCtrl( self, 89, os.getcwdu(), u"Select a file", u"*.wml | *.WML", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_RwiseFile.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer14.Add( self.FilePicker_RwiseFile, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_LoadRwiseFile = wx.Button( self, 90, u"Load data", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_LoadRwiseFile, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 91, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_RwiseFile.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_RwiseFileOnFileChanged )
        self.btn_LoadRwiseFile.Bind( wx.EVT_BUTTON, self.btn_LoadRwiseFileOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_RwiseFileOnFileChanged( self, event ):
        event.Skip()

    def btn_LoadRwiseFileOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_ShapefileToWaMDaM
###########################################################################

class dlg_ShapefileToWaMDaM ( wx.Dialog ):

    def __init__( self, parent ):

        wx.Dialog.__init__ ( self, parent, id = 92, title = u"Convert Shapefile Data To WaMDaM spreadsheet", pos = wx.DefaultPosition, size = wx.Size( 554,321 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Select the shapefile data in a spreadsheet ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer14.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.FilePicker_ShapefileToWaMDaM = wx.FilePickerCtrl( self, 93, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_ShapefileToWaMDaM.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer14.Add( self.FilePicker_ShapefileToWaMDaM, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_ConvertShapefileData = wx.Button( self, 94, u"Convert data", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_ConvertShapefileData, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 95, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_ShapefileToWaMDaM.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_ShapefileToWaMDaMOnFileChanged )
        self.btn_ConvertShapefileData.Bind( wx.EVT_BUTTON, self.btn_ConvertShapefileDataOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_ShapefileToWaMDaMOnFileChanged( self, event ):
        event.Skip()

    def btn_ConvertShapefileDataOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_CrossTabSeasonalToWaMDaM
###########################################################################

class dlg_CrossTabSeasonalToWaMDaM ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 96, title = u"Convert CrossTabulated Seasonal data To WaMDaM spreadsheet", pos = wx.DefaultPosition, size = wx.Size( 554,321 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Select the cross-tabulated spreadsheet", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer14.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.FilePicker_CrossTabSeasonalToWaMDaM = wx.FilePickerCtrl( self, 97, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_CrossTabSeasonalToWaMDaM.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer14.Add( self.FilePicker_CrossTabSeasonalToWaMDaM, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_convertCrossTabulatedSeasonal = wx.Button( self, 98, u"Convert data", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_convertCrossTabulatedSeasonal, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 99, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_CrossTabSeasonalToWaMDaM.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_CrossTabulatedraFileOnFileChanged )
        self.btn_convertCrossTabulatedSeasonal.Bind( wx.EVT_BUTTON, self.btn_convertCrossTabulatedSeasonalOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_CrossTabulatedraFileOnFileChanged( self, event ):
        event.Skip()

    def btn_convertCrossTabulatedSeasonalOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_CrossTabTimeSeriesToWaMDaM
###########################################################################

class dlg_CrossTabTimeSeriesToWaMDaM ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 100, title = u"Convert CrossTabulated Time Series data To WaMDaM spreadsheet", pos = wx.DefaultPosition, size = wx.Size( 554,321 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Select the cross-tabulated spreadsheet", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer14.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.FilePicker_CrossTabTimeSeriesToWaMDaM = wx.FilePickerCtrl( self, 101, os.getcwdu(), u"Select a file", u"Excel files (*.xlsx ,*.xlsm, *.xls)|*.xlsx;*.xlsm;*.xls|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        ctrl = self.FilePicker_CrossTabTimeSeriesToWaMDaM.GetTextCtrl()
        ctrl.SetLabel("")
        bSizer14.Add( self.FilePicker_CrossTabTimeSeriesToWaMDaM, 0, wx.ALL|wx.EXPAND, 5 )

        gSizer111 = wx.GridSizer( 1, 2, 1, 1 )

        self.btn_ConvertCrossTabTimeSeriesToWaMDaM = wx.Button( self, 102, u"Convert data", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_ConvertCrossTabTimeSeriesToWaMDaM, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

        self.btn_cancel = wx.Button( self, 103, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer111.Add( self.btn_cancel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( gSizer111, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.FilePicker_CrossTabTimeSeriesToWaMDaM.Bind( wx.EVT_FILEPICKER_CHANGED, self.FilePicker_RwiseFileOnFileChanged )
        self.btn_ConvertCrossTabTimeSeriesToWaMDaM.Bind( wx.EVT_BUTTON, self.btn_ConvertCrossTabTimeSeriesToWaMDaMOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def FilePicker_RwiseFileOnFileChanged( self, event ):
        event.Skip()

    def btn_ConvertCrossTabTimeSeriesToWaMDaMOnButtonClick( self, event ):
        event.Skip()

    def btn_cancelOnButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_About
###########################################################################

class dlg_About ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 104, title = u"About WaMDaM", pos = wx.DefaultPosition, size = wx.Size( 646,488 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"The Water Management Data Model (WaMDaM) is a data model to consistency organize and synthesize disparate water management data for virtually any spatial boundary. These data are for node and link networks with attributes that have data types of, parameters, seasonal parameters, text free, text controlled, file based, rules, time series, and multi column arrays.   \n  \nOrganizing data into WaMDaM helps users to systematically search for their data that has contextual metadata to correctly interpret it   \n  \nThis WaMDaM Data Loader helps users to load their data into WaMDaM database through a user-friendly interface.   \n  \nThe source code and documentation of WaMDaM and its Data Loader are provided @ https://github.com/WamdamProject/WaMDaM-software-ecosystem and disturbed under a BSD 3-Clause license. All Rights Reserved.  \n  \nWaMDaM was designed and tested at Utah Water Research Laboratory at Utah State University and was funded by the the National Science Foundation as part of the CI-Water Project @ http://ci-water.org \n  \nDevelopent Team: Adel M. Abdallah and David E. Rosenberg @ http://rosenberg.usu.edu \nFor any questions, email Adel @ amabdallah@aggiemail.usu.edu  or visit his site @ adelmabdallah.com \n \nDisclaimers:   \n*Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.  \n*This software has been tested but it comes without any warranty", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer10.Add( self.m_staticText7, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )


        bSizer10.Add( bSizer24, 1, wx.EXPAND, 5 )

        sdbSizer_AboutOK = wx.StdDialogButtonSizer()
        self.sdbSizer_AboutOKOK = wx.Button( self, wx.ID_OK )
        sdbSizer_AboutOK.AddButton( self.sdbSizer_AboutOKOK )
        sdbSizer_AboutOK.Realize();

        bSizer10.Add( sdbSizer_AboutOK, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer10 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.sdbSizer_AboutOKOK.Bind( wx.EVT_BUTTON, self.sdbSizer_AboutOKOnOKButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def sdbSizer_AboutOKOnOKButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_Help
###########################################################################

class dlg_Help ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 105, title = u"Help", pos = wx.DefaultPosition, size = wx.Size( 646,488 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Check out the instructions here at http://docs.wamdam.org/Getting_started/Steps/", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer10.Add( self.m_staticText7, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )


        bSizer10.Add( bSizer24, 1, wx.EXPAND, 5 )

        sdbSizer_AboutOK = wx.StdDialogButtonSizer()
        self.sdbSizer_AboutOKOK = wx.Button( self, wx.ID_OK )
        sdbSizer_AboutOK.AddButton( self.sdbSizer_AboutOKOK )
        sdbSizer_AboutOK.Realize();

        bSizer10.Add( sdbSizer_AboutOK, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer10 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.sdbSizer_AboutOKOK.Bind( wx.EVT_BUTTON, self.sdbSizer_AboutOKOnOKButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def sdbSizer_AboutOKOnOKButtonClick( self, event ):
        event.Skip()


###########################################################################
## Class dlg_License
###########################################################################

class dlg_License ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = 106, title = u"WaMDaM License", pos = wx.DefaultPosition, size = wx.Size( 646,538 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"License\n\nCopyright (c) 2018, Utah State University and WaMDaM development team: Adel M. Abdallah and David E. Rosenberg All rights reserved.\n\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\nRedistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n\nRedistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\nNeither the name of Utah State University, WaMDaM, nor its contributors may be used to endorse or promote products derived from this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer10.Add( self.m_staticText7, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer24 = wx.BoxSizer( wx.VERTICAL )


        bSizer10.Add( bSizer24, 1, wx.EXPAND, 5 )

        sdbSizer_AboutOK = wx.StdDialogButtonSizer()
        self.sdbSizer_AboutOKOK = wx.Button( self, wx.ID_OK )
        sdbSizer_AboutOK.AddButton( self.sdbSizer_AboutOKOK )
        sdbSizer_AboutOK.Realize();

        bSizer10.Add( sdbSizer_AboutOK, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer10 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.sdbSizer_AboutOKOK.Bind( wx.EVT_BUTTON, self.sdbSizer_AboutOKOnOKButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def sdbSizer_AboutOKOnOKButtonClick( self, event ):
        event.Skip()

