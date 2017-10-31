# loadDescriptorValues.py

# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required variables (this are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *


class LoadDescriptorValues(Parse_Excel_File, LoadingUtils):
    """
    Class used to load LoadDescriptorValues data to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadDescriptorValues Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadDescriptorValues, self).__init__(filename)
        self.setup = DB_Setup()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[3]])

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
        :return: None
        """
        for sheet_name, sheet_rows in self.work_sheet.items():
            temp = sheet_rows[:]
            # Detecting start of data in the sheet
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]
                if 'DescriptorValues_table' in temp_row:
                    temp = sheet_rows[row_id + 4:]
                    break

            # Ensuring there is at least a single row of data in the sheet.
            if len(temp) < 1:
                continue
            temp_row = [cell.value for cell in temp[0]]
            temp_row.pop(2)
            stored_rows = [temp_row[:-1]]
            scenario_name = temp[0][2]

            for row_id, row in enumerate(temp):

                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:-1]):
                    continue

                if row[6].value is None or row[6].value == '' or row[6].value == ' ' or row[6].value == '  ':
                    continue

                if row[0].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[1].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[2].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[3].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[4].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[5].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))
                if row[6].value == "":
                    raise Exception(
                        'Error in {} row of "DescriptorValues_table" of  sheet "{}"\nField named "DescriptorValue" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                        .format(row_id, sheet_name))

                # test for datatype
                if not self.data_type_test(self.__session, row, 'DescriptorValues'):
                    raise Exception("'{}' attribute is not associated to {} Datatype".
                                    format(row[3].value, 'DescriptorValues'))

                diff_scene = False
                temp_row = [cell.value for cell in row[:]]
                temp_row.pop(2)

                # Checking row against stored rows to determine if its different or similar
                if temp_row[:-1] in stored_rows:
                    if row[2].value != scenario_name.value:
                        diff_scene = True
                else:
                    stored_rows.append(temp_row[:-1])

                textcontrol = SqlAlchemy.DescriptorValues()
                if row[6].value:
                    textcontrol.DescriptorValue = row[6].value
                else:
                    raise Exception('Error in descriptor value sheet, DescriptorValue column is required, '
                                    'Empty fields were found')

                attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session,
                                                                                         sheet_name, row_id)

                # Test if attrib belongs to object type
                self.test_properties(self.__session, row, sheet_name)

                # If the mapperID exists for the attribs in the current row, we then search if the value exists for
                # the row is stored in the db, if yes we then try to match with the mappingid to get datavaluemapper
                datavalues = self.__session.query(SqlAlchemy.Mapping).filter(
                    and_(
                        SqlAlchemy.Mapping.AttributeID == attrib_id,
                        SqlAlchemy.Mapping.InstanceID == instance_id,
                        SqlAlchemy.Mapping.SourceID == source_id,
                        SqlAlchemy.Mapping.MethodID == method_id
                    )
                ).all()

                value = None
                datavalues_id = None
                found = False
                try:
                    # skips searhing datavaluemapperid for required field if its attribs are not found in mapping table
                    if not datavalues:
                        raise Exception

                    # try getting the datavalue_id based on the required value to try getting the required mappingID
                    datavalues_id = self.__session.query(SqlAlchemy.DescriptorValues).filter(
                        SqlAlchemy.DescriptorValues.DescriptorValue == row[6].value
                    ).all()

                    result = [datavaluemapper.DataValuesMapperID for datavaluemapper in datavalues_id]

                    # check for mapping with same datavaluesmapper as the data value.
                    # if found, reuse of mapping id is emminent.
                    for mapping in datavalues:
                        if found:
                            break
                        for each in result[:]:
                            if mapping.DataValuesMapperID == each:
                                datavalues = mapping
                                found = True
                                break

                    # if the current value datvaluesmapperID is not found matching.
                    # if its not found, new entry is created
                    if not found:
                        raise Exception

                    value = True
                except Exception as e:
                    datavalues = None
                    datavalues_id = None

                # Creating New entry, datavaluemapperID and mappingID
                if not datavalues:
                    datavalmapper = self.load_data_values(self.__session)
                    dataval_map = SqlAlchemy.Mapping()
                    dataval_map.AttributeID = attrib_id
                    dataval_map.InstanceID = instance_id
                    dataval_map.SourceID = source_id
                    dataval_map.MethodID = method_id
                    if datavalues_id is None and not diff_scene:
                        # check if a descriptor value already exists when creating a new mapping.
                        # if both the DescriptorValue and the DescriptorValueCV together are identical,
                        # then share them among "Instances" within the same "Scenario" and across "Scenarios".
                        # If only the DescriptorValue is given, (no DescriptorValueCV with it in excel), then dont
                        # worry about sharing among instances of the same scenario
                        if row[6].value == row[7].value:
                            try:
                                datavalues_id = self.__session.query(SqlAlchemy.DescriptorValues).filter(
                                    SqlAlchemy.DescriptorValues.descriptorvalueCV == self.__session.query(
                                        SqlAlchemy.CV_DescriptorValues).
                                    filter(SqlAlchemy.CV_DescriptorValues.Name == row[6].value).
                                    first().Name
                                ).first().DataValuesMapperID
                                value = True
                            except:
                                pass
                        # if there the row is a different row it creates new datavaluemapperID for the new block
                        if not datavalues_id:
                            self.setup.push_data(datavalmapper)
                            datavalues_id = datavalmapper.DataValuesMapperID
                            dataval_map.DataValuesMapperID = datavalmapper.DataValuesMapperID
                        else:
                            dataval_map.DataValuesMapperID = datavalues_id
                    # If the row is not a different group, it reuses the previous datavalues
                    elif not diff_scene:
                        dataval_map.DataValuesMapperID = datavalues_id
                    self.setup.push_data(dataval_map)

                else:
                    datavalues_id = datavalues.DataValuesMapperID

                # Creating new scenariomapping if scenarioID-mappingID does not exists.
                # Starts by searchine for the mappingID in case its just been created, then tests to see if a
                # scenarioID-mappingID exists, if yes, it skips, if no, it creates an entry
                scenariomap = SqlAlchemy.ScenarioMapping()
                scenariomap.ScenarioID = scenario_id

                # if the row attribs are already mapped, then we reuse the mapping ID else we get the New ID created
                if datavalues:
                    scenariomap.MappingID = datavalues.MappingID
                else:
                    scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                        and_(
                            SqlAlchemy.Mapping.AttributeID == attrib_id,
                            SqlAlchemy.Mapping.InstanceID == instance_id,
                            SqlAlchemy.Mapping.SourceID == source_id,
                            SqlAlchemy.Mapping.MethodID == method_id,
                            SqlAlchemy.Mapping.DataValuesMapperID == datavalues_id
                        )
                    ).first().MappingID

                # test to ensure there is no scenarioID-mappingID relationship existing yet.
                try:
                    test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                        and_(
                            SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                            SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                        )
                    ).first().ScenarioMappingID
                except:
                    self.setup.push_data(scenariomap)

                if row[6].value:
                    # Add new entry to the database if the value is none(depicts similar scenario) and the value is not found
                    if not value:
                        try:
                            textcontrol.descriptorvalueCV = self.__session.query(
                                SqlAlchemy.CV_DescriptorValues).filter(
                                SqlAlchemy.CV_DescriptorValues.Name == row[7].value
                            ).first().Name
                        except:
                            pass

                        textcontrol.DataValuesMapperID = datavalues_id
                        self.setup.push_data(textcontrol)
                        value = False

    def add_data(self):
        self.setup.add_data()
