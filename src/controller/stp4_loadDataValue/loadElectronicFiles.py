#loadElectronicFiles.py

# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# The os library is used to get the file in the directory stored
import os

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required variables (this are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *

from model import SqlAlchemy


class LoadElectronicFiles(Parse_Excel_File, LoadingUtils):
    """
    Class used to load FileBase to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadFileBase Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadElectronicFiles, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[5]])

    def load_data(self):
        """
        This method is used to parse data from each sheet to its
        appropriate table in the database.
        Due to the structure of the excel file, some hard coding
        was done to get data accurately.
        It functions by iterating over the work_sheet dictionary
        and getting each corresponding sheet_name and sheetrows to
        load the table.
        It starts by querying for id's of the datavalue properties.
        then using some tests to load the data value appropriately to
        avoid data duplication and creating links between tables.
        It then concatenates the file name and append to the location
        provided. Using the os module, it opens the file and loads
        the data to the filebase table as a blob.
        :return: None
        """
        for sheet_name, sheet_rows in self.work_sheet.items():
            temp = sheet_rows[:]

            # Detecting start of data in the sheet
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]
                if 'ElectronicFiles_table' in temp_row:
                    temp = sheet_rows[row_id + 4:]
                    break

            for row_id, row in enumerate(temp):
                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:-1]):
                    raise Exception(
                        "Some empty fields where found in ElectronicFiles.\n Please fill all Required fields in " + sheet_name)

                if row[0].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[1].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[2].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[3].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[4].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[5].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[6].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "ElectronicFileName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[7].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "ElectronicFileFormatCV" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[8].value == "":
                    raise Exception('Error in {} row of "ElectronicFiles_table" of  sheet "{}"\nField named "FileLocationOnDesk" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))

                # test for datatype
                if not self.data_type_test(self.__session, row, 'File'):
                    raise Exception("'{}' attribute is not associated to {} Datatype".
                                    format(row[3].value, 'File'))

                file_base = SqlAlchemy.File()
                attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session, sheet_name, row_id)

                # Test if attrib belongs to object type
                self.test_properties(self.__session, row, sheet_name)

                # getting datavaluemapper id using the above params fro Mapping table
                datavalues = self.__session.query(SqlAlchemy.Mappings).filter(
                    and_(
                        SqlAlchemy.Mappings.AttributeID == attrib_id,
                        SqlAlchemy.Mappings.InstanceID == instance_id,
                        SqlAlchemy.Mappings.SourceID == source_id,
                        SqlAlchemy.Mappings.MethodID == method_id
                    )
                ).first()

                '''
                    The Idea in creating link used here is to query the datavalue
                    table to get the DataValueMapperID using a combination of
                    (aggregattionstatisticcvid, aggreationInterval, Internvaltimeunitcvid)
                    for the current value combination. Only required fields are considered.
                    if the value already exists in the table, the Mapping id is
                    selected and loaded with the scenario id else a new record
                    is created in the Mapping table and link in the scenarioMapping
                    table.
                '''

                value = None
                datavalues_id = None
                try:
                    datavalues_id = self.__session.query(SqlAlchemy.TextFree).filter(
                        and_(
                            SqlAlchemy.File.FileName == row[6].value,
                            SqlAlchemy.File.ElectronicFileFormatCV == self.__session.query(SqlAlchemy.CV_ElectronicFormat).filter(
                                SqlAlchemy.CV_ElectronicFormat.Name == row[7].value
                            ).first().Name
                        )
                    ).first().ValuesMapperID
                    value = True
                except Exception as e:
                    print e
                    raise Exception(e.message)

                if not datavalues:
                    datavalmapper = self.load_data_values(self.__session)
                    dataval_map = SqlAlchemy.Mappings()
                    dataval_map.AttributeID = attrib_id
                    dataval_map.InstanceID = instance_id
                    dataval_map.SourceID = source_id
                    dataval_map.MethodID = method_id

                    if datavalues_id is None:
                        self.setup.push_data(datavalmapper)
                        datavalues_id = datavalmapper.ValuesMapperID
                        dataval_map.ValuesMapperID = datavalmapper.ValuesMapperID
                    else:
                        dataval_map.ValuesMapperID = datavalues_id
                    self.setup.push_data(dataval_map)

                if not datavalues_id:
                    datavalues_id = datavalues.ValuesMapperID

                if row[5].value and row[6].value and row[7].value:
                    if not value:
                        file_base.FileName = row[6].value
                        file_base.ValuesMapperID = datavalues_id
                        file_base.ElectronicFileFormatCV = self.__session.query(SqlAlchemy.CV_ElectronicFormat).filter(
                            SqlAlchemy.CV_ElectronicFormat.Name == row[7].value
                        ).first().Name
                        file_base.Description = row[9].value

                        # getting file data and storing as blob in model
                        filename = row[6].value + '.' + row[7].value
                        file_path = os.path.join(row[8].value, filename)
                        fp = open(file_path, mode='rb')
                        data = fp.read()

                        file_base.File = data

                        self.setup.push_data(file_base)
                        value = False

                scenariomap = SqlAlchemy.ScenarioMappings()
                scenariomap.ScenarioID = scenario_id

                if datavalues:
                    scenariomap.MappingID = datavalues.MappingID
                else:
                    scenariomap.MappingID = self.__session.query(SqlAlchemy.Mappings).filter(
                        and_(
                            SqlAlchemy.Mappings.AttributeID == attrib_id,
                            SqlAlchemy.Mappings.InstanceID == instance_id,
                            SqlAlchemy.Mappings.SourceID == source_id,
                            SqlAlchemy.Mappings.MethodID == method_id
                        )
                    ).first().MappingID

                try:
                    test = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                        and_(
                            SqlAlchemy.ScenarioMappings.MappingID == scenariomap.MappingID,
                            SqlAlchemy.ScenarioMappings.ScenarioID == scenariomap.ScenarioID
                        )
                    ).first().ScenarioMappingID
                except:
                    self.setup.push_data(scenariomap)
    def add_data(self):
            self.setup.add_data()
