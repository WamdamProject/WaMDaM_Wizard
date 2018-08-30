"""
    The ConnectDB_ParseExcel.py file contain two very important classes used
    throughout all the classes in controller. these classes are:

    DB_Setup(): used to setup the database. It has methods which help
                get the active session, push and connect to the database
                through sqlalchemy (the Model)

    Parse_Excel_File(): Used to parse an excel workbook and return a
                        dictionary containing the sheetnames as keys and
                        the sheet rows as values. The sheetnames returned
                        are those sent to the parse_object_control_value()
                        method. other than those sheets no other sheet will
                        be returned. If a sheet is sent and not found in the
                        workbook, and error is raised 
                        (the workbook is different than what it is supposed to be) .
"""

# import the database params from SqlAlchemy.py found in the Model folder
from model import SqlAlchemy

# used to read an excel workbook (its pretty fast and works with xlsx and xlsm)
import xlrd as excel

# used to create an ordered dictionary [Why?]]
from collections import OrderedDict

# importing the sqlalchemy error package so as to catch errors
import sqlalchemy.exc as e

# Used to create an active session   [[not used anymore?? if so, delete]]
from sqlalchemy.orm import sessionmaker

# used to connect to the model       [[not used anymore?? if so, delete]]
from sqlalchemy import create_engine

from shutil import copyfile
import os

# Get only one copy of database class at a time and use it throughout the Wizard
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            # print "Singleton", cls._instances[cls]
        return cls._instances[cls]


# ****************************************************************************************************************** #
#                                                                                                                    #
#                                         Script Begins here                                                         #
#                                                                                                                    #
# ****************************************************************************************************************** #

class DB_Setup(object):
    '''
        class used to setup the database and
        persist data to the database
    '''
    __metaclass__ = Singleton
    __session = None
    #### MY CODE ####
    __path = None
    __type = None
    __backupName = None

    def __init__(self):
        pass

    def get_session(self):
        '''
            used to return an active session to
            the caller
        :return: active session
        '''
        return self.__session

    def get_dbpath(self):
        '''
            used to return an active session to
            the caller
        :return: active session
        '''
        return self.__path

    '''If the user cancels data loading in the middle, the thread might continue loading data
       for a bit of time until it finishes the job at hand. 
       The Data loader has a rule to load all or nothing. so if the user cancels in the middle, 
       then, the App, deletes the db which might have half loaded data, then it restores a backup db before 
       loading the new data'''

    def connect(self, dbpath, db_type, sql_string=None):
        self.__session = SqlAlchemy.connect(dbpath, db_type, sql_string)
        print dbpath, 'path'
        print db_type, 'type'
        print sql_string, 'string'
        self.__path = dbpath  # To be used later to backup the database.
        self.__type = db_type

    def add_data(self, table=None):
        '''
            used to commit data to the database
        :return: None
        '''
        try:
            self.__session.commit()
        except e.IntegrityError as error:
            self.__session.rollback()
            print error
            raise Exception('\n Duplicate entries found \n looks like some {} tables have already been loaded'
                            .format(table))

        except e and Exception as error:
            print error

    def push_data(self, obj):
        '''
        used to push data which pending commit.
        :param obj: a table instance of the model
        :return:
        '''
        try:
            self.__session.add(obj)
        except e and Exception as error:
            print error

    def remove_data(self, obj):  # [[[it has been updated.]]]
        """
        used to remove most failed instances and permit session rollback.
        NB!!! Not working yet
        :param obj:
        :return:
        """
        'TODO: Make this function to work'
        self.__session.flush()
        self.__session.delete(obj)
        self.__session.flush()
        self.__session.expunge(obj)

    def close_db(self):
        """
        used to close the model
        :return:
        """
        self.__session.close()
        self.__session.bind.dispose()
        self.__session = None

    def getType(self):
        return self.__type

    def backup_db(self):
        """
        used to backup the database before importing data into it.
        copies the current database, and renames it "currentname---backup"
        """
        src = self.__path
        filename = os.path.basename(src)
        f_name, ext = os.path.splitext(filename)
        new_fname = f_name + '---backup.' + ext
        path, filename = os.path.split(src)
        dst = path + '/' + new_fname
        # dst = src.split('.')[0] + '---backup.' + src.split('.')[-1]
        self.__backupName = dst
        print 'Backing up the DB\nsrc:{}\ndst:{}'.format(src, dst)
        copyfile(src, dst)

    def restore_db(self):
        """
        used to restore the database after the user cancels data loading.
        copies the backup database, and renames it "currentname" then
        connects to it, so the user can load more data safely.
        the thread does not exit immediately, it finishes the job at hand,
        then it exits, this is safe because if it exits the job in the middle
        it might cause a deadlock to the pc or any other issues
        """
        self.close_db()
        src = self.__backupName
        dst = src.split('---')[0] + '.' + src.split('.')[1]
        copyfile(src, dst)
        self.__session = SqlAlchemy.connect(dst, self.__type)


class Parse_Excel_File(object):
    '''
        this class is used to parse
        the excel workbook
    '''

    def __init__(self, obj):
        self.filename = None
        self.__workbook = obj
        self.__controlled_queries = list()
        self.__structure_queries = list()

    def open_file(self):
        """
        used to open a workbook
        :return: a pointer to the workbook
        """
        return excel.open_workbook(self.filename)

    def get_sheet(self, sheet_name):
        """
        used to return the contents of a worksheet
        to the calling function
        :param sheet_name:
        :return:
        """
        try:
            return self.__workbook.sheet_by_name(sheet_name)
        except:
            raise Exception("Cannot find sheet name {} in workbook \n Please select a valid workbook"
                            .format(sheet_name))

    def parse_object_control_value(self, sheet_names=None):
        """
        used to parse the workbook and create a dictionary
        of sheetname as keys and sheetrows as values [[why? to use it where?]]
        :param sheet_names:
        :return:
        """
        work_data = OrderedDict()
        for sheet_name in sheet_names:
            print sheet_name
            sheet = self.get_sheet(sheet_name)
            work_data[sheet_name] = [row for row in sheet.get_rows()]
        return work_data

