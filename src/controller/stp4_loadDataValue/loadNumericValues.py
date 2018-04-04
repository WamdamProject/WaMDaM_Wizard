
# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required variables (this are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *

from model import SqlAlchemy


class LoadNumericValues(Parse_Excel_File, LoadingUtils):
    """
    Class used to load NumericValues data to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadNumericValues Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadNumericValues, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[0]])

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
                if 'NumericValues_table' in temp_row:
                    temp = sheet_rows[row_id + 4:]
                    break

            if len(temp) < 1:
                continue
            # rows are stored for comparison to determine if a row is similar to others or different
            temp_row = [cell.value for cell in temp[0]]
            temp_row.pop(2)
            stored_rows = [temp_row]
            scenario_name = temp[0][2]

            for row_id, row in enumerate(temp):

                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:-1]):
                    raise Exception("Some empty fields where found in NumericValues.\n Please fill all Required")

                if row[-1].value is None:
                    continue

                if row[0].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[1].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[2].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[3].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[4].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[5].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[6].value == "":
                    raise Exception('Error in {} row of "NumericValues_table" of  sheet "{}"\nField named "NumericValue" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))

                # test for datatype
                if not self.data_type_test(self.__session, row, 'NumericValues'):
                    raise Exception("'{}' attribute is not associated to {} Datatype".
                                    format(row[3].value, 'NumericValues'))

                diff_scene = False
                temp_row = [cell.value for cell in row[:]]
                temp_row.pop(2)

                # Checking row against stored rows to determine if its different or similar
                for each in stored_rows:
                    if temp_row == each:  # checking if current row is same as any previous rows
                        if row[2].value != scenario_name.value:  # basing difference in terms of scenario name
                            diff_scene = True
                            break
                        break

                stored_rows.append(temp_row)

                params = SqlAlchemy.NumericValues()
                attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session, sheet_name, row_id)

                # Test if the provided attribute name belongs to object type
                self.test_properties(self.__session, row, sheet_name)

                # getting datavaluemapper id using the above params fro Mapping table
                datavalues = self.__session.query(SqlAlchemy.Mappings).filter(
                    and_(
                        SqlAlchemy.Mappings.AttributeID == attrib_id,
                        SqlAlchemy.Mappings.InstanceID == instance_id,
                        SqlAlchemy.Mappings.SourceID == source_id,
                        SqlAlchemy.Mappings.MethodID == method_id
                    )
                ).all()

                '''
                    The Idea in creating link between tables used here is to query the datavalue
                    table to get the DataValueMapperID for the current value.
                    if the value already exists in the table, the Mapping id is
                    selected and loaded with the scenario id else a new record
                    is created in the Mapping table and link in the scenarioMapping
                    table.
                '''

                value = None
                datavalues_id = None

                found = False
                try:
                    # skips searching datavaluemapperid for required field if its attribs are not found in mapping table
                    # this means a new datavaluemapperID will be created. this occurs when the ros is different
                    if not datavalues:
                        raise Exception

                    # If the mapperID exists for the attribs in the current row, we then search if the value exists for
                    # the row is stored in the db, if yes we then try to match with the mappingid to get datavaluemapper
                    datavalues_id = self.__session.query(SqlAlchemy.NumericValues).filter(
                        SqlAlchemy.NumericValues.NumericValue == row[6].value
                    ).all()

                    result = [datavaluemapper.ValuesMapperID for datavaluemapper in datavalues_id]

                    # check for mapping with same ValuesMapper as the data value.
                    # if found, reuse of mapping id is emminent.
                    for mapping in datavalues:
                        if found:
                            break
                        for each in result[:]:
                            if mapping.ValuesMapperID == each:
                                datavalues = mapping
                                found = True
                                break

                    # if the current value datvaluesmapperID is not found matching.
                    # if its not found, A trigger is sent for new entry creation
                    if not found:
                        raise Exception

                    value = True
                except Exception as e:
                    datavalues = None
                    datavalues_id = None

                # if the current row combination does not exists in mapping table, a new entry is created
                if not datavalues and not diff_scene:
                    datavalmapper = self.load_data_values(self.__session)
                    dataval_map = SqlAlchemy.Mappings()
                    dataval_map.AttributeID = attrib_id
                    dataval_map.InstanceID = instance_id
                    dataval_map.SourceID = source_id
                    dataval_map.MethodID = method_id

                    # creating new datavaluemapper if the row is in a different block
                    if datavalues_id is None and not diff_scene:
                        self.setup.push_data(datavalmapper)
                        datavalues_id = datavalmapper.ValuesMapperID
                        dataval_map.ValuesMapperID = datavalmapper.ValuesMapperID
                    elif not diff_scene:
                        dataval_map.ValuesMapperID = datavalues_id
                    self.setup.push_data(dataval_map)

                else:
                    datavalues_id = datavalues.ValuesMapperID

                # Creating new scenariomapping if scenarioID-mappingID does not exists.
                # Starts by searchine for the mappingID in case its just been created, then tests to see if a
                # scenarioID-mappingID exists, if yes, it skips, if no, it creates an entry
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
                            SqlAlchemy.Mappings.MethodID == method_id,
                            SqlAlchemy.Mappings.ValuesMapperID == datavalues_id
                        )
                    ).first().MappingID

                # test to see if the current mappingid - scenarioid association exists in scenariomapping table
                try:
                    test = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                        and_(
                            SqlAlchemy.ScenarioMappings.MappingID == scenariomap.MappingID,
                            SqlAlchemy.ScenarioMappings.ScenarioID == scenariomap.ScenarioID
                        )
                    ).first().ScenarioMappingID
                except:
                    self.setup.push_data(scenariomap)

                if row[6].value is not None:
                    # value is a boolean variable which tells if a datavalue is already in the database,
                    # if value if false, it is added to the db, also if row is different from previously
                    # loaded rows, that current row is also added to the database.
                    if not value or not diff_scene:
                        params.NumericValue = row[6].value
                        params.ValuesMapperID = datavalues_id
                        self.setup.push_data(params)
                        value = False
                else:
                    raise Exception(
                        'Error in sheet "{}"\n field named "NumericValue" is empty.\nThis field should not be empty.'
                        '\nPlease fill this field to a value'.format(sheet_name))

    def add_data(self):
        self.setup.add_data()
