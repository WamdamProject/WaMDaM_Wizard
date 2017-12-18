'''
Disconnect the connection with the current SQLite db
Report the disconnection to the logfile

'''
import wx, define
import WaMDaMWizard
from controller.ConnectDB_ParseExcel import DB_Setup

class ExitDB(WaMDaMWizard.dlg_ExitDB):
    def __init__(self, parent):
        WaMDaMWizard.dlg_ExitDB.__init__(self, parent)
        self.path = None
        self._session = None

        self.disconnectResult = False

    # Handlers for dlg_ConnectDatabaseSQLite events.

    def btn_yesOnButtonClick(self, event):
        conn = DB_Setup()
        if conn.get_session():
            conn.close_db()

            if not conn.get_session():

                topframe = wx.GetApp().GetTopWindow()
                topframe.SetTitle(topframe.GetTitle().split(':')[0])

                self.disconnectResult = True
                from Messages_forms.msg_infos import  msg_infos
                msg_infos(topframe, msg='\nDatabase disconnected successfully\n\n"' + define.dbName + '" session has been disconnected').Show()

            else:
                from Messages_forms.msg_somethigWrong import msg_somethigWrong
                msg_somethigWrong(None, msg='"' + define.dbName + '"database disconnection failed').Show()

        else:
            from Messages_forms.msg_somethigWrong import msg_somethigWrong
            msg_somethigWrong(None, msg='No "' + define.dbName + '" Connection Found').Show()
        self.Close()
    def disconnect_DB(self):
        conn = DB_Setup()
        if conn.get_session():
            conn.close_db()
    def btn_cancelOnButtonClick(self, event):
        self.Close()