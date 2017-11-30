# helper.py

# Import the classes from .py. These classes are inherited by LoadMetaData
from .. import *

# The and_ method is used to query the database with multiple conditions
from sqlalchemy import and_
from model import SqlAlchemy
import define


class LoadingUtils():
    """
        This is a helper class for each data value clases.
        it hold methods / properties used by all datavalues.
    """

    def __init__(self):
        pass

    @staticmethod
    def load_data_values(session):
        """
        This is a method to create an instance of the
        DataValuesMapper table. it queries the table to get the
        most recent datavaluemapperid. If query returns None,
        the Databaluesmapperid is set to None else 1 is added to the
        highest Datavaluesmapper.
        :return: An instance of DataValuesMapper with filled fields
        """
        dummy_dataval = SqlAlchemy.DataValuesMapper()
        try:
            dummy_dataval.DataValuesMapperID = int(session.query(SqlAlchemy.DataValuesMapper).order_by(
                SqlAlchemy.DataValuesMapper.DataValuesMapperID.desc()).first().DataValuesMapperID)
            dummy_dataval.DataValuesMapperID += 1
        except:
            dummy_dataval.DataValuesMapperID = 1
        return dummy_dataval

    @staticmethod
    def create_dummy_attrib(dum_attrib, session):
        """
        This method creates dummy record in the attribute table when loading
        datasets and objecttypes. Also contributes in creating links in the
        database
        :param session: 
        :param dum_attrib: Dummy attribute name
        :return: An instance of the Attributes() table
        """
        # crating dummy attribute record for dummy object type records
        dummy_attrib = SqlAlchemy.Attributes()
        if not isinstance(dum_attrib[0], int):
            dummy_attrib.AttributeName = dum_attrib[0]
            dummy_attrib.ObjectTypeID = session.query(SqlAlchemy.ObjectTypes).order_by(
                SqlAlchemy.ObjectTypes.ObjectTypeID.desc()).first().ObjectTypeID
        else:
            dummy_attrib.AttributeName = 'DatasetAcronym'
            dummy_attrib.ObjectTypeID = dum_attrib[0]

        dummy_attrib.UnitNameCV = session.query(SqlAlchemy.CV_Units).filter(
            SqlAlchemy.CV_Units.Name == 'Dimensionless'
        ).first().Name

        dummy_attrib.AttributeDataTypeCV = session.query(SqlAlchemy.CV_AttributeDataType).filter(
            SqlAlchemy.CV_AttributeDataType.Name == 'Dummy'
        ).first().Name

        dummy_attrib.AttributeNameCV = None

        dummy_attrib.AttributeCategoryID = None

        dummy_attrib.ModelInputOrOutput = None
        dummy_attrib.AttributeDescription = dum_attrib[1]
        return dummy_attrib

    @staticmethod
    def load_scenario_mapping(params, session):
        """
        This is a helper method to create and instance of
        the ScenarioMappings table and filling the appropriate
        fields with values sent through params.
        :param params: A list of data to fill scenarioMappings table
        :return: a filled instance of the scenarioMappings table
        """
        dummy_scen_map = SqlAlchemy.ScenarioMappings()
        dummy_scen_map.ScenarioID = params[0]
        try:
            dummy_scen_map.MappingID = session.query(SqlAlchemy.Mappings).filter(
                and_(
                    SqlAlchemy.Mappings.AttributeID == params[1],
                    SqlAlchemy.Mappings.InstanceID == params[2],
                    SqlAlchemy.Mappings.SourceID == session.query(SqlAlchemy.Sources).filter(
                        SqlAlchemy.Sources.SourceName == params[3]
                    ).first().SourceID,
                    SqlAlchemy.Mappings.MethodID == session.query(SqlAlchemy.Methods).filter(
                        SqlAlchemy.Methods.MethodName == params[4]
                    ).first().MethodID
                )

            ).first().MappingID
        except:
            raise Exception('An error occurred when loading nodes sheet')
        try:
            test = session.query(SqlAlchemy.ScenarioMappings).filter(
                and_(
                    SqlAlchemy.ScenarioMappings.MappingID == dummy_scen_map.MappingID,
                    SqlAlchemy.ScenarioMappings.ScenarioID == params[0]
                )
            ).first().ScenarioMappingID
            return None
        except:
            return dummy_scen_map

    @staticmethod
    def load_mapping(params, session):
        """
        This is a helper method to create an instance of the
        Mappings table. it creates a connection between Attributes, Instances, Scenarios, Sources and Methods, and DataValeus
        tables.
        :param session: 
        :param params: A list of data to fill Mappings tables
        :return: A filled instance of Mappings() table
        """
        # try:
        dummy_map = SqlAlchemy.Mappings()
        try:
            dummy_id = session.query(SqlAlchemy.Attributes).filter(
                SqlAlchemy.Attributes.ObjectTypeID == params[0]
            ).first().AttributeID
        except Exception as e:
            raise Exception(e.message)
        dummy_map.AttributeID = dummy_id
        dummy_map.InstanceID = params[1]
        try:
            dummy_map.SourceID = session.query(SqlAlchemy.Sources).filter(
                SqlAlchemy.Sources.SourceName == params[2]
            ).first().SourceID
        except:
            # raise exception with Sources table and value if there is no params[2] value in the Sources table.
            msg = "Sources|{}".format(params[2])
            raise Exception(msg)
        try:
            dummy_map.MethodID = session.query(SqlAlchemy.Methods).filter(
                SqlAlchemy.Methods.MethodName == params[3]
            ).first().MethodID
        except:
            # raise exception with Methods table and value if there is no params[3] value in the Methods table.
            msg = "Methods|{}".format(params[3])
            raise Exception(msg)
        dummy_map.DataValuesMapperID = params[4]

        try:
            test = session.query(SqlAlchemy.Mappings).filter(
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

    @staticmethod
    def get_ids_from_names(data_list, session):
        '''
        This method is used to get all the id's of different params from the db
        if the id's cannot be found, and exception is raised.
        :param row: This is a row of the current excel sheet.
        :param session: Takes current session of the db
        :return: return a tuple of id's
        '''
        try:
            # get attribute id based on the existence of attrib_name
            # and object_type in the attibute table. if not found exception is raised.
            attrib_id = session.query(SqlAlchemy.Attributes).filter(
                and_(
                    SqlAlchemy.Attributes.AttributeName == data_list['AttributeName'],
                    SqlAlchemy.Attributes.ObjectTypeID == session.query(SqlAlchemy.ObjectTypes).filter(
                        SqlAlchemy.ObjectTypes.ObjectType == data_list['ObjectType']
                    ).first().ObjectTypeID
                )
            ).first().AttributeID
        except Exception as e:
            raise Exception(
                "Could not find the combination of attribute and objectType '{}' / '{}' in Attributes table".
                format(data_list['AttributeName'], data_list['ObjectType']))

        try:
            instance_id = session.query(SqlAlchemy.Instances).filter(
                SqlAlchemy.Instances.InstanceName == data_list['InstanceName']
            ).first().InstanceID
        except:
            raise Exception("Could not find '{}' in the Instance table".format(data_list['InstanceName']))

        try:
            scenario_id = session.query(SqlAlchemy.Scenarios).filter(
                SqlAlchemy.Scenarios.ScenarioName == data_list['ScenarioName']
            ).first().ScenarioID
        except:
            raise Exception("Could not find '{}' in the Scenarios table".format(data_list['ScenarioName']))

        try:
            source_id = session.query(SqlAlchemy.Sources).filter(
                SqlAlchemy.Sources.SourceName == data_list['SourceName']
            ).first().SourceID
        except:
            raise Exception("Could not find '{}' in Sources table".format(data_list['SourceName']))

        try:
            method_id = session.query(SqlAlchemy.Methods).filter(
                SqlAlchemy.Methods.MethodName == data_list['MethodName']
            ).first().MethodID
        except:
            raise Exception("Could not find '{}' in the Methods table".format(data_list['MethodName']))

        return attrib_id, instance_id, scenario_id, source_id, method_id

    @staticmethod
    def get_ids(row, session, sheet_name, row_id):
        '''
        This method is used to get all the id's of different params from the db
        if the id's cannot be found, and exception is raised.
        :param row: This is a row of the current excel sheet.
        :param session: Takes current session of the db
        :return: return a tuple of id's
        '''
        try:
            # get attribute id based on the existence of attrib_name
            # and object_type in the attibute table. if not found exception is raised.
            attrib_id = session.query(SqlAlchemy.Attributes).filter(
                and_(
                    SqlAlchemy.Attributes.AttributeName == row[3].value,
                    SqlAlchemy.Attributes.ObjectTypeID == session.query(SqlAlchemy.ObjectTypes).filter(
                        and_(
                            SqlAlchemy.ObjectTypes.ObjectType == row[0].value,
                            SqlAlchemy.ObjectTypes.DatasetID == session.query(SqlAlchemy.Datasets).filter(
                                SqlAlchemy.Datasets.DatasetAcronym == define.datasetName
                                ).first().DatasetID
                        )
                    ).first().ObjectTypeID
                )
            ).first().AttributeID
        except:
            raise Exception(
                "The combination of attribute and objectType ('{}' / '{}')\n does not exist as defined in the 2.2_Attributes."
                "\n(Please reference row '{}' in '{}' sheet)".
                format(row[3].value, row[0].value, row_id, sheet_name))

        # Get InstanceID id based on InstanceName. Here, row[1].value--InstanceName
        try:
            instance_id = session.query(SqlAlchemy.Instances).filter(
                SqlAlchemy.Instances.InstanceName == row[1].value
            ).first().InstanceID
        except:
            # Get instance id based on ObjectType.
            instance_type = session.query(SqlAlchemy.ObjectTypes).filter(
                SqlAlchemy.ObjectTypes.ObjectType == row[0].value
            ).first().ObjectTypologyCV
            raise Exception(
                "In the '{}' table,\nCould not find '{}' that existing in row '{}' of '{}' sheet.".format(instance_type,
                                                                                                          row[1].value,
                                                                                                          row_id,
                                                                                                          sheet_name))

        try:
            scenario_id = session.query(SqlAlchemy.Scenarios).filter(
                SqlAlchemy.Scenarios.ScenarioName == row[2].value
            ).first().ScenarioID
        except:
            raise Exception(
                "Could not find '{}' in the Scenarios table.\n(Please reference row '{}' in '{}' sheet)".format(
                    row[2].value, row_id, sheet_name))

        try:
            source_id = session.query(SqlAlchemy.Sources).filter(
                SqlAlchemy.Sources.SourceName == row[4].value
            ).first().SourceID
        except:
            raise Exception(
                "Could not find '{}' in the Sources table.\n(Please reference row '{}' in '{}' sheet)".format(
                    row[4].value, row_id, sheet_name))

        try:
            method_id = session.query(SqlAlchemy.Methods).filter(
                SqlAlchemy.Methods.MethodName == row[5].value
            ).first().MethodID
        except:
            raise Exception(
                "Could not find '{}' in Methods table.\n(Please reference row '{}' in '{}' sheet)".format(row[5].value,
                                                                                                          row_id,
                                                                                                          sheet_name))

        return attrib_id, instance_id, scenario_id, source_id, method_id

    @staticmethod
    def data_type_test(session, row, dtype):
        '''
        this method test if the datatype for the current attribute is 
        defined in the attributes table. if not false is returned.
        :param session: current session for database
        :param row: row of current excel sheet
        :param dtype: The valid datatype to check
        :return: true or false based on the query result.
        '''
        try:
            datatype = session.query(SqlAlchemy.Attributes).filter(
                and_(
                    SqlAlchemy.Attributes.AttributeName == row[3].value,
                    SqlAlchemy.Attributes.AttributeDataTypeCV == dtype
                )
            ).first().AttributeDataTypeCV
            return True
        except Exception as e:
            print e
            return False

    @staticmethod
    def test_properties(session, row, sheet_name):
        """
        this method tests if the attribute - objectype exists.
        if this association is not found, and exception is raised.
        :param session: current session of the db
        :param row: current row in the excel sheet been read
        :param sheet_name: name of excel sheet been read
        :return: None
        """
        # test attrib - objectType existence
        try:
            attrib = session.query(SqlAlchemy.Attributes).filter(
                SqlAlchemy.Attributes.ObjectTypeID == session.query(SqlAlchemy.ObjectTypes).filter(
                    SqlAlchemy.ObjectTypes.ObjectType == row[0].value
                ).first().ObjectTypeID
            ).first().ObjectTypeID
        except:
            raise Exception('Error in Sheet {}\nObjectType {} is not associated to Attribute {}'.
                            format(sheet_name, row[0].value, row[3].value))

            # TODO: test instance - objectType existence  [[lets do it ]]

