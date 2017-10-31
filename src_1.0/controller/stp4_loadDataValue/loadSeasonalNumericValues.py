# loadSeasonalNumericValues.py

# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required variables (this are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *

from model import SqlAlchemy


class LoadSeasonalNumericValues(Parse_Excel_File, LoadingUtils):
    """
    Class used to load SeasonalParams to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadSeasonalParams Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadSeasonalNumericValues, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[1]])

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
                if 'SeasonalNumericValues_table' in temp_row:
                    temp = sheet_rows[row_id + 4:]
                    break

            if len(temp) < 1:
                continue
            # rows are stored for comparison to determine if a row is similar to others or different
            order_value = 0
            temp_row = [cell.value for cell in temp[0][:6]]  # stores from ojectInstance to Methodname for comparison
            order_row_test = temp_row[:6]
            stored_rows = [temp_row]
            scenario_name = temp[0][2]
            for row_id, row in enumerate(temp):

                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:7]):
                    raise Exception("Some empty fields were found in SeasonalNumericValues.\nPlease fill all Required fields")

                if row[-1].value is None:
                    continue

                if row[0].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[1].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[2].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[3].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[4].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[5].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[6].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "SeasonName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[7].value == "":
                    raise Exception('Error in {} row of "SeasonalNumericValues_table" of  sheet "{}"\nField named "SeasonNameCV" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))

                # test for datatype
                if not self.data_type_test(self.__session, row, 'SeasonalNumericValues'):
                    raise Exception("'{}' attribute is not associated to {} Datatype".
                                    format(row[3].value, 'SeasonalNumericValues'))

                diff_scene = False
                temp_row = [cell.value for cell in row[:6]]
                order_current_row = temp_row[:6]

                # TODO: make sure to store only the block in stored rows for comparison so that we can use for loop for unordered data.

                # Make block comparison to see if next block is same or different
                if temp_row != stored_rows[-1]:
                    diff_scene = True  # escaping creation of different datavaluemapperID for same block

                stored_rows.append(temp_row)  # Store new block in temp_row

                sparams = SqlAlchemy.SeasonalNumericValues()
                attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session, sheet_name, row_id)

                # Test if attrib belongs to object type
                self.test_properties(self.__session, row, sheet_name)

                # getting datavaluemapper id using the above params from Mapping table
                # this will be used to a datavaluemapperid to be reused if it already exists

                datavalues = self.__session.query(SqlAlchemy.Mapping).filter(
                    and_(
                        SqlAlchemy.Mapping.AttributeID == attrib_id,
                        SqlAlchemy.Mapping.InstanceID == instance_id,
                        SqlAlchemy.Mapping.SourceID == source_id,
                        SqlAlchemy.Mapping.MethodID == method_id
                    )
                ).order_by(SqlAlchemy.Mapping.MappingID.desc()).all()

                '''
                    The Idea in creating link used here is to query the datavalue
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
                    # if new row's attribs are not mapped yet, then it is a new block, we skip datavaluemap search
                    if not datavalues:
                        diff_scene = False
                        raise Exception

                    # If the mapperID exists for the attribs in the current row, we then search if the value exists for
                    # the row is stored in the db, if yes we then try to match with the mappingid to get datavaluemapper
                    datavalues_id = self.__session.query(SqlAlchemy.SeasonalNumericValues).filter(
                        and_(
                            SqlAlchemy.SeasonalNumericValues.SeasonNumericValue == row[8].value,
                            SqlAlchemy.SeasonalNumericValues.SeasonName == row[6].value
                        )
                    ).all()

                    # if block is different but there is a mapping and the value is not found in the db, we create a
                    # new datavalue mapper ID (this is mostly to handle different  case scenario
                    if datavalues and diff_scene and not datavalues_id:
                        diff_scene = False
                        raise Exception

                    result = [datavaluemapper.DataValuesMapperID for datavaluemapper in datavalues_id]

                    # check for mapping with same datavaluesmapper as the data value.
                    # if found, reuse of mapping id is emminent.
                    if len(result) > 0:
                        for mapping in datavalues:
                            if found:
                                break
                            for each in result[:]:
                                print 'it found something.'
                                if mapping.DataValuesMapperID == each:
                                    datavalues = mapping
                                    found = True
                                    break

                    # if the current value datvaluesmapperID is not found matching
                    # we use the most recent mapping id because they are from same block
                    if not found:
                        datavalues = datavalues[0]
                        datavalues_id = None

                    value = True
                except Exception as e:
                    value = True  # to ensure the first value is logged in
                    datavalues = None
                    datavalues_id = None

                # Creating New entry, datavaluemapperID and mappingID
                if not datavalues and not diff_scene:
                    datavalmapper = self.load_data_values(self.__session)
                    dataval_map = SqlAlchemy.Mapping()
                    dataval_map.AttributeID = attrib_id
                    dataval_map.InstanceID = instance_id
                    dataval_map.SourceID = source_id
                    dataval_map.MethodID = method_id
                    # Creating new datavaluemapper if its the start of another block
                    if datavalues_id is None and not diff_scene:
                        self.setup.push_data(datavalmapper)
                        datavalues_id = datavalmapper.DataValuesMapperID
                        dataval_map.DataValuesMapperID = datavalmapper.DataValuesMapperID
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

                if row[8].value is not None:
                    # Add new entry to the database if the value(depicts similar scenario) and the value is not found
                    if value and not found:
                        if row[7].value:
                            try:
                                sparams.SeasonNameCV = self.__session.query(SqlAlchemy.CV_SeasonName).filter(
                                    SqlAlchemy.CV_SeasonName.Name == row[7].value
                                ).first().Name
                            except:
                                raise Exception(
                                    "Error:\nCannot find '{}' in SeasonNameCV field of SeasonalNumericValues_table".format(
                                        row[7].value))
                        sparams.SeasonNumericValue = row[8].value
                        sparams.DataValuesMapperID = datavalues_id
                        sparams.SeasonName = row[6].value
                        self.setup.push_data(sparams)

                        # Adding order to the seasonalNumericValues according to blocks
                        # If the current row is same as the previous row, we add one to the previous order_value
                        # If it is different from the previous we create a new order_value
                        # This will be inaccurate if the excel file is not arranged in blocks.
                        # TODO: if the excel file at any point will not be arranged in block, this will have to modified
                        # TODO: and we will have to be searching the db at each point to know if the row is in or not
                        # Todo: if it is in we get the most recent value and add one else we create a new order_value
                        if order_current_row == order_row_test:
                            order_value = order_value + 1
                            sparams.SeasonOrder = order_value
                            order_row_test = order_current_row[:]
                        else:
                            order_value = 1
                            sparams.SeasonOrder = order_value
                            order_row_test = order_current_row[:]
                        value = False
                else:
                    raise Exception(
                        'Error in sheet "{}"\nField named "SeasonValue" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                            .format(sheet_name))
    def add_data(self):
        self.setup.add_data()
