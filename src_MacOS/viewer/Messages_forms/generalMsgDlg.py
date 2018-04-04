import wx
import wx.xrc

###########################################################################
## Class messageDlg
###########################################################################

class messageDlg ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title=u"Sorry: something went wrong", pos = wx.DefaultPosition, size = wx.Size( 458, 212 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )


        bSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        gSizer1 = wx.GridSizer( 1, 2, 0, 0 )

        self.btn_OK = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.btn_OK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.btn_Cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.btn_Cancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.btn_OK.Bind( wx.EVT_BUTTON, self.btn_okOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def btn_okOnButtonClick( self, event ):
        self.Destroy()
    def setMessage(self, msg):
        # strList = msg.split("\n")
        # resultStr = ""
        # for s in strList:
        #     if s.__len__() > 60:
        #         resultStr += s[:60] + "\n" + s[60:] + "\n"
        #         continue
        #     resultStr += s + "\n"


        self.m_staticText1.SetLabel(msg)