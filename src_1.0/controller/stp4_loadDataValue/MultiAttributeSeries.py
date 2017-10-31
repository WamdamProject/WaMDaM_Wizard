# MultiAttributeSeries.py

"""In the multiAttribute Series. the main attributes on the big table in excel 
(below line 15 depicts which row is attributed to the main attribute of the small table
"""

# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required variables (this are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *

from model import SqlAlchemy


class LoadMultiCulumnArray(Parse_Excel_File, LoadingUtils):
    """
    Class used to load MultiAttributeSeries to tables.

        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadMultiAttributeSeries Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadMultiCulumnArray, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[7]])

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
        For each attribute code in the multicolumn sheet, the properties
        (Instance name, attribute name, etc ...) are loaded with the
        appropriate value. [[Value sharing is observed if a value exist with
        same properties.]] Is this still true? if yes explain more what is meant by "same properties"
        :return: None
        """
        for sheet_name, sheet_rows in self.work_sheet.items():
            print 'it is here'
            sub_attrib_array_dict = {}  # dictionary to store sub attributes in the form 'main_attrib:[sub_attribs]

            # Gets Row of Interest of main multicolumn table, start row is based on table name.
            rows_of_interest = sheet_rows[:]
            row_id = 6
            lenght = 1

            # Detecting start of data in the sheet
            # Note the table name must come directly below the subattributes table
            for row_id, row in enumerate(rows_of_interest):
                temp_row = [cell.value for cell in row]
                if 'MultiAttributeSeries_table' in temp_row:
                    rows_of_interest = sheet_rows[row_id + 4:]
                    break

            # Piece of code uses for loop to get subattribs. sub_attribs starts at row 4 column 6
            # sub_attributes ends based on the main multicolumn table
            for main_col in range(4, row_id, 1):
                if all(value=='' for value in sheet_rows[main_col]):
                    continue
                sub_attrib_array_dict[sheet_rows[main_col][5]] = sheet_rows[main_col][6:]

            if len(sub_attrib_array_dict) < 1:
                continue

            '''
                The Idea from here is to iterate over each subattribute,
                if sub_attribs are not mapped to a main attribs, that entry is
                escaped.[[explain further, give an exmaple? what does escape mean here?]]
            '''
            for main_col, sub_attrib_array in sub_attrib_array_dict.items():
                if all('' == cell for cell in sub_attrib_array) or not main_col.value:
                    continue
                # if not main_col.value:
                #     continue

                # sets initial values for testing latter in the code. [[Note sure what this mean here, explain more]]
                temp = rows_of_interest[:]
                if len(temp) < 1:
                    lenght = 0
                    break

                instance_name = temp[0][1]
                scenario_name = temp[0][2]
                object_name = temp[0][0]
                attrib_name = sheet_rows[4][6]
                source_name = temp[0][4]
                method_name = temp[0][5]

                print 'it is here'

                # temp_row is used to hold the current row to be loaded in a list so that
                # it can be tested to classify a row as similar or different
                temp_row = [cell.value for cell in temp[0]]
                temp_row.pop(2)

                stored_rows = [temp_row]  # Used to store the loaded rows.
                #print stored_rows

                # Test if sub attribute columns are same, this is to ensure that under a main attibute say VolumeCurve,
                # the sub attributes should stay unique so there should be one and only one e.g, VolumeCurve2 should not
                # repeat.
                array = [val.value for val in sub_attrib_array if val.value != '']
                if len(set(array)) < len(array):
                    # This error is show that there are sub attribute with same name under a main attribute
                    raise Exception(('Error: Same attribute columns found \n with main attribute {} in ' + sheet_name).
                                    format(main_col.value))

                '''
                    Iterate over each row for each sub attributes
                '''
                for row_id, row in enumerate(temp):
                    if row[0].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[1].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[2].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[3].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[4].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[5].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[6].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "AttributeName1_Values" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[7].value == "":
                        raise Exception('Error in {} row of "MultiAttributeSeries_table" of  sheet "{}"\nField named "AttributeName2_Values" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))

                    # make sure main attribs are similar before consuming the row.
                    if row[3].value != main_col.value:
                        continue

                    if all('' == cell.value for cell in row):
                        break

                    if any('' == cell.value for cell in row[:8]):
                        raise Exception("Some Empty Fields where found.\n All Columns in MultiAttributeSeries "
                                        "are Required in " + sheet_name)

                    # Test if data type from the provided AttributeDataType is the same as defined in the attribute Table
                    if not self.data_type_test(self.__session, row, 'MultiAttributeSeries'):
                        raise Exception("'{}' attribute is not associated to {} Datatype in " + sheet_name.
                                        format(row[3].value, 'MultiAttributeSeries'))

                    attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session, sheet_name, row_id)

                    # Test if attrib belongs to the object type
                    self.test_properties(self.__session, row, sheet_name)

                    '''
                        This portion of code tests if the current row to be loaded
                        is the same or not to a row already loaded into the db. if
                        yes then its set to similar else to different and sent to the
                        appropriate code.[[where is this code?]]
                    '''
                    diff_scene = False
                    temp_row = [cell.value for cell in row[:]]
                    temp_row.pop(2)

                    for each in stored_rows:
                        if temp_row == each:
                            if row[2].value != scenario_name.value:
                                diff_scene = True
                                break
                            break

                    stored_rows.append(temp_row)

                    # This is the code to load multicolumns rows put under the similar category.
                    if diff_scene:
                        multi_map = None
                        multiarray_mapping = SqlAlchemy.Mapping()

                        # This is to load the main attribs to multicolumn table
                        # Here, we test if the mapping combination exits, if no, the try clause will
                        # fail and the new mapping combination with main attribute will be loaded from
                        # the except clause.
                        try:
                            multi_map = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                        SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == main_col.value).first().AttributeID,
                                    SqlAlchemy.Mapping.InstanceID == instance_id,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id
                                )
                            ).all()

                            if len(multi_map) == 1:
                                #print 'lenght is greater than  [[meaning what?]]'
                                multi_map = multi_map[0]

                            elif len(multi_map) > 1:
                                multi_map = multi_map[-1]

                            main_data_val = multi_map.DataValuesMapperID

                        except Exception as e:
                            print e
                            datavalmapper = self.load_data_values(self.__session)
                            multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                SqlAlchemy.Attributes.AttributeName == main_col.value
                            ).first().AttributeID
                            multiarray_mapping.InstanceID = instance_id
                            multiarray_mapping.SourceID = source_id
                            multiarray_mapping.MethodID = method_id
                            multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                            self.setup.push_data(datavalmapper)
                            self.setup.push_data(multiarray_mapping)
                            main_data_val = datavalmapper.DataValuesMapperID

                        # Loads Scenariomapping for the new loaded combination
                        scenariomap = SqlAlchemy.ScenarioMapping()
                        scenariomap.ScenarioID = scenario_id

                        # Test if the current mapping row exist in the mapping table,
                        # if yes, the Mapping Id is gotten. else, the most recent mapping ID
                        # entry from the above except clause is gotten
                        if multi_map:
                            scenariomap.MappingID = multi_map.MappingID
                        else:
                            scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                        SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == main_col.value
                                    ).first().AttributeID,
                                    SqlAlchemy.Mapping.InstanceID == instance_id,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id,
                                    SqlAlchemy.Mapping.DataValuesMapperID == main_data_val
                                )
                            ).first().MappingID

                        try:
                            # Tries if the current mapping ID exist with the current scenario ID
                            # if yes, the scenario is shared (not loaded) else new entry is loaded.

                            test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                and_(
                                    SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                                    SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                                )
                            ).first().ScenarioMappingID
                        except:
                            self.setup.push_data(scenariomap)

                        # This is to load sub_attributes into mapping table and multicolumn arrays.
                        for sub_attrib in sub_attrib_array[:]:
                            if not sub_attrib.value:
                                continue

                            main_var_map = None
                            try:
                                # tries to get the current mapping values with the sub_attribute
                                # if it does not exist the current mapping combination is added
                                # with the sub_attribute
                                main_var_map = self.__session.query(SqlAlchemy.Mapping).filter(
                                    and_(
                                        SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                            SqlAlchemy.Attributes).filter(
                                            SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                        ).first().AttributeID,
                                        SqlAlchemy.Mapping.InstanceID == instance_id,
                                        SqlAlchemy.Mapping.SourceID == source_id,
                                        SqlAlchemy.Mapping.MethodID == method_id
                                    )
                                ).all()

                                if len(main_var_map) > 1:
                                    print 'lenght is greater than one'
                                    exit(1)

                                if len(main_var_map) == 1:
                                    main_var_map = main_var_map[0]
                                elif len(main_var_map) > 1:
                                    main_var_map = main_var_map[-1]

                                sub_data_val = main_var_map.DataValuesMapperID
                            except Exception as e:
                                datavalmapper = self.load_data_values(self.__session)
                                multiarray_mapping = SqlAlchemy.Mapping()
                                multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                    SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                ).first().AttributeID
                                multiarray_mapping.InstanceID = instance_id
                                multiarray_mapping.SourceID = source_id
                                multiarray_mapping.MethodID = method_id
                                multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                                self.setup.push_data(multiarray_mapping)
                                self.setup.push_data(datavalmapper)
                                sub_data_val = datavalmapper.DataValuesMapperID

                                # Loading MultiCulumnArrays for each new added mapping combination.
                                try:
                                    self.__session.query(SqlAlchemy.MultiAttributeSeries).filter(
                                        and_(
                                            SqlAlchemy.MultiAttributeSeries.AttributeNameID == sub_data_val,
                                            SqlAlchemy.MultiAttributeSeries.DataValuesMapperID == main_data_val
                                        )
                                    ).first().MultiAttributeSeriesID
                                except:
                                    multicolumn = SqlAlchemy.MultiAttributeSeries()
                                    multicolumn.AttributeNameID = sub_data_val
                                    multicolumn.DataValuesMapperID = main_data_val
                                    self.setup.push_data(multicolumn)

                            # adding scenario for new sub attribute mapping combination.
                            # This follows same law as loading the main_attributes. Sharing is done here
                            scenariomap = SqlAlchemy.ScenarioMapping()
                            scenariomap.ScenarioID = scenario_id
                            if main_var_map:
                                scenariomap.MappingID = main_var_map.MappingID
                            else:
                                scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                    and_(
                                        SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                            SqlAlchemy.Attributes).filter(
                                            SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                        ).first().AttributeID,
                                        SqlAlchemy.Mapping.InstanceID == instance_id,
                                        SqlAlchemy.Mapping.SourceID == source_id,
                                        SqlAlchemy.Mapping.MethodID == method_id,
                                        SqlAlchemy.Mapping.DataValuesMapperID == sub_data_val
                                    )
                                ).first().MappingID

                            try:
                                # we test if the mappingid-scenarioid association exists in scenariomapping, if yes,
                                # we reuse that association and no new entry is added to scenariomapping.
                                test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                    and_(
                                        SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                                        SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                                    )
                                ).first().ScenarioMappingID
                            except:
                                self.setup.push_data(scenariomap)

                        control = False
                        value_order = 1

                        # Loading MultiAttributeSeriesValues
                        for row_id, sub_attrib in enumerate(sub_attrib_array[:]):
                            if not sub_attrib.value:
                                continue
                            multiarray_attrib_id = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                        SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                    ).first().AttributeID,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id,
                                    SqlAlchemy.Mapping.InstanceID == instance_id
                                )
                            ).first().DataValuesMapperID

                            multiarray_id = self.__session.query(SqlAlchemy.MultiAttributeSeries).filter(
                                SqlAlchemy.MultiAttributeSeries.AttributeNameID == multiarray_attrib_id
                            ).first().MultiAttributeSeriesID

                            multicolval = SqlAlchemy.MultiAttributeSeriesValues()
                            multicolval.MultiAttributeSeriesID = multiarray_id
                            multicolval.Value = row[6 + row_id].value

                            # checks if next instance is same as previous, if yes, value order is increamented else
                            # value order is reset to 1
                            if not control:
                                try:
                                    if not (row[1].value == instance_name.value):
                                        raise Exception()
                                    multicolval.ValueOrder = \
                                        self.__session.query(SqlAlchemy.MultiAttributeSeriesValues.ValueOrder).order_by(
                                            SqlAlchemy.MultiAttributeSeriesValues.MultiAttributeSeriesValuesID.desc()
                                        ).first()[0] + 1
                                except Exception as e:
                                    multicolval.ValueOrder = 1

                                    if row[1].value != instance_name.value:
                                        instance_name = row[1]

                                value_order = multicolval.ValueOrder
                                control = True
                            else:
                                multicolval.ValueOrder = value_order

                            try:
                                # Since this values are similar, if value already exists, it is not
                                # loaded into the db else it is added.
                                test = self.__session.query(SqlAlchemy.MultiAttributeSeriesValues).filter(
                                    and_(
                                        SqlAlchemy.MultiAttributeSeriesValues.Value == multicolval.Value
                                    )
                                ).first().MultiAttributeSeriesValuesID
                            except:
                                self.setup.push_data(multicolval)

                    # this code is to load rows classified as different.
                    # if line 1773 fails ( meaning rows are different ), the script executes this portion.
                    else:
                        #print 'it is in diff_scene True'
                        found = False
                        multi_map = None
                        main_data_val = None
                        multiarray_mapping = SqlAlchemy.Mapping()

                        # This is to load the main attribs to multicolumn table
                        try:
                            multi_map = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                        SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == main_col.value).first().AttributeID,
                                    SqlAlchemy.Mapping.InstanceID == instance_id,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id
                                )
                            ).all()

                            # we check if there are any mappingid-scenarioid association, if yest, we will we use that
                            # mappingid, else, we will make new mapping entry in the db
                            for mapping in multi_map:
                                try:
                                    scene = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                        and_(
                                            SqlAlchemy.ScenarioMapping.MappingID == mapping.MappingID,
                                            SqlAlchemy.ScenarioMapping.ScenarioID == scenario_id
                                        )
                                    ).first().ScenarioMappingID
                                    found = True
                                    multi_map = mapping
                                    main_data_val = mapping.DataValuesMapperID
                                except:
                                    pass
                            datavalue = multi_map.DataValuesMapperID

                        # loads mapping combination with main_attribute
                        except Exception as e:
                            datavalmapper = self.load_data_values(self.__session)
                            multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                SqlAlchemy.Attributes.AttributeName == main_col.value
                            ).first().AttributeID
                            multiarray_mapping.InstanceID = instance_id
                            multiarray_mapping.SourceID = source_id
                            multiarray_mapping.MethodID = method_id
                            multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                            self.setup.push_data(datavalmapper)
                            self.setup.push_data(multiarray_mapping)
                            main_data_val = datavalmapper.DataValuesMapperID

                        # this is to load scenariomapping for rows under different category.
                        # gets mapping ID is mapping combination already existed else it gets the
                        # most recent mapping combination loaded.
                        scenariomap = SqlAlchemy.ScenarioMapping()
                        scenariomap.ScenarioID = scenario_id
                        if multi_map and found:
                            scenariomap.MappingID = multi_map.MappingID
                        else:
                            scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == attrib_id,
                                    SqlAlchemy.Mapping.InstanceID == instance_id,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id,
                                    SqlAlchemy.Mapping.DataValuesMapperID == main_data_val
                                )
                            ).first().MappingID

                        try:
                            # tests to see if mapping combination exists with scenarioid
                            test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                and_(
                                    SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                                    SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                                )
                            ).first().ScenarioMappingID
                        except:
                            try:
                                # Tries to get if mapping ID exists in sceario. if it does, a new mapping
                                # is created with same combinations but different datavaluemapper id to
                                # avoid sharing. The this is then loaded to scenariomapping with current
                                # scenario ID.
                                # If the mapping ID does not exist in the scenariomapping ID, then it will
                                # be loaded with the scenario ID
                                scenario_test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                    SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID
                                ).order_by(SqlAlchemy.ScenarioMapping.ScenarioMappingID).first().MappingID

                                datavalmapper = self.load_data_values(self.__session)
                                main_data_val = datavalmapper.DataValuesMapperID
                                multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                    SqlAlchemy.Attributes.AttributeName == main_col.value
                                ).first().AttributeID
                                multiarray_mapping.InstanceID = instance_id
                                multiarray_mapping.SourceID = source_id
                                multiarray_mapping.MethodID = method_id
                                multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                                self.setup.push_data(datavalmapper)
                                self.setup.push_data(multiarray_mapping)

                                scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                    and_(
                                        SqlAlchemy.Mapping.AttributeID == attrib_id,
                                        SqlAlchemy.Mapping.InstanceID == instance_id,
                                        SqlAlchemy.Mapping.SourceID == source_id,
                                        SqlAlchemy.Mapping.MethodID == method_id,
                                        SqlAlchemy.Mapping.DataValuesMapperID == datavalmapper.DataValuesMapperID
                                    )
                                ).first().MappingID
                                self.setup.push_data(scenariomap)
                            except:
                                self.setup.push_data(scenariomap)

                        # This is to load sub_attributes into mapping table and multicolumn arrays.
                        # This functions same as the main_column functions but uses sub attribs to load
                        # mappings into the mapping table. and when each mapping is loaded, a MultiAttributeSeries
                        # entry is also loaded.
                        for sub_attrib in sub_attrib_array[:]:
                            if not sub_attrib.value:
                                continue
                            found = False
                            sub_data_val = None
                            try:
                                main_var_map = self.__session.query(SqlAlchemy.Mapping).filter(
                                    and_(
                                        SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                            SqlAlchemy.Attributes).filter(
                                            SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                        ).first().AttributeID,
                                        SqlAlchemy.Mapping.InstanceID == instance_id,
                                        SqlAlchemy.Mapping.SourceID == source_id,
                                        SqlAlchemy.Mapping.MethodID == method_id
                                    )
                                ).all()
                                for mapping in main_var_map:
                                    try:
                                        scene = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                            and_(
                                                SqlAlchemy.ScenarioMapping.MappingID == mapping.MappingID,
                                                SqlAlchemy.ScenarioMapping.ScenarioID == scenario_id
                                            )
                                        ).first().ScenarioMappingID
                                        found = True
                                        main_var_map = mapping
                                        sub_data_val = mapping.DataValuesMapperID
                                    except:
                                        pass
                                test = main_var_map.DataValuesMapperID
                            except Exception as e:
                                datavalmapper = self.load_data_values(self.__session)
                                multiarray_mapping = SqlAlchemy.Mapping()
                                multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                    SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                ).first().AttributeID
                                multiarray_mapping.InstanceID = instance_id
                                multiarray_mapping.SourceID = source_id
                                multiarray_mapping.MethodID = method_id
                                multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                                self.setup.push_data(multiarray_mapping)
                                self.setup.push_data(datavalmapper)
                                sub_data_val = datavalmapper.DataValuesMapperID

                                # Loading MultiAttributeSeries
                                try:
                                    self.__session.query(SqlAlchemy.MultiAttributeSeries).filter(
                                        and_(
                                            SqlAlchemy.MultiAttributeSeries.AttributeNameID == sub_data_val,
                                            SqlAlchemy.MultiAttributeSeries.DataValuesMapperID == main_data_val
                                        )
                                    ).first().MultiAttributeSeriesID
                                except:
                                    multicolumn = SqlAlchemy.MultiAttributeSeries()
                                    multicolumn.AttributeNameID = sub_data_val
                                    multicolumn.DataValuesMapperID = main_data_val
                                    self.setup.push_data(multicolumn)

                            scenariomap = SqlAlchemy.ScenarioMapping()
                            scenariomap.ScenarioID = scenario_id
                            if main_var_map and found:
                                scenariomap.MappingID = main_var_map.MappingID
                            else:
                                scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                    and_(
                                        SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                            SqlAlchemy.Attributes).filter(
                                            SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                        ).first().AttributeID,
                                        SqlAlchemy.Mapping.InstanceID == instance_id,
                                        SqlAlchemy.Mapping.SourceID == source_id,
                                        SqlAlchemy.Mapping.MethodID == method_id,
                                        SqlAlchemy.Mapping.DataValuesMapperID == sub_data_val
                                    )
                                ).first().MappingID

                            try:
                                test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                    and_(
                                        SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                                        SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                                    )
                                ).first().ScenarioMappingID
                            except:
                                try:
                                    scenario_test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                        SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID
                                    ).order_by(SqlAlchemy.ScenarioMapping.ScenarioMappingID).first().MappingID

                                    datavalmapper = self.load_data_values(self.__session)
                                    main_data_val = datavalmapper.DataValuesMapperID
                                    multiarray_mapping.AttributeID = self.__session.query(SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == main_col.value
                                    ).first().AttributeID
                                    multiarray_mapping.InstanceID = instance_id
                                    multiarray_mapping.SourceID = source_id
                                    multiarray_mapping.MethodID = method_id
                                    multiarray_mapping.DataValuesMapperID = datavalmapper.DataValuesMapperID
                                    self.setup.push_data(datavalmapper)
                                    self.setup.push_data(multiarray_mapping)

                                    # Loading MultiAttributeSeries
                                    try:
                                        self.__session.query(SqlAlchemy.MultiAttributeSeries).filter(
                                            and_(
                                                SqlAlchemy.MultiAttributeSeries.AttributeNameID == sub_data_val,
                                                SqlAlchemy.MultiAttributeSeries.DataValuesMapperID == main_data_val
                                            )
                                        ).first().MultiAttributeSeriesID
                                    except:
                                        multicolumn = SqlAlchemy.MultiAttributeSeries()
                                        multicolumn.AttributeNameID = sub_data_val
                                        multicolumn.DataValuesMapperID = main_data_val
                                        self.setup.push_data(multicolumn)

                                    scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                                        and_(
                                            SqlAlchemy.Mapping.AttributeID == attrib_id,
                                            SqlAlchemy.Mapping.InstanceID == instance_id,
                                            SqlAlchemy.Mapping.SourceID == source_id,
                                            SqlAlchemy.Mapping.MethodID == method_id,
                                            SqlAlchemy.Mapping.DataValuesMapperID == datavalmapper.DataValuesMapperID
                                        )
                                    ).first().MappingID
                                    self.setup.push_data(scenariomap)
                                except:
                                    self.setup.push_data(scenariomap)

                        control = False
                        value_order = 1

                        # Loading MultiAttributeSeriesValues
                        for row_id, sub_attrib in enumerate(sub_attrib_array[:]):
                            if not sub_attrib.value:
                                continue
                            multiarray_attrib_id = self.__session.query(SqlAlchemy.Mapping).filter(
                                and_(
                                    SqlAlchemy.Mapping.AttributeID == self.__session.query(
                                        SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == sub_attrib.value
                                    ).first().AttributeID,
                                    SqlAlchemy.Mapping.SourceID == source_id,
                                    SqlAlchemy.Mapping.MethodID == method_id,
                                    SqlAlchemy.Mapping.InstanceID == instance_id
                                )
                            ).all()

                            for mapping in multiarray_attrib_id:
                                try:
                                    scene = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                                        and_(
                                            SqlAlchemy.ScenarioMapping.MappingID == mapping.MappingID,
                                            SqlAlchemy.ScenarioMapping.ScenarioID == scenario_id
                                        )
                                    ).first().ScenarioMappingID
                                    multiarray_attrib_id = mapping.DataValuesMapperID
                                except:
                                    pass

                            multiarray_id = self.__session.query(SqlAlchemy.MultiAttributeSeries).filter(
                                SqlAlchemy.MultiAttributeSeries.AttributeNameID == multiarray_attrib_id
                            ).first().MultiAttributeSeriesID

                            multicolval = SqlAlchemy.MultiAttributeSeriesValues()
                            multicolval.MultiAttributeSeriesID = multiarray_id
                            multicolval.Value = row[6 + row_id].value

                            # checks if next instance is same as previous, if yes, value order is increamented else
                            # value order is reset to 1
                            # No sharing  is done here. So each value is loaded with its correspongin array.

                            if not control:
                                try:
                                    if not (row[1].value == instance_name.value):
                                        raise Exception()
                                    multicolval.ValueOrder = \
                                        self.__session.query(SqlAlchemy.MultiAttributeSeriesValues.ValueOrder).order_by(
                                            SqlAlchemy.MultiAttributeSeriesValues.MultiAttributeSeriesValuesID.desc()
                                        ).first()[0] + 1
                                except Exception as e:
                                    multicolval.ValueOrder = 1
                                    instance_name = row[1]
                                value_order = multicolval.ValueOrder
                                control = True
                            else:
                                multicolval.ValueOrder = value_order

                            self.setup.push_data(multicolval)
            if lenght < 1:
                continue
    def add_data(self):
            self.setup.add_data()
