
import xml.etree.ElementTree as ET
import urllib2
from sqlalchemy import and_
from datetime import datetime
from .ConnectDB_ParseExcel import *
from stp0_loadCVs import Load_CV_To_DB
from stp4_loadDataValue.helper import LoadingUtils




class CUAHS_importer():
    '''
    This class is used to get data putting to WaMDaM database
        from data responded of web.
    '''
    def __init__(self):
        self.setup = DB_Setup()
        self.__session = self.setup.get_session()

    def load_data(self, response_data):
        '''
        :param resphonse_string: responded data from web
        :return: None
        '''

    # Firstly, load CV data
        instance_cvData = Load_CV_To_DB(None)
        instance_cvData.load_data()
        instance_cvData.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data to add within Organizations table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Organizations;')
        organizationID = 0
        for n in recordCountResult:
            organizationID = int(n[0])
            organizationID += 1

        organizationName = response_data.timeSeries[0].values[0].source[0].organization
        organizationWebpage = response_data.timeSeries[0].values[0].source[0].sourceLink[0]

        # Check whether same name exist in Organizations table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Organizations).filter(
                                        SqlAlchemy.Organizations.OrganizationName == organizationName).first().OrganizationID
        except:
            pass
        if exsting is None:
            org = SqlAlchemy.Organizations()
            # org.OrganizationID = organizationID
            org.OrganizationName = organizationName
            org.OrganizationWebpage = organizationWebpage
            self.setup.push_data(org)
            self.setup.add_data()

    #////////////////////////////////////////////////////////////////////#

    # Add data within People table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM People;')
        personID = 0
        for n in recordCountResult:
            personID = int(n[0])
        personID += 1

        personName = "Unknown"

        # Check whether same name exist in People table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.People).filter(
                                        SqlAlchemy.People.PersonName == personName).first().PersonID
        except:
            pass
        if exsting is None:
            people = SqlAlchemy.People()
            people.PersonID = personID
            people.PersonName = personName
            people.OrganizationID = organizationID
            self.setup.push_data(people)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Sources table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Sources;')
        sourceID = 0
        for n in recordCountResult:
            sourceID = int(n[0])
        sourceID += 1

        source_name = "CUAHSI Water One Flow"

        # Check whether same name exist in Sources table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Sources).filter(
                                        SqlAlchemy.Sources.SourceName == source_name).first().SourceID
        except:
            pass
        if exsting is None:
            sources = SqlAlchemy.Sources()
            sources.SourceID = sourceID
            sources.SourceName = source_name
            sources.SourceWebpage = "http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL"
            sources.PersonID = personID
            self.setup.push_data(sources)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Methods table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Methods;')
        methodID = 0
        for n in recordCountResult:
            methodID = int(n[0])
            methodID += 1

        method_name = "CUAHSI/ODM"

        # Check whether same name exist in Methods table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Methods).filter(
                                        SqlAlchemy.Methods.MethodName == method_name).first().MethodID
        except:
            pass
        if exsting is None:
            methods = SqlAlchemy.Methods()
            methods.MethodID = methodID
            methods.MethodName = method_name
            methods.MethodWebpage = "https://water.usbr.gov/query.php"
            methods.MethodTypeCV = "Derivation"
            methods.PersonID = personID
            self.setup.push_data(methods)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Datasets table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Datasets;')
        datasetID = 0
        for n in recordCountResult:
            datasetID = int(n[0])
            datasetID += 1

        dataset_name = "CUAHSI web service"

        # Check whether same name exist in Datasets table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Datasets).filter(
                                        SqlAlchemy.Datasets.DatasetName == dataset_name).first().DatasetID
        except:
            pass
        if exsting is None:
            datasets = SqlAlchemy.Datasets()
            datasets.DatasetID = datasetID
            datasets.DatasetName = dataset_name
            datasets.DatasetAcronym = "CUAHSI"
            datasets.SourceID = sourceID
            self.setup.push_data(datasets)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within ObjectTypes table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM ObjectTypes;')
        objectTypeID = 0
        for n in recordCountResult:
            objectTypeID = int(n[0])
            objectTypeID += 1

        objecttype = "site"

        # Check whether same name exist in ObjectTypes table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                        SqlAlchemy.ObjectTypes.ObjectType == objecttype).first().ObjectTypeID
        except:
            pass
        if exsting is None:
            objectTypes = SqlAlchemy.ObjectTypes()
            objectTypes.ObjectTypeID = objectTypeID
            objectTypes.ObjectType = objecttype
            objectTypes.ObjectTypologyCV = "Node"
            objectTypes.DatasetID = datasetID
            self.setup.push_data(objectTypes)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Attributes table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
        attributesID = 0
        for n in recordCountResult:
            attributesID = int(n[0])
            attributesID += 1

        attribute_name = response_data.timeSeries[0].variable.variableName
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Attributes).filter(
                                        SqlAlchemy.Attributes.AttributeName == attribute_name).first().AttributeID
        except:
            pass
        if exsting is None:
            attributes = SqlAlchemy.Attributes()
            attributes.AttributeID = attributesID
            attributes.AttributeName = attribute_name

            try:
                attributes.ObjectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                            SqlAlchemy.ObjectTypes.ObjectType == 'site').first().ObjectTypeID
            except:
                raise Exception('Error \n Could not find {} in ObjectTypes'
                                .format('site'))
            attributes.UnitNameCV = response_data.timeSeries[0].variable.unit.unitName
            attributes.AttributeDataTypeCV = 'TimeSeries'
            attributes.AttributeNameCV = 'Flow'

            self.setup.push_data(attributes)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within MasterNetworks  table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM MasterNetworks;')
        masterNetworkID = 0
        for n in recordCountResult:
            masterNetworkID = int(n[0])
            masterNetworkID += 1

        masternetwork_name = "CUAHSI"

        # Check whether same name exist in MasterNetworks table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.MasterNetworks).filter(
                                        SqlAlchemy.MasterNetworks.MasterNetworkName == masternetwork_name).first().MasterNetworkID
        except:
            pass
        if exsting is None:
            masterNetworks = SqlAlchemy.MasterNetworks()
            masterNetworks.MasterNetworkID = masterNetworkID
            masterNetworks.MasterNetworkName = masternetwork_name
            self.setup.push_data(masterNetworks)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Scenarios  table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Scenarios;')
        scenarioID = 0
        for n in recordCountResult:
            scenarioID = int(n[0])
        scenarioID += 1

        scenario_name = "CUAHSI data as-is"

        # Check whether same name exist in Scenarios table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Scenarios).filter(
                                        SqlAlchemy.Scenarios.ScenarioName == scenario_name).first().ScenarioID
        except:
            pass
        if exsting is None:
            scenarios = SqlAlchemy.Scenarios()
            scenarios.ScenarioID = scenarioID
            scenarios.MasterNetworkID = masterNetworkID
            scenarios.ScenarioName = scenario_name
            self.setup.push_data(scenarios)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within Instances  table
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Instances;')
        instanceID = 0
        for n in recordCountResult:
            instanceID = int(n[0])
        instanceID += 1

        node_instance_name = response_data.timeSeries[0].sourceInfo.siteName

        # Check whether same name exist in Instances table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Instances).filter(
                                        SqlAlchemy.Instances.InstanceName == node_instance_name).first().InstanceID
        except:
            pass
        if exsting is None:
            instances = SqlAlchemy.Instances()
            instances.InstanceID = instanceID
            instances.InstanceName = node_instance_name
            instances.InstanceNameCV = 'USGS 10046500 BEAR RIVER BL STEWART DAM NR MONTPELIER, ID'

            self.setup.push_data(instances)
            self.setup.add_data()

        instance_name = node_instance_name
    #////////////////////////////////////////////////////////////////////#

    # Load data for DataValuesMapper, Mapping, ScenarioMapping, TimeSeries and TimeSeriesValues table
        # Add data for DataValuesMapper
        dataValuesMapper = SqlAlchemy.DataValuesMapper()
        try:
            dataValuesMapper.DataValuesMapperID = int(self.__session.query(SqlAlchemy.DataValuesMapper).order_by(
                SqlAlchemy.DataValuesMapper.DataValuesMapperID.desc()).first().DataValuesMapperID)
            dataValuesMapper.DataValuesMapperID += 1
        except:
            dataValuesMapper.DataValuesMapperID = 1
        self.setup.push_data(dataValuesMapper)
        self.setup.add_data()
        #///////////////////////////////////#

        # Add data for Mapping
        attrib_id, instance_id, scenario_id, source_id, method_id = LoadingUtils.get_ids_from_names({'ObjectType': objecttype,
                                                                                                     'AttributeName': attribute_name,
                                                                                                     'InstanceName': instance_name,
                                                                                                     'ScenarioName': scenario_name,
                                                                                                     'SourceName': source_name,
                                                                                                     'MethodName': method_name}, self.__session)
        dataval_map = SqlAlchemy.Mapping()
        dataval_map.AttributeID = attrib_id
        dataval_map.InstanceID = instance_id
        dataval_map.SourceID = source_id
        dataval_map.MethodID = method_id
        dataval_map.DataValuesMapperID = dataValuesMapper.DataValuesMapperID
        self.setup.push_data(dataval_map)
        self.setup.add_data()
        #///////////////////////////////////#

        # Add data for ScenarioMapping
        scenariomap = SqlAlchemy.ScenarioMapping()
        scenariomap.ScenarioID = scenario_id

        datavalues = self.__session.query(SqlAlchemy.Mapping).filter(
            and_(
                SqlAlchemy.Mapping.AttributeID == attrib_id,
                SqlAlchemy.Mapping.InstanceID == instance_id,
                SqlAlchemy.Mapping.SourceID == source_id,
                SqlAlchemy.Mapping.MethodID == method_id
            )
        ).first()
        if datavalues:
            scenariomap.MappingID = datavalues.MappingID
        else:
            scenariomap.MappingID = self.__session.query(SqlAlchemy.Mapping).filter(
                and_(
                    SqlAlchemy.Mapping.AttributeID == attrib_id,
                    SqlAlchemy.Mapping.InstanceID == instance_id,
                    SqlAlchemy.Mapping.SourceID == source_id,
                    SqlAlchemy.Mapping.MethodID == method_id
                )
            ).first().MappingID

            # if the current mappingid - scenarioid does not exist, a new
            # one is created else the old is reused.
        try:
            test = self.__session.query(SqlAlchemy.ScenarioMapping).filter(
                and_(
                    SqlAlchemy.ScenarioMapping.MappingID == scenariomap.MappingID,
                    SqlAlchemy.ScenarioMapping.ScenarioID == scenariomap.ScenarioID
                )
            ).first().ScenarioMappingID
        except:
            self.setup.push_data(scenariomap)
            self.setup.add_data()
        #///////////////////////////////////#

        # Add data within TimeSeries  table
        timeSeries = SqlAlchemy.TimeSeries()
        timeSeries.WaterOrCalendarYear = 'CalendarYear'
        timeSeries.AggregationStatisticCV = "Average"
        timeSeries.AggregationInterval = 1
        timeSeries.IntervalTimeUnitCV = "day"
        timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

        self.setup.push_data(timeSeries)
        self.setup.add_data()
        #////////////////////////////////////////////////////////////////////#

        # Add data within TimeSeriesValues table
        values = response_data.timeSeries[0].values[0].value
        for value in values:
            timeSeriesValues = SqlAlchemy.TimeSeriesValues()
            timeSeriesValues.TimeSeriesID = timeSeries.TimeSeriesID
            timeSeriesValues.DateTimeStamp = datetime(value._dateTime.year, value._dateTime.month, value._dateTime.day,
                                                      value._dateTime.hour, value._dateTime.minute, value._dateTime.second)
            try:
                timeSeriesValues.Value = value.value
            except:
                timeSeriesValues.Value = 0.0
            self.setup.push_data(timeSeriesValues)
            self.setup.add_data()
#////////////////////////////////////////////////////////////////////#

