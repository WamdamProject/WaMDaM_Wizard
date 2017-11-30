"""
    RWISE_importer is used to parse the wml file provided by 
    the user and load the timeseries data to the WamDam database.
"""

import xml.etree.ElementTree as ET
import urllib2
from sqlalchemy import and_
from datetime import datetime
from .ConnectDB_ParseExcel import *
from stp0_loadCVs import Load_CV_To_DB
from stp4_loadDataValue.helper import LoadingUtils


class RWISE_importer():
    """
    This class gets data from an xml file given by the user
    and stores in the Wamdam database
    """

    def __init__(self):
        self.setup = DB_Setup()
        self.__session = self.setup.get_session()

    def load_data(self, xml_string):
        """
        :param xml_string: responded data from web(xml string)
        :param input_parameters: dictionary of parameters to make web request url
        :return: None
        """

        # loading CV Data into Wamdam db
        print '**************************************'
        instance_cvData = Load_CV_To_DB(None)
        instance_cvData.load_data()
        instance_cvData.add_data()

        # parsing the xml_string gotten from the wml file provided by user
        namespace = {'wml2': '{http://www.opengis.net/waterml/2.0}', 'gml': '{http://www.opengis.net/gml/3.2}'}
        tree = ET.fromstring(xml_string)

        # loading metadata into Wamdam db

        # ** loading Organization data ** #
        org = SqlAlchemy.Organizations()
        org.OrganizationName = 'USBR RWISE'
        org.OrganizationType = ''
        org.OrganizationWebpage = 'https://water.usbr.gov/query.php'
        org.Description = ''
        self.setup.push_data(org)
        self.setup.add_data()

        # ** loading people data ** #
        pple = SqlAlchemy.People()
        personName = "Unknown"

        # Check whether same name exist in People table
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
            people.OrganizationID = org.OrganizationID
            people.Address = ''
            people.Email = ''
            people.Phone = ''
            people.Position = ''
            people.PersonWebpage = ''

            self.setup.push_data(people)
            self.setup.add_data()

        # ** loading sources data ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Sources;')
        sourceID = 0
        for n in recordCountResult:
            sourceID = int(n[0])
        sourceID += 1

        source_name = "RWIS Web-Service"

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
            sources.SourceWebpage = "https://water.usbr.gov/query.php"
            sources.PersonID = personID
            sources.Description = ''
            sources.SourceCitation = ''
            self.setup.push_data(sources)
            self.setup.add_data()

        # ** loading methods ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Methods;')
        methodID = 0
        for n in recordCountResult:
            methodID = int(n[0])
        methodID += 1

        method_name = "MethodName USBR"

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
            methods.MethodCitation = ''
            methods.Description = ''
            self.setup.push_data(methods)
            self.setup.add_data()

        # ** loading Datasets ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Datasets;')
        datasetID = 0
        for n in recordCountResult:
            datasetID = int(n[0])
        datasetID += 1

        dataset_name = "Reclamation's Water Information System (RWIS)"

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
            datasets.DatasetAcronym = "RWISE"
            datasets.SourceID = sourceID
            datasets.Description = ''
            self.setup.push_data(datasets)
            self.setup.add_data()

            # ** loading object types data ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM ObjectTypes;')
        objectTypeID = 0
        for n in recordCountResult:
            objectTypeID = int(n[0])
        objectTypeID += 1

        objecttype = "RWIS Global Attributes"

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
            objectTypes.ObjectTypologyCV = "Network"
            objectTypes.DatasetID = datasetID
            objectTypes.icon = None
            objectTypes.Description = ''
            objectTypes.ObjectCategoryID = None
            self.setup.push_data(objectTypes)

            # Creating dummy attributes for corresponding object type
            obj = LoadingUtils.create_dummy_attrib(['ObjectTypeInstances', "The purpose of this "
                                                                           "Attribute is to connect"
                                                                           " and help query all "
                                                                           "the instances that "
                                                                           "belong to one "
                                                                           "ObjectType"], self.__session)
            self.setup.push_data(obj)

        for field in tree.iter('{}site'.format(namespace['wml2'])):
            type = field.find('type')
            if type is not None:
                objecttype = type.text

                exsting = None
                objectTypeID += 1
                try:
                    exsting = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                        SqlAlchemy.ObjectTypes.ObjectType == objecttype).first().ObjectTypeID
                    print objecttype
                except Exception as e:
                    print e
                if exsting is None:
                    objectTypes = SqlAlchemy.ObjectTypes()
                    objectTypes.ObjectTypeID = objectTypeID
                    objectTypes.ObjectType = objecttype
                    objectTypes.ObjectTypeCV = 'Reservoir'
                    objectTypes.ObjectTypologyCV = "Node"
                    objectTypes.DatasetID = datasetID
                    objectTypes.icon = None
                    objectTypes.Description = ''
                    objectTypes.ObjectCategoryID = None
                    self.setup.push_data(objectTypes)

                    # Creating dummy attributes for corresponding object type
                    obj = LoadingUtils.create_dummy_attrib(['ObjectTypeInstances', "The purpose of this "
                                                                                   "Attribute is to connect"
                                                                                   " and help query all "
                                                                                   "the instances that "
                                                                                   "belong to one "
                                                                                   "ObjectType"], self.__session)
                    self.setup.push_data(obj)
                    print 'it has completed'
        self.setup.add_data()

        # ** loading master network data ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM MasterNetworks;')
        masterNetworkID = 0
        for n in recordCountResult:
            masterNetworkID = int(n[0])
        masterNetworkID += 1

        masternetwork_name = "RWIS Western States"

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
            # masterNetworks.SpatialReferenceNameCV = ''
            # masterNetworks.VerticalDatumCV = ''
            masterNetworks.Description = ''
            self.setup.push_data(masterNetworks)

            # adding dummy instance for each Master Network Loaded
            dummy_instance = SqlAlchemy.Instances()
            dummy_instance.InstanceName = masternetwork_name
            dummy_instance.InstanceNameCV = 'Hyrum Reservoir'
            dummy_instance.Longitude_x = None
            dummy_instance.Latitude_y = None
            dummy_instance.Description = "Dummy instance to help connect scenarios and networks with " \
                                         "their Dataset through the ObjectTypeInstancesAttribute and " \
                                         "'DatasetAcronym' ObjectType.\nIt is also used in referencing " \
                                         "the Global Attributes of each model or dataset"
            dummy_instance.InstanceCategoryID = None
            self.setup.push_data(dummy_instance)

            self.setup.add_data()

            # ** loading scenarios ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Scenarios;')
        scenarioID = 0
        for n in recordCountResult:
            scenarioID = int(n[0])
        scenarioID += 1

        scenario_name = "RWIS data as-is"

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
            scenarios.ScenarioStartDate = None
            scenarios.ScenarioEndDate = None
            # scenarios.TimeStepUnitCV = ''
            scenarios.TimeStepValue = None
            scenarios.Description = ''

            self.setup.push_data(scenarios)

            # adding  datavaluemapperid for each scenario loaded
            dummy_dataval = LoadingUtils.load_data_values(self.__session)
            self.setup.push_data(dummy_dataval)

            # adding network connection for dummy mapping
            try:
                dummy_id = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                    SqlAlchemy.ObjectTypes.ObjectType == 'RWIS Global Attributes'
                ).first().ObjectTypeID
            except Exception as e:
                raise Exception(e.message)

            instance_id = self.__session.query(SqlAlchemy.Instances).filter(
                SqlAlchemy.Instances.InstanceName == masternetwork_name
            ).first().InstanceID

            try:
                print 'it is starting here'
                dummy_map, attrib = LoadingUtils.load_mapping([dummy_id, instance_id, source_name,
                                                               method_name, dummy_dataval.DataValuesMapperID],
                                                              self.__session)
                print 'it is ending here'
            except Exception as e:
                print 'it is in this error'
                msg = e.message
                raise Exception(msg)

            if dummy_map:
                self.setup.push_data(dummy_map)

            # loading scenario mapping for dummy entry

            dummy_scen_map = LoadingUtils.load_scenario_mapping([scenarios.ScenarioID, attrib,
                                                                 instance_id, source_name, method_name], self.__session)
            if dummy_scen_map is not None:
                self.setup.push_data(dummy_scen_map)
            self.setup.add_data()

            # ** loading instances ** #
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Instances;')
        instanceID = 0
        for n in recordCountResult:
            instanceID = int(n[0])
        instanceID += 1

        instance_name, latitude, longitude = (None, None, None)

        for field in tree.iter('{}site'.format(namespace['wml2'])):
            des = field.find('description')
            lat = field.find('latitiude')
            long = field.find('longitude')

            if des is not None:
                instance_name = des.text
            if lat is not None:
                latitude = lat.text
            if long is not None:
                longitude = long.text

        node_instance_name = instance_name

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
            instances.Latitude_y = latitude
            instances.Longitude_x = longitude
            instances.InstanceCategoryID = None
            instances.Description = ''
            instances.InstanceNameCV = 'Hyrum Reservoir'
            self.setup.push_data(instances)

            try:
                dummy_id = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                    SqlAlchemy.ObjectTypes.ObjectType == objecttype).first().ObjectTypeID
            except Exception as e:
                raise Exception('Error \n Could not find {} in ObjectTypes'
                                .format(objecttype))

            # load DataValueMapper for new instance
            dummy_dataval = LoadingUtils.load_data_values(self.__session)
            self.setup.push_data(dummy_dataval)

            dummy_map, attrib = LoadingUtils.load_mapping([dummy_id, instanceID, source_name,
                                                           method_name, dummy_dataval.DataValuesMapperID],
                                                          self.__session)
            self.setup.push_data(dummy_map)

            scenario_id = self.__session.query(SqlAlchemy.Scenarios).filter(
                SqlAlchemy.Scenarios.ScenarioName == 'RWIS data as-is'
            ).first().ScenarioID

            # loading scenario mapping for dummy entry

            dummy_scen_map = LoadingUtils.load_scenario_mapping([scenario_id, attrib,
                                                                 instanceID, source_name, method_name], self.__session)
            if dummy_scen_map is not None:
                self.setup.push_data(dummy_scen_map)

            self.setup.add_data()

        instance_name = node_instance_name

        # ** loading attributes ** #
        # get current timeseriesid to map to the attribute when loading
        # so as to ease reuse when adding timeseries values
        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM TimeSeries;')
        timeSeriesID = 0
        for n in recordCountResult:
            timeSeriesID = int(n[0])
        timeSeriesID += 1

        recordCountResult = self.__session.execute('SELECT COUNT(*) FROM Attributes;')
        attributesID = 0
        for n in recordCountResult:
            attributesID = int(n[0])
        attributesID += 1

        attrib_name = None
        attrib_unit = None
        attrib_unittext = None
        attrib_timeseries = {}

        # iterate over parameter tag defined in the wml2 namespace to get attrib data
        # then for each attribute timeseries is added and a mapping is done
        for field in tree.iter('{}parameter'.format(namespace['wml2'])):
            name = field.find('name')
            units = field.find('units')
            unitstext = field.find('unitstext')
            if name is not None:
                attrib_name = name.text
                attrib_unit = units.text
                attrib_unittext = unitstext.text
            else:
                continue

            exsting = None
            try:
                exsting = self.__session.query(SqlAlchemy.Attributes).filter(
                    SqlAlchemy.Attributes.AttributeName == attrib_name).first().AttributeID
            except:
                pass
            if exsting is None:
                attributes = SqlAlchemy.Attributes()
                attributes.AttributeID = attributesID
                attributes.AttributeName = attrib_name
                try:
                    attributes.ObjectTypeID = self.__session.query(SqlAlchemy.ObjectTypes).filter(
                        SqlAlchemy.ObjectTypes.ObjectType == objecttype).first().ObjectTypeID
                except Exception as e:
                    print e
                    print '*********************'
                    raise Exception('Error \n Could not find {} in ObjectTypes'
                                    .format(objecttype))



                #attributes.UnitNameCV = 'foot'


                attributes.UnitName = attrib_unittext
                attributes.AttributeDataTypeCV = 'TimeSeries'
                attributes.AttributeDescription = ''
                if attrib_name=='Reservoir Storage':
                    attributes.AttributeNameCV = 'Volume'
                elif attrib_name=='Reservoir Elevation':
                    attributes.AttributeNameCV = 'Elevation'
                else:
                    attributes.AttributeNameCV = 'Flow'

                # attributes.AttributeCategoryID = ''

                attributes.ModelInputOrOutput = ''
                attributesID += 1
                self.setup.push_data(attributes)
                self.setup.add_data()

                # ** Add data for DataValuesMapper ** #
            dataValuesMapper = SqlAlchemy.DataValuesMapper()
            try:
                dataValuesMapper.DataValuesMapperID = int(self.__session.query(SqlAlchemy.DataValuesMapper).order_by(
                    SqlAlchemy.DataValuesMapper.DataValuesMapperID.desc()).first().DataValuesMapperID)
                dataValuesMapper.DataValuesMapperID += 1
            except:
                dataValuesMapper.DataValuesMapperID = 1
            self.setup.push_data(dataValuesMapper)

            # ** Add data for Mapping ** #
            attrib_id, instance_id, scenario_id, source_id, method_id = LoadingUtils.get_ids_from_names(
                {'ObjectType': objecttype,
                 'AttributeName': attrib_name,
                 'InstanceName': instance_name,
                 'ScenarioName': scenario_name,
                 'SourceName': source_name,
                 'MethodName': method_name}, self.__session)
            dataval_map = SqlAlchemy.Mappings()
            dataval_map.AttributeID = attrib_id
            dataval_map.InstanceID = instance_id
            dataval_map.SourceID = source_id
            dataval_map.MethodID = method_id
            dataval_map.DataValuesMapperID = dataValuesMapper.DataValuesMapperID
            self.setup.push_data(dataval_map)

            # ** Add data for ScenarioMapping ** #
            scenariomap = SqlAlchemy.ScenarioMappings()
            scenariomap.ScenarioID = scenario_id

            datavalues = self.__session.query(SqlAlchemy.Mappings).filter(
                and_(
                    SqlAlchemy.Mappings.AttributeID == attrib_id,
                    SqlAlchemy.Mappings.InstanceID == instance_id,
                    SqlAlchemy.Mappings.SourceID == source_id,
                    SqlAlchemy.Mappings.MethodID == method_id
                )
            ).first()
            if datavalues:
                scenariomap.MappingID = datavalues.MappingID
            else:
                scenariomap.MappingID = self.__session.query(SqlAlchemy.Mappings).filter(
                    and_(
                        SqlAlchemy.Mappings.AttributeID == attrib_id,
                        SqlAlchemy.Mappings.InstanceID == instance_id,
                        SqlAlchemy.Mappings.SourceID == source_id,
                        SqlAlchemy.Mappings.MethodID == method_id,
                        SqlAlchemy.Mappings.DataValuesMapperID == dataValuesMapper.DataValuesMapperID
                    )
                ).first().MappingID

            # if the current mappingid - scenarioid does not exist, a new
            # one is created else the old is reused.
            try:
                test = self.__session.query(SqlAlchemy.ScenarioMappings).filter(
                    and_(
                        SqlAlchemy.ScenarioMappings.MappingID == scenariomap.MappingID,
                        SqlAlchemy.ScenarioMappings.ScenarioID == scenariomap.ScenarioID
                    )
                ).first().ScenarioMappingID
            except:
                self.setup.push_data(scenariomap)

                # ** load timeseries data ** #
            timeSeries = SqlAlchemy.TimeSeries()
            timeSeries.YearType = 'CalendarYear'
            timeSeries.AggregationStatisticCV = "Average"
            timeSeries.AggregationInterval = 1.0
            timeSeries.IntervalTimeUnitCV = "day"
            timeSeries.BeginDateTime = None
            timeSeries.EndDateTime = None
            timeSeries.IsRegular = None
            timeSeries.NoDataValue = ''
            timeSeries.Description = ''
            timeSeries.DataValuesMapperID = dataValuesMapper.DataValuesMapperID

            self.setup.push_data(timeSeries)

            # to be used when loading timeseries values
            attrib_timeseries[''.join(attrib_name.split(' ')) + ':' + attrib_unit] = timeSeriesID
            timeSeriesID += 1

        self.setup.add_data()

        # ** load timeseriesvalues data ** #
        # Each attribute has points from the MeasurementTimeseries tag, for each of this tag
        # points are gotten and loaded with the correcponding timeseriesID
        for field in tree.iter('{}MeasurementTimeseries'.format(namespace['wml2'])):

            # this gets the attribute name and the units used to know what timeseriesID to use
            result = field.get('{}id'.format(namespace['gml']))
            attrib_name = result.split('.')[-2]
            attrib_unit = result.split('.')[-1]
            timeseriesID = attrib_timeseries[attrib_name + ':' + attrib_unit]

            for point in field.iter('{}MeasurementTVP'.format(namespace['wml2'])):
                timeSeriesValues = SqlAlchemy.TimeSeriesValues()
                value = point.find('{}value'.format(namespace['wml2']))
                date = point.find('{}time'.format(namespace['wml2']))

                try:
                    value = value.text
                    date = date.text.split('T')
                    date = ' '.join(date)
                    float(value)
                except:
                    continue

                if value is not None or value != '':
                    timeSeriesValues.TimeSeriesID = timeseriesID
                    timeSeriesValues.DateTimeStamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    timeSeriesValues.Value = value
                    self.setup.push_data(timeSeriesValues)
        self.setup.add_data()
