
'''
    The load_step_3.py file is used to load networks excel files
    to the sqlite database using sqlalchemy.
    It Inherits properties from the Parse_Excel_File and DB_Setup
    classes.
    It is primarily made up of:
    - Load_Networks_Data(): This is the main and only class in this file.
                            it inherits methods for two other classes so as
                            to achieve its task. This class is made up of a
                            constructor used to initialize the other classes,
                            setup the database session which is a private variable
                            and also initialize the work_sheet variable which holds
                            all data from sheets in the excel files.
    Important methods and Variables of the class:
    - load_data():  This is a method which does all the processing of each Network.
                    it functions by iterating through the work_sheet dictionary, and
                    for each sheet parse the data appropriately so as to store in the
                    required table and fields.
    - work_sheet:   This a dictionary having network sheet as keys and the sheet
                    data as values. its data is gotten from the
                    parse_object_control_value() method found in Parse_Excel_File class.
    - __session:    Session variables (private) used to access the database.
    
      
    **Important software business rules implemented in this file:**
    
    1. An Object Type in WaMDaM can have one or many Instances. However, due to design reasons, 
    the WaMDaM Data Model, does not have a direct relationship between ObjectTypes and 
    Instances as in primary and foreign key constraints. 
    
    The Wizard business rule implemented in this file connects an Object Type with one or many of its 
    instances through the Mappings Table. The connection between the ObjectType and the MappingID happens through
    a dummy attribute called "ObjectTypeInstancesAttribute" created by the Wizard to each ObjectType in stp2_loadDataStructure.py.
    Whenever an Instance is loaded into the database (which also comes with its father ObjectType, 
    the Wizard creates a new record in the Mappings Table that connects the Instance, with the unique ID
    of the dummy attribute called ObjectTypeInstancesAttribute for the father ObjectType. 
    An Instance always must belong to a scenario and a Master Network. It also must have a source and a method name. 
    With all these provided entries in the 3.2_Nodes or 3.3_Links sheets in the WaMDaM workbook template,
    the wizard implements this businesses rule to connect an instance to its object type, and metadata.        
    
    
    2. Water Management Model or datasets may have two types of attributes: 
       local attributes that apply to one instance of an ObjectType 
       or Global Attributes that may apply to all the instances in the same scneario within a network.
       Local attributes within an Object Type in WaMDaM design can have their specifc data values that apply to an instance.
       To organize Global Attributes, WaMDaM Wizard impelments a software buiness rule to creates
       a dummy ObjectType that takes the name of the "Dataset" or "Model" an added to it "Global Attributes".
       create dummy attribuets 
       contunie 
       
       Then the rule creates a new record in the Instance table that takes the name of the MasterNetwork.
       
       
       
       
       
       "their Dataset through the ObjectTypeInstancesAttribute and " \
                                                         " 'DatasetAcronym' ObjectType. It is also used in referencing the"\ 
                                                          "the Global Attributes of each model or dataset"
    
    
    
    
    
    
    
    
    
    
    
'''

# Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
from .ConnectDB_ParseExcel import *

# This is used to create a datetime instance gotten from an excel file
import datetime

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_, or_

# Import required variables (this are the network sheet names and their start values in the excel file)
from .ReadWorkbook_SheetsNames import Network_sheets_ordered

import define

# ****************************************************************************************************************** #
#                                                                                                                    #
#                                         Script Begins here                                                         #
#                                                                                                                    #
# ****************************************************************************************************************** #


class Load_Networks_Data(Parse_Excel_File):
    """
        Class used to load Networks data to database tables.
        ::: Inherits From :::
        Parse_Excel_File: Class used to parse Excel files
        DB_Setup:   Class used to setup and create a connection
                    to the database.
    """

    def __init__(self, filename):
        """
        This is the LoadMetaData Constructor used to initialize inherited
        classes and some variables.
        :param filename: Sent to Parse_Excel_File class during instantiation
        :return:
        """
        super(Load_Networks_Data, self).__init__(filename)
        self.setup = DB_Setup()
        # self.__session = self.init()
        self.__session = self.setup.get_session()
        self.work_sheet = self.parse_object_control_value(Network_sheets_ordered[:])

    def load_scenario_mappings(self, params):
        """
        This is a helper method to create and instance of
        the ScenarioMappings table and filling the appropriate
        fields with values sent through params.
        :param params: A list of data to fill scenariomappings table
        :return: a filled instance of the scenariomappings table
        """
        dummy_scen_map = SqlAlchemy.ScenarioMappings()
        dummy_scen_map.ScenarioID = params[0]
        try:
            dummy_scen_map.MappingID = self.__session.query(SqlAlchemy.Mappings).filter(
                and_(
                    SqlAlchemy.Mappings.AttributeID == params[1],
                    SqlAlchemy.Mappings.InstanceID == params[2],
                    SqlAlchemy.Mappings.SourceID == self.__session.query(SqlAlchemy.Sources).filter(
                        SqlAlchemy.Sources.SourceName == params[3]
                    ).first().SourceID,
                    SqlAlchemy.Mappings.MethodID == self.__session.query(SqlAlchemy.Methods).filter(
                        SqlAlchemy.Methods.MethodName == params[4]
                    ).first().MethodID
                )

            ).first().MappingID
        except:
            raise Exception('An error occurred when loading nodes sheet')
        try:
            test = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                and_(
                    SqlAlchemy.ScenarioMappings.MappingID == dummy_scen_map.MappingID,
                    SqlAlchemy.ScenarioMappings.ScenarioID == params[0]
                )
            ).first().ScenarioMappingID
            return None
        except:
            return dummy_scen_map

    def load_data_values(self):
        """
        This is a helper method to create an instance of the
        DataValuesMapper table. it queries the table to get the
        most recent datavaluemapperid. If query returns None,
        the Databaluesmapperid is set to None else, one is added to the
        highest Datavaluesmapper.
        :return: An instance of DataValuesMapper with filled fields
        """
        dummy_dataval = SqlAlchemy.DataValuesMapper()
        try:
            dummy_dataval.DataValuesMapperID = int(self.__session.query(SqlAlchemy.DataValuesMapper).order_by(
                SqlAlchemy.DataValuesMapper.DataValuesMapperID.desc()).first().DataValuesMapperID)
            dummy_dataval.DataValuesMapperID += 1
        except:
            dummy_dataval.DataValuesMapperID = 1
        return dummy_dataval

    def load_mappings(self, params):
        """
        This is a helper method to create an instance of the
        Mappings table. it creates a connection between Attributes, Instances, Scenarios, Sources and Methods, and DataValeus
        tables.
        :param params: A list of data to fill Mappings tables
        :return: A filled instance of Mappings() table
        """
        # try:
        dummy_map = SqlAlchemy.Mappings()
        try:
            dummy_id = self.__session.query(SqlAlchemy.Attributes).filter(
                SqlAlchemy.Attributes.ObjectTypeID == params[0]
            ).first().AttributeID
        except Exception as e:
            raise Exception(e.message)
        dummy_map.AttributeID = dummy_id
        dummy_map.InstanceID = params[1]
        try:
            dummy_map.SourceID = self.__session.query(SqlAlchemy.Sources).filter(
                SqlAlchemy.Sources.SourceName == params[2]
            ).first().SourceID
        except:
            # raise exception with Sources table and value if there is no params[2] valuye in the Sources table.
            msg = "Sources|{}".format(params[2])
            raise Exception(msg)
        try:
            dummy_map.MethodID = self.__session.query(SqlAlchemy.Methods).filter(
                SqlAlchemy.Methods.MethodName == params[3]
            ).first().MethodID
        except:
            # raise exception with Methods table and value if there is no params[3] valuye in the Methods table.
            msg = "Methods|{}".format(params[3])
            raise Exception(msg)
        dummy_map.DataValuesMapperID = params[4]
        # except Exception as e:
        #     print e
        #     raise Exception('Object Type: ' + str(params[0])
        #                 + ',instance ID: ' + str(dummy_map.InstanceID) + ',method Name: ' + str(params[3]))

        # check for mappings
        try:
            test = self.__session.query(SqlAlchemy.Mappings).filter(
                and_(
                    SqlAlchemy.Mappings.AttributeID == dummy_map.AttributeID,
                    SqlAlchemy.Mappings.InstanceID == dummy_map.InstanceID,
                    SqlAlchemy.Mappings.SourceID == dummy_map.SourceID,
                    SqlAlchemy.Mappings.MethodID == dummy_map.MethodID
                )
            ).first().MappingID
            return None, dummy_id
        except:
            return dummy_map, dummy_id

    def load_data(self):
        """
        This method is used to parse data from each sheet to its
        appropriate table in the database.
        Due to the structure of the excel file, some hard coding
        was done to get data accurately.
        It functions by iterating over the work_sheet dictionary
        and getting each corresponding sheet_name and sheetrows,
        then using if statements to test what sheet it is , afterwards
        the appropriate table is initialized
        ed and the table fields are
        loaded using data from the corresponding sheet.
        :return: None
        """
        static_rownum = 10
        for sheet_name, sheet_rows in self.work_sheet.items():
            data_struct_acronym = dict()
            temp = sheet_rows[:]
            for row_id, row in enumerate(temp):
                temp_row = [cell.value for cell in row]

                if sheet_name == Network_sheets_ordered[0]:
                    if 'InstanceCategory_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum - 3
                            if all('' == cell.value for cell in row):
                                break
                            instance_cat = SqlAlchemy.InstanceCategories()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "InstanceCategory_table" of sheet "{}"\nField named "InstanceCategory" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id , Network_sheets_ordered[0]))
                            instance_cat.InstanceCategory = row[0].value
                            instance_cat.CategoryDefinition = row[1].value
                            self.setup.push_data(instance_cat)
                        break

                if sheet_name == Network_sheets_ordered[1]:
                    temp_row = [cell.value for cell in row]
                    if 'MasterNetworks_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum
                            if all('' == cell.value for cell in row):
                                break
                            Master_Networks = SqlAlchemy.MasterNetworks()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "MasterNetworks_table" of sheet "{}"\nField named "MasterNetworkName" is empty. This field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[1].value == "":
                                raise Exception('Error in {} row of "MasterNetworks_table" of sheet "{}"\nField named "DatasetAcronym" is empty. This field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[2].value == "":
                                raise Exception('Error in {} row of "MasterNetworks_table" of sheet "{}"\nField named "SpatialReferenceNameCV" is empty. This field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[3].value == "":
                                raise Exception('Error in {} row of "MasterNetworks_table" of sheet "{}"\nField named "ElevationDatumCV" is empty. This field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            Master_Networks.MasterNetworkName = row[0].value
                            # Foreign key constraint
                            # Raise an error if the provided CV_SpatialReference in the spreadsheet does not exist in the CV_SpatialReference t
                            try:
                                Master_Networks.SpatialReferenceNameCV = self.__session.query(SqlAlchemy.CV_SpatialReference). \
                                    filter(
                                    SqlAlchemy.CV_SpatialReference.Name == row[2].value
                                ).first().Name
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in CV_SpatialReference'
                                                .format(sheet_name, row[2].value))
                            # Foreign key constraint
                            # Raise an error if the provided VerticalDatumCV in the spreadsheet does not exist in the VerticalDatumCV table
                            try:
                                Master_Networks.VerticalDatumCV = self.__session.query(SqlAlchemy.CV_ElevationDatum).filter(
                                    SqlAlchemy.CV_ElevationDatum.Name == row[3].value
                                ).first().Name
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in VerticalDatum'
                                                .format(Network_sheets_ordered[2], row[3].value))
                            Master_Networks.Description = row[4].value

                            # storing data structure acronym from master networks to load in dummy data
                            data_struct_acronym[Master_Networks.MasterNetworkName] = row[1].value
                            self.setup.push_data(Master_Networks)

                            # adding dummy instance for each Master Network Loaded
                            dummy_instance = SqlAlchemy.Instances()
                            dummy_instance.InstanceName = row[0].value
                            dummy_instance.InstanceNameCV = None
                            dummy_instance.Longitude_x = None
                            dummy_instance.Latitude_y = None
                            dummy_instance.Description = "Dummy instance to help connect scenarios and networks with " \
                                                         "their Dataset through the ObjectTypeInstancesAttribute and " \
                                                         "'DatasetAcronym' ObjectType.\nIt is also used in referencing "\
                                                          "the Global Attributes of each model or dataset"
                            dummy_instance.InstanceCategoryID = None
                            self.setup.push_data(dummy_instance)

                    if 'Scenarios_table' in temp_row:
                        cur_table = sheet_rows[row_id + 4:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum + 10
                            if all('' == cell.value for cell in row):
                                break
                            Scenario = SqlAlchemy.Scenarios()
                            if row[0].value == "":
                                raise Exception('Error in {} row of "Scenarios_table" of sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[1].value == "":
                                raise Exception('Error in {} row of "Scenarios_table" of sheet "{}"\nField named "MasterNetworkName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[2].value == "":
                                raise Exception('Error in {} row of "Scenarios_table" of sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            if row[3].value == "":
                                raise Exception('Error in {} row of "Scenarios_table" of sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[1]))
                            Scenario.ScenarioName = row[0].value
                            if row[4].value:
                                Scenario.ScenarioStartDate = datetime.date.fromordinal(int(row[4].value) + 693594)
                            if row[5].value:
                                Scenario.ScenarioEndDate = datetime.date.fromordinal(int(row[5].value) + 693594)
                            if row[6].value:
                                    Scenario.TimeStepValue = row[6].value
                            # Foreign key constraint
                            # Raise an error if the provided Unit name in the spreadsheet does not exist in the CV_Units table
                            try:
                                if row[7].value:
                                    Scenario.TimeStepUnitCV = self.__session.query(SqlAlchemy.CV_Units).filter(
                                        SqlAlchemy.CV_Units.Name == row[7].value
                                    ).first().Name
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in Units table'
                                                .format(Network_sheets_ordered[2], row[7].value))
                            if row[8].value:
                                Scenario.Description = row[8].value
                            # Foreign key constraint
                            # Raise an error if the provided MasterNetworkName in the spreadsheet does not exist in the MasterNetworks table
                            try:
                                if row[1].value:
                                    Scenario.MasterNetworkID = self.__session.query(SqlAlchemy.MasterNetworks).filter(
                                        SqlAlchemy.MasterNetworks.MasterNetworkName == row[1].value
                                    ).first().MasterNetworkID
                            except Exception as e:
                                print e
                                raise Exception('Error in sheet {}\ncould not find {} in MasterNetworks'
                                                .format(Network_sheets_ordered[2], row[1].value))

                            self.setup.push_data(Scenario)

                            # adding  datavaluemapperid for each scenario loaded
                            dummy_dataval = self.load_data_values()
                            self.setup.push_data(dummy_dataval)

                            # adding network connection for dummy mappings
                            try:
                                dummy_id = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                    SqlAlchemy.ObjectTypes.ObjectType == data_struct_acronym[row[1].value] + ' Global Attributes'
                                ).first().ObjectTypeID
                            except Exception as e:
                                raise Exception(e.message)

                            instance_id = self.__session.query(SqlAlchemy.Instances).filter(
                                SqlAlchemy.Instances.InstanceName == row[1].value
                            ).first().InstanceID

                            try:
                                dummy_map, attrib = self.load_mappings([dummy_id, instance_id, row[2].value,
                                                                       row[3].value, dummy_dataval.DataValuesMapperID])
                            except Exception as e:
                                msg = e.message
                                if msg[:8] == "Methods|":
                                    err_method_name = msg[8:]
                                    if err_method_name != "":
                                        msg = "Error: row {} in the {} sheet.\n" \
                                              "There is no MethodName named '{}' in Methods_table of \n" \
                                              "1.2_Sources&Methods sheet.".format(row_id, sheet_name, err_method_name)
                                    else:
                                        msg = "Error: row {} in the {} sheet.\n" \
                                              "MethodName in row {} of {} sheet is empty.".format(row_id, sheet_name, row_id, sheet_name)
                                raise Exception(msg)


                            if dummy_map:
                                self.setup.push_data(dummy_map)

                            # loading scenario mappings for dummy entry

                            dummy_scen_map = self.load_scenario_mappings([Scenario.ScenarioID, attrib,
                                                                         instance_id, row[2].value, row[3].value,
                                                                         ])
                            if dummy_scen_map is not None:
                                self.setup.push_data(dummy_scen_map)
                        break

                if sheet_name == Network_sheets_ordered[2]:
                    if 'NodeInstances_table' in temp_row:
                        cur_table = sheet_rows[row_id + 5:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum
                            if all('' == cell.value for cell in row):
                                break
                            #print 'it is in node'
                            node_test = None
                            same_node = False

                            if row[0].value == "":
                                raise Exception('Error in {} row of "NodeInstances_table" of sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[2]))
                            if row[1].value == "":
                                raise Exception('Error in {} row of "NodeInstances_table" of sheet "{}"\nField named "NodeInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[2]))
                            if row[3].value == "":
                                raise Exception('Error in {} row of "NodeInstances_table" of sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[2]))
                            if row[4].value == "":
                                raise Exception('Error in {} row of "NodeInstances_table" of sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[2]))
                            if row[5].value == "":
                                raise Exception('Error in {} row of "NodeInstances_table" of sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[2]))
                            # Software business rule
                            # Check if the provided instance is a link as defined earlier in the Object Types table
                            # check if ObjectTypologyCV is Link
                            # check if ObjectTypologyCV is Link
                            try:
                                Typology_test = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                    SqlAlchemy.ObjectTypes.ObjectType == row[0].value
                                ).first().ObjectTypologyCV
                                if Typology_test == 'Link':
                                    raise Exception('Error in sheet {}\nObjectType {} has ObjectTypology Link'.
                                                    format(sheet_name, row[0].value))
                            except:
                                pass

                            # what type of error is this one (like a category)
                            # explain the comment below more
                            # this is used to share nodes so that they are not duplicated.
                            try:
                                # checking if node already exists if yes, the node is shared in the model
                                node_test = self.__session.query(SqlAlchemy.Instances).filter(
                                    SqlAlchemy.Instances.InstanceName == row[1].value
                                ).first().InstanceID
                                same_node = True
                            except:
                                nodes = SqlAlchemy.Instances()
                                if row[1].value == "":
                                    raise Exception('Error in "NodeInstances_table" of sheet "{}"\nField named "NodeInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                    .format(Network_sheets_ordered[2]))
                                nodes.InstanceName = row[1].value
                                if row[2].value:
                                    try:
                                        nodes.InstanceNameCV = self.__session.query(SqlAlchemy.CV_InstanceName).filter(
                                            SqlAlchemy.CV_InstanceName.Name == row[2].value
                                        ).first().Name
                                    except Exception as e:
                                        print e
                                        raise Exception('Error with {} sheet\n Cannot Find {} in CV_InstanceName table'.
                                                    format(sheet_name, row[2].value))

                                # //////////////// convert float error catch////////////////////
                                try:

                                    if row[7].value:
                                        nodes.Longitude_x = float(row[7].value)
                                    if row[8].value:
                                        nodes.Latitude_y = float(row[8].value)
                                except:
                                    nodes.Longitude_x = None
                                    nodes.Latitude_y = None
                                nodes.Description = row[9].value
                                if row[6].value:
                                    try:
                                        nodes.InstanceCategoryID = self.__session.query(SqlAlchemy.InstanceCategories).filter(
                                            SqlAlchemy.InstanceCategories.InstanceCategory == row[6].value
                                        ).first().InstanceCategoryID
                                    except Exception as e:
                                        print e
                                        raise Exception('Error with {} sheet\nCannot Find {} in InstanceCategories table'.
                                                        format(sheet_name, row[6].value))
                                self.setup.push_data(nodes)

                            # load DataValueMapper for new instance
                            dummy_dataval = self.load_data_values()

                            # load Mappings of node instance
                            try:
                                # ////////////// dataset name and object type name join in object type table///////////
                                DatasetID = self.__session.query(SqlAlchemy.Datasets).filter(
                                            SqlAlchemy.Datasets.DatasetAcronym == define.datasetName
                                        ).first().DatasetID


                                obj = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                and_(
                                        SqlAlchemy.ObjectTypes.ObjectType == row[0].value,
                                        SqlAlchemy.ObjectTypes.DatasetID == DatasetID
                                    )
                                ).first().ObjectTypeID
                            except Exception as e:
                                msg = "'{}' ObjectType within NodeInstances_table is not existing in ObjectTypes table.\nPlease check whether '{}' ObjectType is existing in ObjectTypes table.".format(row[0].value, row[0].value)
                                raise Exception(msg)
                            try:
                                if node_test:
                                    dummy_map, attrib = self.load_mappings([obj, node_test, row[4].value,
                                                                           row[5].value, dummy_dataval.DataValuesMapperID])
                                else:
                                    dummy_map, attrib = self.load_mappings([obj, nodes.InstanceID, row[4].value,
                                                                           row[5].value, dummy_dataval.DataValuesMapperID])
                            except Exception as e:
                                # Get exception from load_mappings method
                                msg = e.message
                                temp = msg.split('|')
                                if temp.__len__() > 1:
                                    error_msg = "Could not find {} value in {} table.\n(Please reference row {} of {} sheet.)".format(temp[1], temp[0], row_id, sheet_name)
                                else:
                                    error_msg = msg
                                raise Exception(error_msg)

                            test_same_nodes = None

                            # Foreign key constraint
                            # Raise an error if the provided MasterNetworkName in the spreadsheet does not exist in the MasterNetworks table
                            try:
                                if same_node:
                                    test_same_nodes = self.__session.query(SqlAlchemy.Mappings).filter(
                                        and_(SqlAlchemy.Mappings.AttributeID == dummy_map.AttributeID,
                                             SqlAlchemy.Mappings.InstanceID == node_test,
                                             SqlAlchemy.Mappings.SourceID == dummy_map.SourceID,
                                             SqlAlchemy.Mappings.MethodID == dummy_map.MethodID)
                                    ).first().InstanceID
                                else:
                                    raise Exception('They are not same nodes')
                            except Exception as e:
                                if dummy_dataval:
                                    self.setup.push_data(dummy_dataval)
                                if dummy_map:
                                    self.setup.push_data(dummy_map)

                            # load SenarioMappings for new instance
                            try:
                                scenario_id = self.__session.query(SqlAlchemy.Scenarios).filter(
                                    SqlAlchemy.Scenarios.ScenarioName == row[3].value
                                ).first().ScenarioID
                            except:
                                msg = "Error:row {} in the {} sheet.\nThere is no '{}' value in Scenarios_table of 3.1_Networkss_Scenarios sheet,\n (Please reference row {} in the {} sheet)".format(row_id, sheet_name, row[3].value.encode('ascii','ignore'), row_id, sheet_name)
                                raise Exception(msg)
                            if test_same_nodes or same_node:
                                dummy_scen_map = self.load_scenario_mappings([scenario_id, attrib,
                                                                             node_test, row[4].value, row[5].value
                                                                             ])
                                same_node = False
                            else:
                                dummy_scen_map = self.load_scenario_mappings([scenario_id, attrib,
                                                                             nodes.InstanceID, row[4].value, row[5].value
                                                                             ])

                            if dummy_scen_map is not None:
                                self.setup.push_data(dummy_scen_map)
                        break

                if sheet_name == Network_sheets_ordered[3]:
                    if 'LinkInstances_table' in temp_row:
                        cur_table = sheet_rows[row_id + 5:]
                        for row_id, row in enumerate(cur_table):
                            row_id = row_id + static_rownum - 1
                            if all('' == cell.value for cell in row[:-1]):
                                break
                            #print row
                            link_test = None
                            same_link = False

                            if row[0].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "ObjectType" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[1].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "LinkInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[3].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "ScenarioName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[4].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "SourceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[5].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "MethodName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[6].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "StartNodeInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))
                            if row[7].value == "":
                                raise Exception('Error in {} row of "LinkInstances_table" of sheet "{}"\nField named "EndNodeInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                .format(row_id, Network_sheets_ordered[3]))

                            # check if ObjectTypologyCV is Link
                            try:
                                Typology_test = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                    SqlAlchemy.ObjectTypes.ObjectType == row[0].value
                                ).first().ObjectTypologyCV
                                if Typology_test == 'Node':
                                    raise Exception('Error in sheet {}\nObjectType {} has ObjectTypology Node'.
                                                    format(sheet_name, row[0].value))
                            except:
                                pass

                            try:
                                # check if link already exists, if yes, link is shared
                                link_test = self.__session.query(SqlAlchemy.Instances).filter(
                                    SqlAlchemy.Instances.InstanceName == row[1].value
                                ).first().InstanceID
                                same_link = True
                            except Exception:
                                links = SqlAlchemy.Instances()
                                if row[1].value == "":
                                    raise Exception('Error in "LinkInstances_table" of sheet "{}"\nField named "LinkInstanceName" is empty.\nThis field should not be empty.\nPlease fill this field to a value'
                                                    .format(Network_sheets_ordered[3]))
                                links.InstanceName = row[1].value
                                if row[2].value:

                            # Foreign key constraint
                            # Raise an error if the provided InstanceNameCV in the spreadsheet does not exist in the CV_InstanceName table
                                    try:
                                        links.InstanceNameCV = self.__session.query(SqlAlchemy.CV_InstanceName).filter(
                                            SqlAlchemy.CV_InstanceName.Name == row[2].value
                                        ).first().Name
                                    except Exception as e:
                                        print e
                                        raise Exception('Error with {} sheet\nCannot Find {} in CV_InstanceName table'.
                                                        format(sheet_name, row[2].value))
                                coord = self.__session.query(SqlAlchemy.Instances).filter(
                                    or_(
                                        SqlAlchemy.Instances.InstanceName == row[6].value,
                                        SqlAlchemy.Instances.InstanceName == row[7].value
                                    )
                                ).all()

                                valid_coord = []
                                for value in coord:
                                    try:
                                        int(value.Longitude_x)
                                        int(value.Latitude_y)
                                        valid_coord.append(value)
                                    except:
                                        pass
                                coord = valid_coord

                                if len(coord) > 0:
                                    links.Longitude_x = sum([value.Longitude_x for value in coord]) / len(coord)
                                    links.Latitude_y = sum([value.Latitude_y for value in coord]) / len(coord)
                                links.Description = row[9].value
                                if row[8].value:

                            # Foreign key constraint
                            # Raise an error if the provided InstanceCategory in the spreadsheet does not exist in the InstanceCategory table
                                    try:
                                        links.InstanceCategoryID = self.__session.query(SqlAlchemy.InstanceCategories).filter(
                                            SqlAlchemy.InstanceCategories.InstanceCategory == row[8].value
                                        ).first().InstanceCategoryID
                                    except Exception as e:
                                        print e
                                        raise Exception('Error with {} sheet\nCannot Find {} in InstanceCategory table'.
                                                        format(sheet_name, row[8].value))
                                self.setup.push_data(links)

                            # load DataValueMapper for new instance
                            dummy_dataval = self.load_data_values()

                            # load Mappings of link instance
                            try:
                                obj = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                    SqlAlchemy.ObjectTypes.ObjectType == row[0].value
                                ).first().ObjectTypeID
                            except Exception as e:
                                raise Exception('Error with {} sheet\nCannot Find {} in ObjectTypes table'.
                                                        format(sheet_name, row[0].value))
                                # raise Exception(e.message)
                            if link_test:
                                dummy_map, attrib = self.load_mappings([obj, link_test, row[4].value,
                                                                       row[5].value, dummy_dataval.DataValuesMapperID])
                            else:
                                dummy_map, attrib = self.load_mappings([obj, links.InstanceID, row[4].value,
                                                                       row[5].value, dummy_dataval.DataValuesMapperID])

                            test_same_links = None

                            try:
                                if same_link:
                                    test_same_links = self.__session.query(SqlAlchemy.Mappings).filter(
                                        and_(SqlAlchemy.Mappings.AttributeID == dummy_map.AttributeID,
                                             SqlAlchemy.Mappings.InstanceID == link_test,
                                             SqlAlchemy.Mappings.SourceID == dummy_map.SourceID,
                                             SqlAlchemy.Mappings.MethodID == dummy_map.MethodID)
                                    ).first().InstanceID
                                else:
                                    raise Exception('They are not same nodes')
                            except Exception as e:
                                if dummy_dataval:
                                    self.setup.push_data(dummy_dataval)
                                if dummy_map:
                                    self.setup.push_data(dummy_map)

                            # load SenarioMappings for new instance
                            try:
                                scenario_id = self.__session.query(SqlAlchemy.Scenarios).filter(
                                    SqlAlchemy.Scenarios.ScenarioName == row[3].value
                                ).first().ScenarioID
                            except:
                                msg = "Error: row {} in the {} sheet.\nThere is no {}.In Scenarios_table of 3.1_Networkss@Scenarios sheet,\n" \
                                      "(Please reference row {} in the {} sheet)".format(row_id, sheet_name, row[3].value, row_id, sheet_name)
                                raise Exception(msg)
                            if test_same_links or same_link:
                                dummy_scen_map = self.load_scenario_mappings([scenario_id, attrib,
                                                                             link_test, row[4].value, row[5].value])
                                same_link = False
                            else:
                                dummy_scen_map = self.load_scenario_mappings([scenario_id, attrib,
                                                                             links.InstanceID, row[4].value, row[5].value
                                                                             ])

                            if dummy_scen_map is not None:
                                self.setup.push_data(dummy_scen_map)

                            # loading Connections (start and end nodes)
                            link_conn = SqlAlchemy.Connections()

                            '''if links is None, links.InstanceID is invalid . Therefore put 'link_test' to 'link_conn.LinkInstanceID'''
                            try:
                                link_conn.LinkInstanceID = links.InstanceID
                            except:
                                link_conn.LinkInstanceID = link_test

                            # Foreign key constraint
                            # Raise an error if the provided start InstanceName node in the spreadsheet does not exist in the Instanes table
                            try:
                                link_conn.StartNodeInstanceID = self.__session.query(SqlAlchemy.Instances).filter(
                                    SqlAlchemy.Instances.InstanceName == row[6].value
                                ).first().InstanceID
                            except:
                                raise Exception('Error in sheet {}\nstartnode value "{}" cannot be found in NodeInstances_table '
                                                'table'.format(sheet_name, row[6].value))

                            # Foreign key constraint
                            # Raise an error if the provided end InstanceName node in the spreadsheet does not exist in the Instanes table
                            try:
                                link_conn.EndNodeInstanceID = self.__session.query(SqlAlchemy.Instances).filter(
                                    SqlAlchemy.Instances.InstanceName == row[7].value
                                ).first().InstanceID
                                self.setup.push_data(link_conn)
                            except:
                                raise Exception('Error in sheet {}\nEndnode value "{}" cannot be found in NodeInstances_table '
                                                'table'.format(sheet_name, row[7].value))
                        break

    def add_data(self):
        self.setup.add_data()