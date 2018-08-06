"""Subclass of dlg_ConnectNewDatabaseSQLite, which is generated by wxFormBuilder."""

import wx
import WaMDaMWizard
import os, define
from controller.ConnectDB_ParseExcel import DB_Setup
from Messages_forms.msg_somethigWrong import msg_somethigWrong
from model import SqlAlchemy


# Implementing dlg_ConnectNewDatabaseSQLite


class dlg_ConnectNewDatabaseSQLite(WaMDaMWizard.dlg_ConnectNewDatabaseSQLite):
    def __init__(self, parent):
        WaMDaMWizard.dlg_ConnectNewDatabaseSQLite.__init__(self, parent)

    # Handlers for dlg_ConnectNewDatabaseSQLite events.
    def dirPicker_newDBOnDirChanged(self, event):
        '''print '*************** it works ***************'''''

    def btn_connectOnButtonClick(self, event):
        topframe = wx.GetApp().GetTopWindow()
        dir_name = self.dirPicker_newDB.GetPath()
        db_name = self.m_textCtrl1.GetValue()

        # Check whether user select the file to write data correctly.
        fileCheck = False
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                if file.endswith(".sqlite"):
                    if file.split('.')[0] == db_name:
                        from Messages_forms.generalMsgDlg import messageDlg
                        errMsgDlg = messageDlg(topframe)
                        errMsgDlg.SetTitle("Error")
                        errMsgDlg.setMessage(
                            "This database name already exists in this directory.\nPlease choose a different database name!")
                        errMsgDlg.ShowModal()
                        return

        # Report connecting to the db in the logfile
        define.logger = define.create_logger(db_name)
        define.logger.name = __name__
        define.logger.info("Start database connection.")

        setup = DB_Setup()
        if setup.get_session():
            define.logger.error(
                'Failed database connection.\n\nError: You are already connected to a database. \n\n to use another'
                'database, you need to disconnect from the current one')
            msg_somethigWrong(topframe, msg='\n\nError: You are already connected to a database. \n\n to use another'
                                        'database, you need to disconnect from the current one').Show()
            return

        if not dir_name:
            define.logger.error(
                'Failed database connection.\n\nError: Please select a directory. \n\nIf already so, try using the "other..." '
                'option in the Dir Dialog')
            msg_somethigWrong(topframe,
                              msg='\n\nError: Please select a directory. \n\nIf already so, try using the "other..." '
                                  'option in the Dir Dialog').Show()
            return

        if not db_name:
            define.logger.error('Failed database connection.\n\nError: The database name is required.')
            msg_somethigWrong(topframe, msg='\n\n\nError: The database name is required.').Show()
            return

        if len(db_name.split('.')) > 1:
            if db_name.split('.')[-1] in ['sqlite']:
                pass
            else:
                db_name += '.sqlite'
        else:
            db_name += '.sqlite'

        # Get connection with db
        db_path = os.path.join(dir_name, db_name)
        db = DB_Setup()
        db.connect(db_path, db_type='sqlite')

        # Create WaMDaMVersion table and fills it the version number declared in define.py file
        obj_cat = SqlAlchemy.WaMDaMVersion()
        obj_cat.VersionNumber = define.version
        db.push_data(obj_cat)
        db.add_data()

        topframe.SetTitle(topframe.GetTitle() + ' ::: You are connected to ' + os.path.basename(db_name))

        from Messages_forms.msg_connSQLiteSuccs import msg_connSQLiteSuccs
        msgdlg = msg_connSQLiteSuccs(topframe)
        msgdlg.setMessage(u"\n\n\n\n\nYou are successfully connected to " + db_path.split('\\')[-1] + u".")
        msgdlg.Show()
        '''Report the connected db name to the logfile'''
        define.logger.info("'" + db_path.split('\\')[-1] + "'was connected successfully.\n")
        define.dbName = db_path.split('\\')[-1]
        self.Close()

    def btn_cancelOnButtonClick(self, event):
        self.Destroy()