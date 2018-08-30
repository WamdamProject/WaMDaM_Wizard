

from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq

'''
    This class is used to get result that query to get data of instances in sqlite db.
'''

class GetInstances(object):
    def __init__(self, pathOfSqlite=''):
        self.setup = DB_Setup()
        if self.setup.get_session() == None and pathOfSqlite != '':
            self.setup.connect(pathOfSqlite, db_type='sqlite')

        self.session = self.setup.get_session()

        self.excel_pointer = None

    def getMasterNetwork(self, selectedResourceType=''):
        '''
            This method is used to get data from MasterNetworks table by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of MasterNetworkName and set of data queried
        '''
        try:
            if selectedResourceType == '':
                # get all data
                sql_command = "Select ResourceTypeAcronym,MasterNetworkName, SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description' "\
                                    "FROM ResourceTypes "\
                                    "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
                                    "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
                                    "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
                                    "left join Instances on instances.instanceid = Mappings.Instanceid "\
                                    "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
                                    "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
                                    "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
                                    "WHERE ObjectTypologyCV='Network' "
            else:
                sql_command = "Select ResourceTypeAcronym,MasterNetworkName, SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description' "\
                                        "FROM ResourceTypes "\
                                        "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
                                        "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
                                        "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
                                        "left join Instances on instances.instanceid = Mappings.Instanceid "\
                                        "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
                                        "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
                                        "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
                                        "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network' ".format(selectedResourceType)
            #Get data the remaining data except overlapping MasterNetworkName.
            result = self.session.execute(sql_command)
            nameResult = list()
            dataResult = list()
            for row in result:
                if row.MasterNetworkName == None:
                    continue
                isExisting = False
                for name in nameResult:
                    if name == row.MasterNetworkName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.MasterNetworkName)
                    dataResult.append([row.MasterNetworkName, row.ResourceTypeAcronym,
                                      row.SpatialReferenceNameCV, row.VerticalDatumCV,
                                      row.Description])


            return nameResult, dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def getScenario(self, selectedResourceType='', masterNetworkName=''):
        '''
            This method is used to get data from Scenarios table by selected ResourceTypeAcronym and MasterNetworkName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :return: list of ScenarioName and set of data queried
        '''
        try:
            if selectedResourceType == '' and masterNetworkName == '':
                sql_command = "Select ResourceTypeAcronym,ObjectType,ObjectTypologyCV,AttributeName,InstanceName,MasterNetworkName,ScenarioName, "\
                                          "ScenarioEndDate,Sourcename, TimeStepValue, TimeStepUnitCV, 'Scenarios'.'Description', Methodname ,ScenarioStartDate "\
                                            "FROM ResourceTypes "\
                                            "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
                                            "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
                                            "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
                                            "left join Instances on instances.instanceid = Mappings.Instanceid "\
                                            "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
                                            "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
                                            "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
                                            "left join Methods on Methods.Methodid = Mappings.Methodid "\
                                            "left join Sources on Sources.Sourceid = Mappings.Sourceid  "\
                                            "WHERE ObjectTypologyCV='Network'"
            else:
                sql_command = "Select ResourceTypeAcronym,ObjectType,ObjectTypologyCV,AttributeName,InstanceName,MasterNetworkName,ScenarioName, "\
                                              "ScenarioEndDate,Sourcename, TimeStepValue, TimeStepUnitCV, 'Scenarios'.'Description', Methodname ,ScenarioStartDate "\
                                                "FROM ResourceTypes "\
                                                "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
                                                "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
                                                "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
                                                "left join Instances on instances.instanceid = Mappings.Instanceid "\
                                                "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
                                                "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
                                                "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
                                                "left join Methods on Methods.Methodid = Mappings.Methodid "\
                                                "left join Sources on Sources.Sourceid = Mappings.Sourceid  "\
                                                "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network' AND MasterNetworkName='{}'"\
                                                "ORDER BY InstanceName DESC".format(selectedResourceType, masterNetworkName)
            result = self.session.execute(sql_command)
            #Get data the remaining data except overlapping ScenarioName.
            nameResult = list()
            dataResult = list()
            for row in result:
                if row.ScenarioName == None:
                    continue
                isExisting = False
                for name in nameResult:
                    if name == row.ScenarioName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.ScenarioName)
                    dataResult.append([row.ScenarioName, row.MasterNetworkName,
                                       row.SourceName, row.MethodName,
                                       row.ScenarioStartDate, row.ScenarioEndDate,
                                       row.TimeStepValue, row.TimeStepUnitCV,
                                       row.Description])

            return nameResult, dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def getNodes(self, selectedResourceType='', masterNetworkName='', scenarioName=''):
        '''
            This method is used to get data of Nodes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried and InstanceName
        '''
        try:
            if selectedResourceType == '' and masterNetworkName == '' and scenarioName == '':
                sql_command = "Select ResourceTypeAcronym,ScenarioName, InstanceName , 'ObjectTypes'.'ObjectType',Longitude_x ,Latitude_y,"\
                                            "SourceName,MethodName,Instances.Description, Instances.InstanceNameCV,InstanceCategory "\
                                            "FROM ResourceTypes "\
                                            "left join ObjectTypes on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID  "\
                                            "left join Attributes on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID "\
                                            "left join Mappings on Mappings.AttributeID = Attributes.AttributeID  "\
                                            "left join Instances on Instances.InstanceID = Mappings.InstanceID "\
                                            "left join InstanceCategories on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID "\
                                            "left join ScenarioMappings on ScenarioMappings.MappingID = Mappings.MappingID "\
                                            "left join Scenarios on Scenarios.ScenarioID=ScenarioMappings.ScenarioID "\
                                            "left join MasterNetworks on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID "\
                                            "left join Methods on Methods.MethodID  = Mappings.MethodID "\
                                            "left join Sources on Sources.SourceID  = Mappings.SourceID   "\
                                            "WHERE ObjectTypologyCV='Node' AND Attributes.AttributeName='ObjectTypeInstances' "
            else:
                sql_command = "Select ResourceTypeAcronym,ScenarioName, InstanceName , 'ObjectTypes'.'ObjectType',Longitude_x ,Latitude_y,"\
                                                "SourceName,MethodName,Instances.Description, Instances.InstanceNameCV,InstanceCategory "\
                                                "FROM ResourceTypes "\
                                                "left join ObjectTypes on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID  "\
                                                "left join Attributes on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID "\
                                                "left join Mappings on Mappings.AttributeID = Attributes.AttributeID  "\
                                                "left join Instances on Instances.InstanceID = Mappings.InstanceID "\
                                                "left join InstanceCategories on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID "\
                                                "left join ScenarioMappings on ScenarioMappings.MappingID = Mappings.MappingID "\
                                                "left join Scenarios on Scenarios.ScenarioID=ScenarioMappings.ScenarioID "\
                                                "left join MasterNetworks on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID "\
                                                "left join Methods on Methods.MethodID  = Mappings.MethodID "\
                                                "left join Sources on Sources.SourceID  = Mappings.SourceID   "\
                                                "WHERE ObjectTypologyCV='Node' AND Attributes.AttributeName='ObjectTypeInstances' " \
                                                    "AND ResourceTypeAcronym='{}' AND MasterNetworkName='{}' AND ScenarioName='{}'".format(selectedResourceType, masterNetworkName, scenarioName)
            result = self.session.execute(sql_command)

            #Get data the remaining data except overlapping InstanceName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                if row.InstanceName in nameResult:
                    isExisting = True
                if not isExisting:
                    nameResult.append(row.InstanceName)
                    dataResult.append([row.ObjectType, row.InstanceName,
                                        row.InstanceNameCV, row.ScenarioName,
                                        row.SourceName, row.MethodName,
                                        row.InstanceCategory, row.Longitude_x,
                                        row.Latitude_y, row.Description])

            return nameResult, dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def getLinkes(self, selectedResourceType='', masterNetworkName='', scenarioName=''):
        """
            This method is used to get data of Linkes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried
        """
        try:
            if selectedResourceType == '' and masterNetworkName == '' and scenarioName == '':
                sql_command = "Select ResourceTypeAcronym,ScenarioName,'Instances'.'InstanceName' As LinkInstanceName, 'Instances'.'InstanceNameCV', 'ObjectTypes'.'ObjectType' " \
                              "AS LinkObjectType,'ObjectTypes'.'ObjectTypeCV', 'StartNodeInstance'.'InstanceName' As StartNodeInstanceName,'StartNodeInstance'.'Longitude_x'" \
                              " As StartInstanceLong,'StartNodeInstance'.'Latitude_y' As StartLatitude_y,'ObjectTypeStartNodeInstance'.'ObjectType' " \
                              "AS StartNodeObjectType,'EndNodeInstance'.'InstanceName' As EndNodeInstanceName,'EndNodeInstance'.'Longitude_x' " \
                              "As EndStartInstanceLong,'EndNodeInstance'.'Latitude_y' As EndLatitude_y,'ObjectTypeEndNodeInstance'.'ObjectType' " \
                              "AS EndNodeObjectType,SourceName,MethodName,'Instances'.'Description',InstanceCategory " \
                              "FROM ResourceTypes " \
                              "left join ObjectTypes on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID " \
                              "left join Attributes on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID " \
                              "left join Mappings on Mappings.AttributeID = Attributes.AttributeID  " \
                              "left join Instances on Instances.InstanceID = Mappings.InstanceID  " \
                              "left join InstanceCategories  on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID  " \
                              "left join Connections on Connections.LinkInstanceID = Instances.InstanceID  " \
                              "left join Instances AS StartNodeInstance  on StartNodeInstance.InstanceID = Connections.StartNodeInstanceID  " \
                              "left join Mappings AS MappingStartNodeInstance  on MappingStartNodeInstance.InstanceID = StartNodeInstance.InstanceID " \
                              "left join Attributes AS AttributesStartNodeInstance  on AttributesStartNodeInstance.AttributeID = MappingStartNodeInstance.AttributeID " \
                              "left join ObjectTypes AS ObjectTypeStartNodeInstance on ObjectTypeStartNodeInstance.ObjectTypeID = AttributesStartNodeInstance.ObjectTypeID  " \
                              "left join Instances AS EndNodeInstance  on EndNodeInstance.InstanceID = Connections.EndNodeInstanceID  " \
                              "left join Mappings AS MappingEndNodeInstance on MappingEndNodeInstance.InstanceID = EndNodeInstance.InstanceID  " \
                              "left join Attributes AS AttributesEndNodeInstance  on AttributesEndNodeInstance.AttributeID = MappingEndNodeInstance.AttributeID  " \
                              "left join ObjectTypes AS ObjectTypeEndNodeInstance  on ObjectTypeEndNodeInstance.ObjectTypeID = AttributesEndNodeInstance.ObjectTypeID  " \
                              "left join ScenarioMappings  on ScenarioMappings.MappingID = Mappings.MappingID  " \
                              "left join Scenarios on Scenarios.ScenarioID=ScenarioMappings.ScenarioID  " \
                              "left join MasterNetworks on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID  " \
                              "left join Methods on Methods.MethodID  = Mappings.MethodID  " \
                              "left join Sources on Sources.SourceID  = Mappings.SourceID   " \
                              "WHERE 'ObjectTypes'.'ObjectTypologyCV'='Link'  AND Attributes.AttributeName='ObjectTypeInstances' " \
                              "AND AttributesStartNodeInstance.AttributeName='ObjectTypeInstances'  AND AttributesEndNodeInstance.AttributeName='ObjectTypeInstances' "
            else:
                sql_command = "Select ResourceTypeAcronym,ScenarioName,'Instances'.'InstanceName' As LinkInstanceName, 'Instances'.'InstanceNameCV', 'ObjectTypes'.'ObjectType' " \
                          "AS LinkObjectType,'ObjectTypes'.'ObjectTypeCV', 'StartNodeInstance'.'InstanceName' As StartNodeInstanceName,'StartNodeInstance'.'Longitude_x'" \
                          " As StartInstanceLong,'StartNodeInstance'.'Latitude_y' As StartLatitude_y,'ObjectTypeStartNodeInstance'.'ObjectType' " \
                          "AS StartNodeObjectType,'EndNodeInstance'.'InstanceName' As EndNodeInstanceName,'EndNodeInstance'.'Longitude_x' " \
                          "As EndStartInstanceLong,'EndNodeInstance'.'Latitude_y' As EndLatitude_y,'ObjectTypeEndNodeInstance'.'ObjectType' " \
                          "AS EndNodeObjectType,SourceName,MethodName,'Instances'.'Description',InstanceCategory " \
                          "FROM ResourceTypes " \
                          "left join ObjectTypes on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID " \
                          "left join Attributes on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID " \
                          "left join Mappings on Mappings.AttributeID = Attributes.AttributeID  " \
                          "left join Instances on Instances.InstanceID = Mappings.InstanceID  " \
                          "left join InstanceCategories  on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID  " \
                          "left join Connections on Connections.LinkInstanceID = Instances.InstanceID  " \
                          "left join Instances AS StartNodeInstance  on StartNodeInstance.InstanceID = Connections.StartNodeInstanceID  " \
                          "left join Mappings AS MappingStartNodeInstance  on MappingStartNodeInstance.InstanceID = StartNodeInstance.InstanceID " \
                          "left join Attributes AS AttributesStartNodeInstance  on AttributesStartNodeInstance.AttributeID = MappingStartNodeInstance.AttributeID " \
                          "left join ObjectTypes AS ObjectTypeStartNodeInstance on ObjectTypeStartNodeInstance.ObjectTypeID = AttributesStartNodeInstance.ObjectTypeID  " \
                          "left join Instances AS EndNodeInstance  on EndNodeInstance.InstanceID = Connections.EndNodeInstanceID  " \
                          "left join Mappings AS MappingEndNodeInstance on MappingEndNodeInstance.InstanceID = EndNodeInstance.InstanceID  " \
                          "left join Attributes AS AttributesEndNodeInstance  on AttributesEndNodeInstance.AttributeID = MappingEndNodeInstance.AttributeID  " \
                          "left join ObjectTypes AS ObjectTypeEndNodeInstance  on ObjectTypeEndNodeInstance.ObjectTypeID = AttributesEndNodeInstance.ObjectTypeID  " \
                          "left join ScenarioMappings  on ScenarioMappings.MappingID = Mappings.MappingID  " \
                          "left join Scenarios on Scenarios.ScenarioID=ScenarioMappings.ScenarioID  " \
                          "left join MasterNetworks on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID  " \
                          "left join Methods on Methods.MethodID  = Mappings.MethodID  " \
                          "left join Sources on Sources.SourceID  = Mappings.SourceID   " \
                          "WHERE 'ObjectTypes'.'ObjectTypologyCV'='Link'  AND Attributes.AttributeName='ObjectTypeInstances' " \
                          "AND AttributesStartNodeInstance.AttributeName='ObjectTypeInstances'  AND AttributesEndNodeInstance.AttributeName='ObjectTypeInstances' " \
                          "AND ResourceTypeAcronym='{}' AND MasterNetworkName='{}' " \
                          "AND ScenarioName='{}'".format(selectedResourceType, masterNetworkName, scenarioName)
            result = self.session.execute(sql_command)

            complete_result = list()

            for row in result:
                complete_result.append([row.LinkObjectType, row.LinkInstanceName,
                                        row.InstanceNameCV, row.ScenarioName,
                                        row.SourceName, row.MethodName,
                                        row.StartNodeInstanceName, row.EndNodeInstanceName,
                                        row.InstanceCategory, row.Description])
            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)