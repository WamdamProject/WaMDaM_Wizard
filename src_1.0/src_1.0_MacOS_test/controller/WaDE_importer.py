
import xml.etree.ElementTree as ET
import urllib2
from sqlalchemy import and_
from datetime import datetime
from .ConnectDB_ParseExcel import *
from stp0_loadCVs import Load_CV_To_DB
from stp4_loadDataValue.helper import LoadingUtils
import urllib2

FRONT_KEY = '{http://www.exchangenetwork.net/schema/WaDE/0.2}'



class WaDE_importer():
    '''
    This class is used to get data putting to WaMDaM database
        from WaDE data (XML) responded of web.
    '''
    def __init__(self):
        self.setup = DB_Setup()
        self.__session = self.setup.get_session()

    def load_data(self, xml_string, input_parameters):
        '''
        :param xml_string: responded data from web(xml string)
        :param input_parameters: dictionary of parameters to make web request url
        :return: None
        '''

    # Firstly, load CV data
        instance_cvData = Load_CV_To_DB(None)
        instance_cvData.load_data()
        instance_cvData.add_data()
    #////////////////////////////////////////////////////////////////////#

        data_wamdam = []
        # for xml_string in xml_string_list:
        tree = ET.fromstring(xml_string)
        tables_data ={}

    # Add data to add within Organizations table  # ex: '{http://www.exchangenetwork.net/schema/WaDE/0.2}OrganizationName'
        WADE_Organizations_Columns = ['OrganizationName', 'OrganizationIdentifier', 'WaDEURLAddress']
        organization_field_some_names = ['OrganizationName', 'Description', 'OrganizationWebpage']
        columns_data = {}
        i = 0
        for column_name in WADE_Organizations_Columns:
            column_existing = False
            for field in tree.iter(FRONT_KEY + column_name):
                columns_data.__setitem__(organization_field_some_names[i], field.text)
                column_existing = True
                break
            if not column_existing:
                columns_data.__setitem__(organization_field_some_names[i], '')
            i += 1
        organization_name = columns_data['OrganizationName']

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Organizations;')
        organizationID = 0
        for n in recordCountResult:
            organizationID = int(n[0])
        organizationID += 1

        # Check whether same name exist in Organizations table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Organizations).filter(
                                        SqlAlchemy.Organizations.OrganizationName == columns_data['OrganizationName']).first().OrganizationID
        except:
            pass
        if exsting is None:
            org = SqlAlchemy.Organizations()
            # org.OrganizationID = organizationID
            org.OrganizationName = columns_data['OrganizationName']
            org.Description = columns_data['Description']
            org.OrganizationWebpage = columns_data['OrganizationWebpage']
            self.setup.push_data(org)
            self.setup.add_data()

        tables_data.__setitem__('Organizations', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within People table
        # Get PersonName by combining FirstName and LastName.
        columns_data = {}
        column_existing = False
        first_name = ""
        for field in tree.iter(FRONT_KEY + 'FirstName'):
            first_name = field.text
            column_existing = True
            break
        if not column_existing:
            first_name = ''
            column_existing = False

        last_name = ""
        for field in tree.iter(FRONT_KEY + 'LastName'):
            last_name = field.text
            column_existing = True
            break
        if not column_existing:
            last_name = ''
            column_existing = False
        person_name = first_name + ' ' + last_name
        columns_data.__setitem__('PersonName', person_name)
        #////////////////////////////////////////////////////////////////////#

        # Get Position, Email
        WADE_People_Some_Columns = ['WaDEURLAddress', 'EmailAddressText']
        people_field_some_names = ['PersonName', 'PersonWebpage', 'Email', 'Address']
        i = 1
        for column_name in WADE_People_Some_Columns:
            for field in tree.iter(FRONT_KEY + column_name):
                columns_data.__setitem__(people_field_some_names[i], field.text)
                column_existing = True
                break
            if not column_existing:
                columns_data.__setitem__(people_field_some_names[i], '')
                column_existing = False
            i += 1
        #////////////////////////////////////////////////////////////////////#

        # Get Address
        WADE_Some_Columns_For_Address = ['MailingAddressCityName', 'MailingAddressStateUSPSCode',
                                         'MailingAddressCountryCode', 'MailingAddressZIPCode']
        address_str = ''
        for column_name in WADE_Some_Columns_For_Address:
            for field in tree.iter(FRONT_KEY + column_name):
                address_str = address_str + field.text + ','
                break
        address_str = address_str[:address_str.__len__() - 1]
        columns_data.__setitem__('Address', address_str)
        #////////////////////////////////////////////////////////////////////#
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM People;')
        personID = 0
        for n in recordCountResult:
            personID = int(n[0])
        personID += 1

        # Check whether same name exist in People table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.People).filter(
                                        SqlAlchemy.People.PersonName == columns_data['PersonName']).first().PersonID
        except:
            pass
        if exsting is None:
            people = SqlAlchemy.People()
            people.PersonID = personID
            people.PersonName = columns_data['PersonName']
            people.PersonWebpage = columns_data['PersonWebpage']
            people.Email = columns_data['Email']
            people.Address = columns_data['Address']
            people.OrganizationID = organizationID
            self.setup.push_data(people)
            self.setup.add_data()
        # tables_data.__setitem__('People', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within Sources table
        # Get SourceName
        columns_data = {}
        columns_data.__setitem__('SourceName', 'WaDE Web-Service')
        #////////////////////////////////////////////////////////////////////#

        # Get SourceWebpage
        columns_data.__setitem__('SourceWebpage', tables_data['Organizations']['OrganizationWebpage'])
        #////////////////////////////////////////////////////////////////////#

        # Get PersonName
        columns_data.__setitem__('PersonName', person_name)
        #////////////////////////////////////////////////////////////////////#

        # Get OrganizationName
        columns_data.__setitem__('OrganizationName', organization_name)
        #////////////////////////////////////////////////////////////////////#
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Sources;')
        sourceID = 0
        for n in recordCountResult:
            sourceID = int(n[0])
        sourceID += 1

        # Check whether same name exist in Sources table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Sources).filter(
                                        SqlAlchemy.Sources.SourceName == columns_data['SourceName']).first().SourceID
        except:
            pass
        if exsting is None:
            sources = SqlAlchemy.Sources()
            sources.SourceID = sourceID
            sources.SourceName = columns_data['SourceName']
            sources.SourceWebpage = columns_data['SourceWebpage']
            sources.PersonID = personID
            self.setup.push_data(sources)
            self.setup.add_data()

        source_name = columns_data['SourceName']
        # tables_data.__setitem__('Sources', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within Methods table
        url = 'http://www.westernstateswater.org/Wyoming/WADE/v0.2/GetMethod/GetMethod.php?' \
              'methodid=WYWDC&methodname=Green%20River%20Basin%20Report%20Consumptive%20Use%20Estimation'
        response = urllib2.urlopen(url)
        data_tree = ET.parse(response)
        data_root = data_tree.getroot()
        for elem in data_root:
            columns_data.__setitem__('MethodName', elem[3][1].text)
            columns_data.__setitem__('MethodWebpage', elem[3][6].text)
            break
        columns_data.__setitem__('MethodTypeCV', 'Derivation')
        columns_data.__setitem__('PersonName', person_name)
        columns_data.__setitem__('OrganizationName', organization_name)

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Methods;')
        methodID = 0
        for n in recordCountResult:
            methodID = int(n[0])
        methodID += 1

        # Check whether same name exist in Methods table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Methods).filter(
                                        SqlAlchemy.Methods.MethodName == columns_data['MethodName']).first().MethodID
        except:
            pass
        if exsting is None:
            methods = SqlAlchemy.Methods()
            methods.MethodID = methodID
            methods.MethodName = columns_data['MethodName']
            methods.MethodWebpage = columns_data['MethodWebpage']
            methods.MethodTypeCV = columns_data['MethodTypeCV']
            methods.PersonID = personID
            self.setup.push_data(methods)
            self.setup.add_data()

        method_name = columns_data['MethodName']
        # tables_data.__setitem__('Methods', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within Datasets table
        columns_data = {}
        columns_data.__setitem__('DatasetName', 'Water Data Exchange')
        columns_data.__setitem__('DatasetAcronym', 'WaDE')
        columns_data.__setitem__('SourceName', 'WaDE Web-Service')

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Datasets;')
        datasetID = 0
        for n in recordCountResult:
            datasetID = int(n[0])
        datasetID += 1

        # Check whether same name exist in Datasets table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Datasets).filter(
                                        SqlAlchemy.Datasets.DatasetName == columns_data['DatasetName']).first().DatasetID
        except:
            pass
        if exsting is None:
            datasets = SqlAlchemy.Datasets()
            datasets.DatasetID = datasetID
            datasets.DatasetName = columns_data['DatasetName']
            datasets.DatasetAcronym = columns_data['DatasetAcronym']
            datasets.SourceID = sourceID
            self.setup.push_data(datasets)
            self.setup.add_data()

        dataset_name = columns_data['DatasetName']
        # tables_data.__setitem__('Datasets', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within ObjectTypes table
        columns_data = {}
        # if input_parameters['State'] == 'Utah':
        #     columns_data.__setitem__('ObjectType', 'WaDE Global Attributes')
        # else:
        columns_data.__setitem__('ObjectType', 'Basin Water')
        columns_data.__setitem__('ObjectTypology', 'Network')
        columns_data.__setitem__('DatasetAcronym', 'WaDE')

        objecttype_list = []

        for field in tree.iter(FRONT_KEY + "WaterUseTypeName"):
            objecttype = field.text
            recordCountResult = self.__session.execute('SELECT COUNT(*) FROM ObjectTypes;')
            objectTypeID = 0
            for n in recordCountResult:
                objectTypeID = int(n[0])
            objectTypeID += 1

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
                objectTypes.ObjectTypologyCV = 'Network'
                objectTypes.DatasetID = datasetID
                self.setup.push_data(objectTypes)
                self.setup.add_data()

                objecttype_list.append(objecttype)

            objecttype = objecttype
        # tables_data.__setitem__('ObjectTypes', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within Attributes table
        attr_tag_name = 'WaterUse'
        # objectTypeID = 1
        # try:
        #     objectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
        #                                 SqlAlchemy.ObjectTypes.ObjectType == objecttype).first().ObjectTypeID
        # except:
        #     pass
        attribute_name_list = []
        columns_data = {}
        for field in tree.iter(FRONT_KEY + attr_tag_name):
            columns_data.__setitem__('AttributeUnitCV', 'acre foot')
            columns_data.__setitem__('AttributeDataTypeCV', 'TimeSeries')
            if input_parameters['State'] != "Utah":
                columns_data.__setitem__('ObjectType', field[2].text)
                columns_data.__setitem__('AttributeName', "Consumptive Use " + field[3][1].text)
                columns_data.__setitem__('AttributeCategory', field[3][1].text)

                objectTypeID = None
                try:
                    objectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                                SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']).first().ObjectTypeID
                except:
                    raise Exception('Error \n Could not find {} in ObjectTypes'
                                    .format('Basin Water'))
                attrib_id = None
                try:
                    attrib_id = self.__session.query(SqlAlchemy.Attributes).filter(
                    and_(
                        SqlAlchemy.Attributes.AttributeName == columns_data['AttributeName'],
                        SqlAlchemy.Attributes.ObjectTypeID == self.__session.query(SqlAlchemy.ObjectTypes).filter(
                            SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']
                        ).first().ObjectTypeID
                        )
                    ).first().AttributeID
                except:
                    pass
                if attrib_id is None:
                    recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
                    attributesID = 0
                    for n in recordCountResult:
                        attributesID = int(n[0])
                    attributesID += 1

                    attributes = SqlAlchemy.Attributes()
                    attributes.AttributeID = attributesID
                    attributes.AttributeName = columns_data['AttributeName']
                    attributes.ObjectTypeID = objectTypeID
                    attributes.UnitNameCV = 'acre foot'
                    attributes.AttributeDataTypeCV = 'TimeSeries'
                    self.setup.push_data(attributes)
                    self.setup.add_data()

            else:
                columns_data.__setitem__('ObjectType', field[1].text)
                columns_data.__setitem__('AttributeName', "ConsumptiveUse " + field[2][1].text)
                columns_data.__setitem__('AttributeCategory', field[2][1].text)

                objectTypeID = None
                try:
                    objectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                                SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']).first().ObjectTypeID
                except:
                    raise Exception('Error \n Could not find {} in ObjectTypes'
                                    .format('Basin Water'))
                attrib_id = None
                try:
                    attrib_id = self.__session.query(SqlAlchemy.Attributes).filter(
                    and_(
                        SqlAlchemy.Attributes.AttributeName == columns_data['AttributeName'],
                        SqlAlchemy.Attributes.ObjectTypeID == self.__session.query(SqlAlchemy.ObjectTypes).filter(
                            SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']
                        ).first().ObjectTypeID
                        )
                    ).first().AttributeID
                except:
                    pass
                if attrib_id is None:
                    recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
                    attributesID = 0
                    for n in recordCountResult:
                        attributesID = int(n[0])
                    attributesID += 1

                    attributes = SqlAlchemy.Attributes()
                    attributes.AttributeID = attributesID
                    attributes.AttributeName = columns_data['AttributeName']
                    attributes.ObjectTypeID = objectTypeID
                    attributes.UnitNameCV = 'acre foot'
                    attributes.AttributeDataTypeCV = 'TimeSeries'
                    self.setup.push_data(attributes)
                    self.setup.add_data()

                columns_data.__setitem__('ObjectType', field[1].text)
                columns_data.__setitem__('AttributeName', "Diversion SURFACE")
                columns_data.__setitem__('AttributeCategory', field[2][1].text)

                objectTypeID = None
                try:
                    objectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                                SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']).first().ObjectTypeID
                except:
                    raise Exception('Error \n Could not find {} in ObjectTypes'
                                    .format('Basin Water'))
                attrib_id = None
                try:
                    attrib_id = self.__session.query(SqlAlchemy.Attributes).filter(
                    and_(
                        SqlAlchemy.Attributes.AttributeName == columns_data['AttributeName'],
                        SqlAlchemy.Attributes.ObjectTypeID == self.__session.query(SqlAlchemy.ObjectTypes).filter(
                            SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']
                        ).first().ObjectTypeID
                        )
                    ).first().AttributeID
                except:
                    pass
                if attrib_id is None:
                    recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
                    attributesID = 0
                    for n in recordCountResult:
                        attributesID = int(n[0])
                    attributesID += 1

                    attributes = SqlAlchemy.Attributes()
                    attributes.AttributeID = attributesID
                    attributes.AttributeName = columns_data['AttributeName']
                    attributes.ObjectTypeID = objectTypeID
                    attributes.UnitNameCV = 'acre foot'
                    attributes.AttributeDataTypeCV = 'TimeSeries'
                    self.setup.push_data(attributes)
                    self.setup.add_data()

                columns_data.__setitem__('ObjectType', field[1].text)
                columns_data.__setitem__('AttributeName', "Diversion GROUND")
                columns_data.__setitem__('AttributeCategory', field[2][1].text)

                objectTypeID = None
                try:
                    objectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                                                SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']).first().ObjectTypeID
                except:
                    raise Exception('Error \n Could not find {} in ObjectTypes'
                                    .format('Basin Water'))
                attrib_id = None
                try:
                    attrib_id = self.__session.query(SqlAlchemy.Attributes).filter(
                    and_(
                        SqlAlchemy.Attributes.AttributeName == columns_data['AttributeName'],
                        SqlAlchemy.Attributes.ObjectTypeID == self.__session.query(SqlAlchemy.ObjectTypes).filter(
                            SqlAlchemy.ObjectTypes.ObjectType == columns_data['ObjectType']
                        ).first().ObjectTypeID
                        )
                    ).first().AttributeID
                except:
                    pass
                if attrib_id is None:
                    recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
                    attributesID = 0
                    for n in recordCountResult:
                        attributesID = int(n[0])
                    attributesID += 1

                    attributes = SqlAlchemy.Attributes()
                    attributes.AttributeID = attributesID
                    attributes.AttributeName = columns_data['AttributeName']
                    attributes.ObjectTypeID = objectTypeID
                    attributes.UnitNameCV = 'acre foot'
                    attributes.AttributeDataTypeCV = 'TimeSeries'
                    self.setup.push_data(attributes)
                    self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

    # Add data within MasterNetworks  table
        columns_data = {}
        columns_data.__setitem__('MasterNetworkName', 'WaDE Western States')
        columns_data.__setitem__('DatasetAcronym', 'WaDE')

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM MasterNetworks;')
        masterNetworkID = 0
        for n in recordCountResult:
            masterNetworkID = int(n[0])
        masterNetworkID += 1

        # Check whether same name exist in MasterNetworks table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.MasterNetworks).filter(
                                        SqlAlchemy.MasterNetworks.MasterNetworkName == columns_data['MasterNetworkName']).first().MasterNetworkID
        except:
            pass
        if exsting is None:
            masterNetworks = SqlAlchemy.MasterNetworks()
            masterNetworks.MasterNetworkID = masterNetworkID
            masterNetworks.MasterNetworkName = columns_data['MasterNetworkName']
            self.setup.push_data(masterNetworks)
            self.setup.add_data()

        masternetwork_name = columns_data['MasterNetworkName']
        # tables_data.__setitem__('MasterNetworks', columns_data)
    #////////////////////////////////////////////////////////////////////#

    # Add data within Scenarios  table
        columns_data = {}
        columns_data.__setitem__('ScenarioName', 'WaDE data as-is')
        columns_data.__setitem__('MasterNetworkID', masterNetworkID)
        columns_data.__setitem__('SourceName', 'WaDE Web-Service')
        columns_data.__setitem__('MethodID', methodID)

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Scenarios;')
        scenarioID = 0
        for n in recordCountResult:
            scenarioID = int(n[0])
        scenarioID += 1

        # Check whether same name exist in Scenarios table
        exsting = None
        try:
            exsting = self.__session.query(SqlAlchemy.Scenarios).filter(
                                        SqlAlchemy.Scenarios.ScenarioName == 'WaDE data as-is').first().ScenarioID
        except:
            pass
        if exsting is None:
            scenarios = SqlAlchemy.Scenarios()
            scenarios.ScenarioID = scenarioID
            scenarios.MasterNetworkID = masterNetworkID
            scenarios.ScenarioName = 'WaDE data as-is'
            self.setup.push_data(scenarios)
            self.setup.add_data()

        scenario_name = 'WaDE data as-is'
    #////////////////////////////////////////////////////////////////////#

    # Add data within Instances  table

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Instances;')
        instanceID = 0
        for n in recordCountResult:
            instanceID = int(n[0])
        instanceID += 1

        node_instance_name = ''
        for field in tree.iter(FRONT_KEY + 'ReportingUnitName'):
            node_instance_name = field.text
            break

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
            self.setup.push_data(instances)
            self.setup.add_data()

        instance_name = node_instance_name
    #////////////////////////////////////////////////////////////////////#

    # Load data for DataValuesMapper, Mapping, ScenarioMapping, TimeSeries and TimeSeriesValues table
    #     attr_tag_name = 'AvailabilitySummary'
    #     if input_parameters['State'] == "Utah":
        attr_tag_name = 'WaterUse'
        attrList = []
        timeSeries = None
        for field in tree.iter(FRONT_KEY + attr_tag_name):
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
            if input_parameters['State'] != "Utah":
                objecttype = field[2].text
                attribute_name = "Consumptive Use " + field[3][1].text
            else:
                objecttype = field[1].text
                attribute_name = "ConsumptiveUse " + field[2][1].text

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
            # reportidentifier = "2005_ConsumptiveUse"
            # for field in tree.iter(FRONT_KEY + 'ReportIdentifier'):
            #     reportidentifier = field.text
            #     break
            # url = 'https://water.utah.gov/DWRE/WADE/v0.2/GetSummary/GetSummary.php?' \
            #       'loctype=REPORTUNIT&loctxt=01-01-04&orgid=utwre&reportid={}&datatype=ALL'.format(reportidentifier)
            # response = urllib2.urlopen(url)
            # tree1 = ET.parse(response)
            # root1 = tree1.getroot()
            # for elem in root1:
            #     pass

            if input_parameters['State'] == "Utah":
                timeSeries = SqlAlchemy.TimeSeries()
                timeSeries.WaterOrCalendarYear = 'WaterYear'
                timeSeries.AggregationStatisticCV = "Cumulative"
                timeSeries.AggregationInterval = 1.0
                timeSeries.IntervalTimeUnitCV = "Year"
                timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

                self.setup.push_data(timeSeries)
                self.setup.add_data()

                timeSeries = SqlAlchemy.TimeSeries()
                timeSeries.WaterOrCalendarYear = 'WaterYear'
                timeSeries.AggregationStatisticCV = "Cumulative"
                timeSeries.AggregationInterval = 1.0
                timeSeries.IntervalTimeUnitCV = "Year"
                timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

                self.setup.push_data(timeSeries)
                self.setup.add_data()

                timeSeries = SqlAlchemy.TimeSeries()
                timeSeries.WaterOrCalendarYear = 'WaterYear'
                timeSeries.AggregationStatisticCV = "Cumulative"
                timeSeries.AggregationInterval = 1.0
                timeSeries.IntervalTimeUnitCV = "Year"
                timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

                self.setup.push_data(timeSeries)
                self.setup.add_data()
            else:
                # attributeName = "Consumptive Use " + field[3][1].text
                # attrID = None
                # try:
                #     attrID = self.__session.query(SqlAlchemy.Attributes).filter(
                #                                 SqlAlchemy.Attributes.AttributeName == attributeName).first().AttributeID
                # except:
                #     pass
                if timeSeries is None:
                    timeSeries = SqlAlchemy.TimeSeries()
                    timeSeries.WaterOrCalendarYear = 'WaterYear'
                    timeSeries.AggregationStatisticCV = "Cumulative"
                    timeSeries.AggregationInterval = 1.0
                    timeSeries.IntervalTimeUnitCV = "Year"
                    timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

                    self.setup.push_data(timeSeries)
                    self.setup.add_data()
            #////////////////////////////////////////////////////////////////////#
            # Add data within TimeSeriesValues table
            timeSeriesValues = SqlAlchemy.TimeSeriesValues()
            if timeSeries is None:
                timeSeriesValues.TimeSeriesID = 1
            else:
                timeSeriesValues.TimeSeriesID = timeSeries.TimeSeriesID
            for field0 in tree.iter(FRONT_KEY + 'ReportingYear'):
                s = field0.text
                timeSeriesValues.DateTimeStamp = datetime(int(s.split('-')[0]), 1, 1)
            try:
                for field0 in field.iter(FRONT_KEY + 'AmountNumber'):
                    timeSeriesValues.Value = field0.text
                    break
            except:
                timeSeriesValues.Value = 0.0
            if timeSeriesValues.Value is None:
                timeSeriesValues.Value = 0.0
            self.setup.push_data(timeSeriesValues)
            self.setup.add_data()
    #////////////////////////////////////////////////////////////////////#

