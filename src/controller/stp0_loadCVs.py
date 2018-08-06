# -*- coding: utf-8 -*-#
import sys
import unicodedata

'''
    The stp0_loadCVs.py file is used to load Control values excel sheets
    to the sqlite database using sqlalchemy.
    It Inherits properties from the Parse_Excel_File and DB_Setup
    classes.
    I- Load_CV_To_DB():  This is the class for loading CV data in this file.
                        it inherits methods for two other classes so as
                        to achieve its task. This class is made up of a
                        constructor used to initialize its self and its
                        inherited classes, setup the session which is a
                        private variable and also initialize the work_sheet
                        variable which holds all data from sheets in the
                        excel files.

        Important methods and variables of the class:
        -> load_data():  This is a method which does all the processing of each CV data.
                        it functions by iterating through the work_sheet dictionary, and
                        for each sheet parse the data appropriately so as to store in the
                        required table and fields.
        -> work_sheet:  This a dictionary having cv sheetnames as keys and the sheet
                        data as values. its data is gotten from the
                        parse_object_control_value() method found in Parse_Excel_File class.
        -> __session:    Session variables (private) used to access the database.
'''

# We Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from .ConnectDB_ParseExcel import *

from .ReadWorkbook_SheetsNames import *

import urllib2

import csv


# ****************************************************************************************************************** #
#                                                                                                                    #
#                                         Script Begins here                                                         #
#                                                                                                                    #
# ****************************************************************************************************************** #


class Load_CV_To_DB(Parse_Excel_File):
    """
        Class used to load Load_Data_Values to the database tables.

        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        super(Load_CV_To_DB, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        # self.work_sheet = self.parse_object_control_value(DataValues_ordered[:])

    def load_cv(self, model, row, result):
        try:
            if len(row) > 1 and not row[1] in result:
                if row[0] and row[1] is not None:
                    model.Term = row[0]
                    model.Name = row[1]
                else:
                    raise Exception()
                model.Definition = unicodedata.normalize("NFKD", unicode(row[2], 'UTF-8')) \
                    .replace(u"\u2018", "'").replace(u"\u2019", "'")

                if len(row) > 3:
                    model.Category = unicodedata.normalize("NFKD", unicode(row[3], 'UTF-8')) \
                        .replace(u"\u2018", "'").replace(u"\u2019", "'")

                model.SourceVocabularyURI = row[5]
                if hasattr(model, "AttributeName"):
                    model.AttributeName = row[7]
                if hasattr(model, "BooleanValue"):
                    model.BooleanValue = row[7]
                if hasattr(model, "UnitSystem"):
                    model.UnitSystem = row[7]
            else:
                return None
        except Exception as e:
            print e
            raise Exception('Please some required fields are found empty in ' + key)

        return model

    def check_sync(self):
        """
        Check if the data in the db is same as that online for all
        the tables in the db
        :return:
        """

    def load_data(self):
        """
        This method is used to parse data from each sheet to its
        appropriate table in the database.
        Due to the structure of the excel file, some hard coding
        was done to get data accurately.
        It functions by iterating over the work_sheet dictionary
        and getting each corresponding sheet_name and sheetrows,
        then using if statements to test what sheet it is , afterwards
        the appropriate table is initialized and the table fields are
        loaded using data from the corresponding sheet.
        :return: None
        """
        try:
            for key, value in vocab.items():
                # Defining the URL to extract the csv files.
                url = 'http://vocabulary.wamdam.org/api/v1/{}/?format=csv'.format(key)
                # url = 'http://vocabulary.wamdam.org/'

                # check if db CV tables are empty. it suffices to check one table.
                # try:
                #     s = self.__session.query(SqlAlchemy.CV_AggregationStatistic).first().Name
                #     raise Exception('CV tables Not empty.')
                # except Exception as e:
                #     print 'it is here.'
                #     print e
                try:
                    response = urllib2.urlopen(url)
                except:
                    continue
                csv_content = csv.reader(response)
                cv_model = value

                if key == "aggregationstatistic":
                    result = self.__session.query(SqlAlchemy.CV_AggregationStatistic.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "attributedatatype":
                    result = self.__session.query(SqlAlchemy.CV_AttributeDataType.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "attributename":
                    result = self.__session.query(SqlAlchemy.CV_AttributeName.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)


                if key == "electronicfileformat":
                    result = self.__session.query(SqlAlchemy.CV_ElectronicFileFormat.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "instancename":
                    result = self.__session.query(SqlAlchemy.CV_InstanceName.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "methodtype":
                    result = self.__session.query(SqlAlchemy.CV_MethodType.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "objecttypology":
                    result = self.__session.query(SqlAlchemy.CV_ObjectTypology.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "objecttype":
                    result = self.__session.query(SqlAlchemy.CV_ObjectType.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "seasonname":
                    result = self.__session.query(SqlAlchemy.CV_SeasonName.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "spatialreference":
                    result = self.__session.query(SqlAlchemy.CV_SpatialReference.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "descriptorvalue":
                    result = self.__session.query(SqlAlchemy.CV_Categorical.Name).all()
                    # print result
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "units":
                    result = self.__session.query(SqlAlchemy.CV_Units.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)

                if key == "elevationdatum":
                    result = self.__session.query(SqlAlchemy.CV_ElevationDatum.Name).all()
                    result = [row[0] for row in result]
                    for row in list(csv_content)[1:]:
                        model = cv_model()
                        model = self.load_cv(model, row, result)
                        if model:
                            self.setup.push_data(model)
        except Exception as e:
            print e.message
    def add_data(self):
        self.setup.add_data('CV')
