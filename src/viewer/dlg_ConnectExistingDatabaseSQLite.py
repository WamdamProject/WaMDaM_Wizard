"""Subclass of dlg_ConnectDatabaseSQLite, which is generated by wxFormBuilder."""

import wx
import os, define, sqlalchemy
from sqlalchemy.orm import relationship
import WaMDaMWizard
from controller.ConnectDB_ParseExcel import DB_Setup
from Messages_forms.msg_somethigWrong import msg_somethigWrong
from controller.wamdamAPI.GetComapreScenarios import GetComapreScenarios
from controller.HydroShare.PublishWaMDaM import publishOnHydraShare
import model.SqlAlchemy as SAlchemy
# Implementing dlg_ConnectDatabaseSQLite
class dlg_ConnectExistingDatabaseSQLite(WaMDaMWizard.dlg_ConnectExistingDatabaseSQLite):
    def __init__(self, parent):
        WaMDaMWizard.dlg_ConnectExistingDatabaseSQLite.__init__(self, parent)
        self.path = None
        self._session = None
        self.isCheckedSqlite = False

    # Handlers for dlg_ConnectDatabaseSQLite events.
    def FilePicker_ConnectSQLiteOnFileChanged(self, event):
        self.path = self.FilePicker_ConnectSQLite.GetPath()

    def btn_connectOnButtonClick(self, event):
        topframe = wx.GetApp().GetTopWindow()

        # print 'it is here and working'
        valid_extension = ['sqlite']

        # Check whether user select db correctly.
        if self.path == None or self.path == "":
            msg_somethigWrong(topframe, msg='Please select the existing SQLite database.').Show()
            return

        # Get name of db.
        db_name = self.path.split('\\')[-1]
        db_name = db_name.split('.')[0]
        define.logger = define.create_logger(db_name)
        define.logger.name = __name__
        define.logger.info("Start database connect.")

        # Get connection of db
        setup = DB_Setup()
        if setup.get_session():
            define.logger.error('Failed database connection.\n\nError: You are already connected to a database. \n\n to use another '
										'database, you need to disconnect from the current one')

            msg_somethigWrong(topframe, msg='\n\nError: You are already connected to a database. \n\n to use another '
										'database, you need to disconnect from the current one').Show()

        else:
            if self.path is not None and (self.path.split('.')[-1] in valid_extension):
                db = DB_Setup()
                self._session = db.connect(self.path, db_type='sqlite')

                if not self.check_database(self.path.split('\\')[-1]):
                    return

                topframe.SetTitle(topframe.GetTitle() + ' ::: You are connected to ' + os.path.basename(self.path))

                from Messages_forms.msg_connSQLiteSuccs import msg_connSQLiteSuccs
                msgdlg = msg_connSQLiteSuccs(topframe)
                msgdlg.setMessage(u"\n\n\n\n\nYou are successfully connected to " + self.path.split('\\')[-1] + u".")
                msgdlg.Show()
            else:
                from Messages_forms.msg_connSQLiteInvalid import msg_connSQLiteInvalid

                msg_connSQLiteInvalid(topframe).Show()
        define.logger.info("'" + self.path.split('\\')[-1] + "'was connected to successfully.\n")
        define.dbName = self.path.split('\\')[-1]
        self.Close()

    #Validate that the selected "existing SQLite file" conforms to WaMDaM structure and schema version
    # if the connection is sucecessful, return two parameters: sqlite file name and its local path on pc
    # we use thse parameters in the HydroShare script to uplaod the file and publish it
    def check_database(self, db_name):
        '''
        :param database name:
        :return: if database structure is same wandam return true, vise versa.
        '''
        try:
            temp = GetComapreScenarios()
            temp_session = temp.session

           # wandam version check. Check if the provided db complies with the version that the Wizard works for (version 1.0)
            sql = 'SELECT  DISTINCT  VersionNumber FROM "WaMDaMVersion"'
            result = temp_session.execute(sql)
            for row in result:
                if row.VersionNumber not in (1.05,1.06):
                    define.logger.error('Failed database connection.\n\nError: The database you are trying to connect to does not matched WaMDaM 1.05 schema version.')
                    raise Exception('\n\nError: The database you are trying to connect to does not matched WaMDaM 1.06 schema version')

            ''' get wandam classes'''
            from inspect import isclass
            class_names = [x for x in dir(SAlchemy) if isclass(getattr(SAlchemy, x))]
            extra_class_names = ["Column", "DateTime", "Float", "ForeignKey", "Integer", "Text", "create_engine",
                                 "BLOB", "Date", "relationship", "sessionmaker", "declarative_base", "SAWarning",
                                 "NullPool", "Base", "String"]

            result = temp_session.execute("SELECT name FROM sqlite_master WHERE type='table';")

            ''' get database table names'''
            table_names = []
            for row in result:
                table_names.append(row[0])

            ''' compare database table name and class name'''
            for class_name in class_names:
                if extra_class_names.__contains__(class_name):
                    continue
                if not table_names.__contains__(class_name):  # and not extra_class_names.__contains__(table_name):
                    define.logger.error('Failed database connection.\n\nError: {} table does not exist in database of WaMDaM 1.03 version.\n'
                                        'Therefore you can not connect with {}.'.format(class_name, db_name))
                    msg = '\n\nError: {} does not exist in the current WaMDaM 1.03 version.\n Therefore you can not connect with {}.'.format(class_name, db_name)
                    raise Exception(msg)

                # if not extra_class_names.__contains__(table_name):
                class_instance = getattr(SAlchemy, class_name)
                members = class_instance.__table__.columns.keys()

                ''' compare database table fields name and class attributes name'''
                import sqlite3
                connection = sqlite3.connect(self.path)
                cursor = connection.execute('select * from {}'.format(class_name))
                field_names = [description[0] for description in cursor.description]

                for member in members:
                    if not field_names.__contains__(member):
                        define.logger.error('Failed database connection.\n\nError: {} field does not exist in "{}" table.\n'
                                            'Therefore You can not connect with {}.'.format(member, class_name, db_name))
                        msg='\n\nError: {} field does not exist in "{}" table.\n Therefore You can not connect with {}.'.format(member, class_name, db_name)
                        raise Exception(msg)
                pass
            self.isCheckedSqlite = True
            return True
        except Exception as e:
            msg = e.message.replace("(sqlite3.OperationalError)", "")
            msg_somethigWrong(None, msg=msg).Show()
            conn = DB_Setup()
            if conn.get_session():
                conn.close_db()
            return False

    def btn_cancelOnButtonClick(self, event):
        self.Close()

    def btn_publishOnButtonClick(self, event):
        if not self.isCheckedSqlite:
            msg = "Please check if the selected sqlite file is a correct file."
            msg_somethigWrong(None, msg=msg).Show()
            return

        publishOnHydraShare((self.path))
