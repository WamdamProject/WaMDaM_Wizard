# LoadTimeSeries.py

# Provides helper functions for datavalues loading
from .helper import LoadingUtils

# Use to convert date entries in excel files into datetime
import datetime

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from ..ConnectDB_ParseExcel import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_

# Import required sheet names (these are the metadata sheet names and their start values in the excel file)
from ..ReadWorkbook_SheetsNames import *

from model import SqlAlchemy
import define

class LoadTimeSeries(Parse_Excel_File, LoadingUtils):
    """
    Class used to load TimeSeries data to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadTimeSeries Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(LoadTimeSeries, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[2], datavalues_sheets_ordered[4]])

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
            if sheet_name != datavalues_sheets_ordered[2]:
                continue
            temp = sheet_rows[:]

            # Detecting start of data in the sheet
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]
                if 'TimeSeries_table' in temp_row:
                    temp = sheet_rows[row_id + 4:]
                    break

            if len(temp) < 1:
                continue
            # testing is timeseriesvalues are different or similar

            # mapx is used to row (object, instance and attribute) to show if other rows with same parms are diff or sim
            mapx = dict()
            timeseries_rows = self.work_sheet[datavalues_sheets_ordered[4]][:]

            # Detecting start of data in the sheet
            for row_id, row in enumerate(timeseries_rows):
                temp_row = [cell.value for cell in row]
                if 'TimeSeriesValues_table' in temp_row:
                    timeseries_rows = sheet_rows[row_id + 4:]
                    break

            # if timeseries sheet is not empty, we get data which will be used for comparison.
            if len(timeseries_rows) > 0:
                temp_row = [cell.value for cell in timeseries_rows[0]]  # get all first row which will be a reference
                stored_rows = [temp_row]  # stored rows will be used to determine if a row is different or similar
                mapx = {str(temp_row[:3]): False}
                scenario_name = temp[0][2]

                diff_scene = True
                row_id = 1
                for row in timeseries_rows:
                    if all('' == cell.value for cell in row):
                        break

                    if any('' == cell.value for cell in row[:4]):
                        raise Exception(
                            "Some Empty Fields where found in TimeSeriesValue.\nPlease fill all Required fields")

                    if row[-1].value is None:
                        continue

                    if row[0].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[1].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[2].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[3].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[4].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[5].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[6].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "YearType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[7].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "AggregationStatisticCV" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[8].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "AggregationInterval" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))
                    if row[9].value == "":
                        raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "IntervalTimeUnit" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                        .format(row_id, sheet_name))

                    temp_row = [cell.value for cell in row[:]]
                    temp_row.pop(2)

                    # determine if a row falls under the category of similar or different
                    for each in stored_rows[:]:
                        if temp_row[:3] == each[:3]:
                            if row[2].value != scenario_name.value:
                                if temp_row == each:
                                    # if rows are similar, they are set to true
                                    mapx[str(temp_row[:3])] = True
                                    break
                                else:
                                    # store current row if not found else we store it in the map and assume they
                                    # are different
                                    if not (str(temp_row[:3]) in mapx.keys()):
                                        mapx[str(temp_row[:3])] = False

                    stored_rows.append(temp_row)

                    row_id += 1

            for row_id, row in enumerate(temp):

                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:9]):
                    raise Exception("Some Empty Fields where found in TimeSeries.\n Please fill all Required fields")

                # test if row is valid for this datatype
                if not self.data_type_test(self.__session, row, 'TimeSeries'):
                    raise Exception("'{}' attribute is not associated to {} Datatype".
                                    format(row[3].value, 'TimeSeries'))

                timeseries = SqlAlchemy.TimeSeries()
                attrib_id, instance_id, scenario_id, source_id, method_id = self.get_ids(row, self.__session, sheet_name, row_id)

                # Test if attrib belongs to object type
                self.test_properties(self.__session, row, sheet_name)

                row_copy = [cell.value for cell in row]
                row_copy.pop(2)

                # getting value of diff_scene var based on the (object, instance, scenario and attribute) of the
                # timeseries values. if diff_scene is True, then the rows are similar and reuse will be implemented
                # else if diff_scene is False, then the rows are different and reuse will not be implemented
                try:
                    diff_scene = mapx[str(row_copy[:3])]
                except:
                    diff_scene = False

                # If the mapperID exists for the attribs in the current row, we then search if the value exists for
                # the row is stored in the db, if yes we then try to match with the mappingid to get datavaluemapper
                datavalues = self.__session.query(SqlAlchemy.Mappings).filter(
                    and_(
                        SqlAlchemy.Mappings.AttributeID == attrib_id,
                        SqlAlchemy.Mappings.InstanceID == instance_id,
                        SqlAlchemy.Mappings.SourceID == source_id,
                        SqlAlchemy.Mappings.MethodID == method_id
                    )
                ).all()

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
                found = False
                try:
                    # skips searhing datavaluemapperid for required field if its attribs are not found in mapping table
                    if not datavalues or not diff_scene:
                        raise Exception

                    # try getting the datavalue_id based on the required value to try getting the required mappingID
                    datavalues_id = self.__session.query(SqlAlchemy.TimeSeries).filter(
                        and_(
                            SqlAlchemy.TimeSeries.AggregationStatisticCV == self.__session.query(
                                SqlAlchemy.CV_AggregationStatistic).filter(
                                SqlAlchemy.CV_AggregationStatistic.Name == row[7].value
                            ).first().Name,
                            SqlAlchemy.TimeSeries.AggregationInterval == row[8].value,
                            SqlAlchemy.TimeSeries.IntervalTimeUnitCV == self.__session.query(
                                SqlAlchemy.CV_Units).filter(
                                SqlAlchemy.CV_Units.Name == row[9].value
                            ).first().Name,
                        )
                    ).all()

                    result = [datavaluemapper.ValuesMapperID for datavaluemapper in datavalues_id]

                    # check for mapping with same datavaluesmapper as the data value.
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
                    # if its not found, new entry is created
                    if not found:
                        raise Exception

                    value = True
                except Exception as e:
                    datavalues = None
                    datavalues_id = None

                # if current row params are not already on the mapping table a new entry added
                # Creating New entry, datavaluemapperID and mappingID
                if not datavalues:
                    datavalmapper = self.load_data_values(self.__session)
                    dataval_map = SqlAlchemy.Mappings()
                    dataval_map.AttributeID = attrib_id
                    dataval_map.InstanceID = instance_id
                    dataval_map.SourceID = source_id
                    dataval_map.MethodID = method_id
                    # Creating new datavaluemapper if its the start of another block
                    if datavalues_id is None:
                        self.setup.push_data(datavalmapper)
                        datavalues_id = datavalmapper.ValuesMapperID
                        dataval_map.ValuesMapperID = datavalmapper.ValuesMapperID
                    else:
                        dataval_map.ValuesMapperID = datavalues_id
                    self.setup.push_data(dataval_map)

                else:
                    datavalues_id = datavalues.ValuesMapperID

                # Creating new scenariomapping if scenarioID-mappingID does not exists.
                # Starts by searchine for the mappingID in case its just been created, then tests to see if a
                # scenarioID-mappingID exists, if yes, it skips, if no, it creates an entry
                scenariomap = SqlAlchemy.ScenarioMappings()
                scenariomap.ScenarioID = scenario_id

                # try to get the mappingid for the scenario if an entry already exist
                # else we get the most recent MappingID
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

                try:
                    # test if the mappingid - scenarioid already exists in scenario table
                    # if yes, then nothing is added, else, we add new entry based of diff_scene var.
                    test = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                        and_(
                            SqlAlchemy.ScenarioMappings.MappingID == scenariomap.MappingID,
                            SqlAlchemy.ScenarioMappings.ScenarioID == scenariomap.ScenarioID
                        )
                    ).first().ScenarioMappingID
                except:
                    self.setup.push_data(scenariomap)


                if row[10].value:
                    timeseries.IsRegular = row[10].value
                if row[11].value:
                    timeseries.NoDataValue = row[11].value
                if row[12].value:
                    timeseries.Description = row[12].value

                timeseries.BeginDateTime = None
                timeseries.EndDateTime = None
                if row[6].value == "":
                    raise Exception('Error in "TimeSeries_table" of sheet "{}"\nField named "YearType" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                    .format(sheet_name))
                if row[8].value == "":
                    raise Exception('Error in "TimeSeries_table" of sheet "{}"\nField named "AggregationInterval" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                    .format(sheet_name))
                if row[5].value and row[6].value and row[7].value and row[8].value:
                    # if the value does not already exist, we add it to the db else we skip
                    if not value or not diff_scene:
                        timeseries.YearType = row[6].value
                        timeseries.AggregationStatisticCV = self.__session.query(
                            SqlAlchemy.CV_AggregationStatistic).filter(
                            SqlAlchemy.CV_AggregationStatistic.Name == row[7].value
                        ).first().Name
                        timeseries.AggregationInterval = row[8].value
                        timeseries.IntervalTimeUnitCV = self.__session.query(SqlAlchemy.CV_Units).filter(
                            SqlAlchemy.CV_Units.Name == row[9].value
                        ).first().Name
                        timeseries.ValuesMapperID = datavalues_id
                        self.setup.push_data(timeseries)
                        value = False

    def add_data(self):
        self.setup.add_data()


class LoadTimeSeriesValue(Parse_Excel_File, LoadingUtils):
    """
    Class used to load TimeSeriesValue to tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadTimeSeriesValue Constructor used to initialise inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return: None
        """
        super(LoadTimeSeriesValue, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value([datavalues_sheets_ordered[4]])

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
        then using a join query to get 'result' (timeseriesID and mappingID).
        if result is Null, then the timeseriesvalue does not exist and its
        loaded to the database, Else, a Datavaluemapperid is created for
        that timeseries.
        :return: None
        """
        for sheet_name, sheet_rows in self.work_sheet.items():
            temp = sheet_rows[:]

            # Detecting start of data in the sheet
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]
                if 'TimeSeriesValues_table' in temp_row:
                    # print '******************** it works here **********************'
                    temp = sheet_rows[row_id + 4:]
                    break

            if len(temp) < 1:
                continue

            # test to see if timeseries has data loaded in it's table, if yes, we load the series values
            try:
                self.__session.query(SqlAlchemy.TimeSeries).first().TimeSeriesID
            except:
                continue

            # get data which will be used to determine if a row is similar or different.
            temp_row = [cell.value for cell in temp[0]]  # getting first row of the timeseriesvalue sheet
            temp_row.pop(2)
            stored_rows = [temp_row]
            scenario_name = temp[0][2]

            # init_instance is used in storing dates in the time series
            init_instance = temp[0][1].value if len(temp) > 0 else False
            dates = []
            for row_id, row in enumerate(temp):
                if all('' == cell.value for cell in row):
                    break

                if any('' == cell.value for cell in row[:4]):
                    raise Exception("Some Empty Fields where found in TimeSeriesValue.\nPlease fill all Required fields")

                if row[-1].value is None:
                    continue

                if row[0].value == "":
                    raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[1].value == "":
                    raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "InstancenName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[2].value == "":
                    raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[3].value == "":
                    raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "AttributeName" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[4].value == "":
                    raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "DateTimeStamp" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                                    .format(row_id, sheet_name))
                if row[5].value == "":
                    row[5].value = "-9999"
                    # raise Exception('Error in {} row of "TimeSeriesValues_table" of  sheet "{}"\nField named "Value" is empty.\nThis field should not be empty.\nPlease fill this field to a value.'
                    #                 .format(row_id, sheet_name))

                timeserieval = SqlAlchemy.TimeSeriesValues()

                # get attibute id based on attrib - objecttype association
                try:
                    ResourceTypeID = self.__session.query(SqlAlchemy.ResourceTypes).filter(
                                            SqlAlchemy.ResourceTypes.ResourceTypeAcronym == define.datasetName
                                        ).first().ResourceTypeID

                    attrib_id = self.__session.query(SqlAlchemy.Attributes).filter(
                        and_(
                            SqlAlchemy.Attributes.AttributeName == row[3].value,
                            SqlAlchemy.Attributes.ObjectTypeID == self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                and_(
                                        SqlAlchemy.ObjectTypes.ObjectType == row[0].value,
                                        SqlAlchemy.ObjectTypes.ResourceTypeID == ResourceTypeID
                                    )
                            ).first().ObjectTypeID
                        )
                    ).first().AttributeID
                except Exception as e:
                    print e
                    raise Exception("Could not find the combination of attribute and objectType '{}' / '{}' in the Attributess table for row '{}' of TimeSeriesValues sheet".
                                    format(row[3].value, row[0].value), row_id)

                # Get InstanceID id based on InstanceName. Here, row[1].value--InstanceName
                try:
                    instance_id = self.__session.query(SqlAlchemy.Instances).filter(
                        SqlAlchemy.Instances.InstanceName == row[1].value
                    ).first().InstanceID
                except:
                    # Get instance id based on ObjectType.
                    instance_type = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                SqlAlchemy.ObjectTypes.ObjectType == row[0].value
                            ).first().ObjectTypologyCV
                    raise Exception("In the '{}' table,\nCould not find '{}' that existing in row '{}' of '{}' sheet.".format(instance_type, row[1].value, row_id, sheet_name))

                    # raise Exception('Could not find "{}" in the {} table'.format(row[1].value, instance_type))

                try:
                    scenario_id = self.__session.query(SqlAlchemy.Scenarios).filter(
                        SqlAlchemy.Scenarios.ScenarioName == row[2].value
                    ).first().ScenarioID
                except:
                    raise Exception('Could not find "{}" in the Scenarios table'.format(row[2].value))

                # check difference or similar in rows
                diff_scene = False
                temp_row = [cell.value for cell in row[:]]
                temp_row.pop(2)

                # Checking row against stored rows to determine if its different or similar
                for each in stored_rows[:]:
                    if temp_row == each:
                        if row[2].value != scenario_name.value:
                            diff_scene = True
                            break
                        break

                stored_rows.append(temp_row)

                # using inner join with mapping, timeseries and scenariomapping to get the timeseries ID
                result = self.__session.query(SqlAlchemy.TimeSeries.TimeSeriesID, SqlAlchemy.Mappings.MappingID,
                                              SqlAlchemy.ScenarioMappings.ScenarioID). \
                    join(SqlAlchemy.Mappings,
                         SqlAlchemy.Mappings.ValuesMapperID == SqlAlchemy.TimeSeries.ValuesMapperID). \
                    join(SqlAlchemy.ScenarioMappings,
                         SqlAlchemy.ScenarioMappings.MappingID == SqlAlchemy.Mappings.MappingID). \
                    filter(
                    and_(
                        SqlAlchemy.Mappings.InstanceID == instance_id,
                        SqlAlchemy.Mappings.AttributeID == attrib_id,
                        SqlAlchemy.ScenarioMappings.ScenarioID == scenario_id
                    )).all()

                if len(result) == 0:
                    raise Exception('One or more parameters in row{} of TimeseriesValues \n'
                                    'Are not found in TimeSeries Table. Please Check \n'
                                    'Loading is Exiting due to this error.'.format(row_id))
                # find mapping id which are mapped with the current scenario in the scenariomapping from result above
                # if it is found, we set the found var to True and reuse the mapping.
                for mapping in result:
                    try:
                        scene = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                            and_(
                                SqlAlchemy.ScenarioMappings.MappingID == mapping.MappingID,
                                SqlAlchemy.ScenarioMappings.ScenarioID == scenario_id
                            )
                        ).first().ScenarioMappingID
                        found = True
                        result = mapping
                        break
                    except Exception as e:
                        print e

                if isinstance(result, list):
                    raise Exception("Timeseriesvalue Maps to multiple timeseries \n"
                                    "Wizard is confused :( ")

                # test if an entry already exists in timeseriesvalues ( TimeSeriesID, Value, DateTimeStamp)
                # if not a new timeseries value entry is added to the db
                try:
                    test_query = self.__session.query(SqlAlchemy.TimeSeriesValues).filter(
                        and_(
                            SqlAlchemy.TimeSeriesValues.TimeSeriesID == result.TimeSeriesID,
                            SqlAlchemy.TimeSeriesValues.DataValue == row[5].value,
                            SqlAlchemy.TimeSeriesValues.DateTimeStamp == datetime.date.fromordinal(int(row[4].value)
                                                                                                   + 693594)
                        )
                    ).first().TimeSeriesValueID

                    # print row

                except Exception as e:
                    if result is None:
                        raise Exception('Error, No TimeSeries was found with "{}"/"{}" '
                                        'attribue and instance combination'.format(row[3].value, row[1].value))
                    # Adding new entery for time series values
                    timeserieval.TimeSeriesID = result.TimeSeriesID
                    timeserieval.DataValue = row[5].value
                    try:
                        if isinstance(row[4].value, float) or isinstance(row[4].value, int):
                            timeserieval.DateTimeStamp = datetime.date.fromordinal(int(row[4].value) + 693594)
                        else:
                            timeserieval.DateTimeStamp = datetime.date(int(row[4].value.split("/")[2]),
                                                                       int(row[4].value.split("/")[0]),
                                                                       int(row[4].value.split("/")[1]))
                    except:
                        msg = "Error: row {} in {}\n" \
                              "'{}' is not date type. (ex:1/1/1996)".format(row_id, sheet_name, row[4].value)
                        raise Exception(msg)
                    # timeserieval.DateTimeStamp = datetime.date.fromordinal(int(row[4].value) + 693594)
                    self.setup.push_data(timeserieval)

                    # adding start and end dates to timeseries.
                    # TODO: add dates to the timeseries when the timeseries values for an instance has been loaded [[is this done? or still to be??]]
                    if row[1].value == init_instance:
                        try:
                            if isinstance(row[4].value, float) or isinstance(row[4].value, int):
                                dates.append(int(row[4].value))
                            else:
                                dates.append(datetime.date(int(row[4].value.split("/")[2]), int(row[4].value.split("/")[0]), int(row[4].value.split("/")[1])))
                        except:
                            msg = "Error: row {} in {}\n" \
                                  "'{}' is not date type. (ex:1/1/1996)".format(row_id, sheet_name, row[4].value)
                            raise Exception(msg)
                    else:
                        init_instance = row[1]
                        dates = []

    def add_data(self):
        self.setup.add_data()
