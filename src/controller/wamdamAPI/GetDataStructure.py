
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq
from sqlalchemy.orm import aliased

'''
    This class is used to get result that query to get needed data in sqlite db.
'''
class GetDataStructure(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
        self.excel_pointer = None

    def getResourceTypes(self, dset_acro=None):
        '''
            This method is used to get all data in "ResourceTypes" table of sqlite db.
            :return: list of row
        '''
        try:
            result = self.session.query(sq.ResourceTypes).all()
            return result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Could not open ResourceTypes table.\n' + e.message)
            print(e)
        # for row in result:
        #     print row.ResourceType

    def get_excel(self):
        pass
    def getResourceType(self, selectedResourceType):
        '''
            This method is used to get DatasetTypes by selected ResourceTypeAcronym.
            First, It is filtered ResourceTypes table by selected ResourceTypeAcronym.
            Next, Get data by comparing SourceID of Sources and ResourceTypes.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of ResourceType, ResourceTypeAcronym, SourceName and Description queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ResourceTypes.ResourceType,
                                        sq.ResourceTypes.Description, sq.Sources.SourceName).filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.ResourceTypes.SourceID).all()
            complete_result = list()

            nameResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.ResourceTypeAcronym:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.ResourceTypeAcronym)
                    complete_result.append([row.ResourceType, row.ResourceTypeAcronym, row.SourceName, row.Description])

            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)
        pass
    def getObjecttypes(self, selectedResourceType):
        '''
            This method is used to get ObjectTypes by selected ResourceTypeAcronym.
            First, It is filtered ResourceTypes table by selected ResourceTypeAcronym.
            Next, Compare ResourceTypeID of ObjectTypes and ResourceTypes tables and join those result.
            Next, Compare ObjectCategoriesID of ObjectCategories and ObjectTypes tables and join those result.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType,
                                        sq.ObjectTypes.ObjectTypologyCV, sq.ObjectTypes.ObjectTypeCV,
                                        sq.ObjectCategories.ObjectCategoriesName, sq.ObjectTypes.Description).filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.ObjectTypes,
                         sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID).\
                    join(sq.ObjectCategories, sq.ObjectCategories.ObjectCategoriesID == sq.ObjectTypes.ObjectCategoriesID).all()
            complete_result = list()

            nameResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.ObjectType:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.ObjectType)
                    complete_result.append([row.ObjectType, row.ObjectTypologyCV, row.ResourceTypeAcronym,
                                            row.ObjectTypeCV, "", "",
                                            row.ObjectCategoriesName, row.Description])

            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)
    def getAttributes(self, selectedResourceType):
        '''
            This method is used to get Attributes by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType,
                                        sq.Attributes.AttributeName, sq.Attributes.AttributeDataTypeCV,
                                        sq.Attributes.AttributeNameCV, sq.Attributes.AttributeCategories,
                                        sq.Attributes.UnitNameCV, sq.Attributes.ModelInputOrOutput,
                                        sq.Attributes.AttributeDescription).filter(sq.ResourceTypes.ResourceTypeAcronym==selectedResourceType).\
                    join(sq.ObjectTypes,
                         sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID).\
                    join(sq.Attributes,
                         sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID).all()
            complete_result = list()

            #Get data the remaining data except overlapping AttributeName.
            nameResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.AttributeName or row.AttributeName == "ObjectTypeInstances":
                        isExisting = True
                        break
                if not isExisting:
                    if row.AttributeCategories != "" and row.AttributeCategories != "FALSE":
                        nameResult.append(row.AttributeName)
                        complete_result.append([row.ObjectType, row.AttributeName, row.UnitNameCV,
                                                row.AttributeDataTypeCV, row.AttributeNameCV, row.AttributeCategories,
                                                row.ModelInputOrOutput, row.AttributeDescription])

            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def getMasterNetwork(self, selectedResourceType):
        '''
            This method is used to get data from MasterNetworks table by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of MasterNetworkName and set of data queried
        '''
        try:
            result = self.session.execute("Select ResourceTypeAcronym,MasterNetworkName, SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description' "\
                                            "FROM ResourceTypes "\
                                            "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
                                            "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
                                            "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
                                            "left join Instances on instances.instanceid = Mappings.Instanceid "\
                                            "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
                                            "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
                                            "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
                                            "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network' ".format(selectedResourceType))
            #Get data the remaining data except overlapping MasterNetworkName.
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

    def getScenario(self, selectedResourceType, masterNetworkName):
        '''
            This method is used to get data from Scenarios table by selected ResourceTypeAcronym and MasterNetworkName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :return: list of ScenarioName and set of data queried
        '''
        try:
            result = self.session.execute("Select ResourceTypeAcronym,ObjectType,ObjectTypologyCV,AttributeName,InstanceName,MasterNetworkName,ScenarioName, "\
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
                                            "ORDER BY InstanceName DESC".format(selectedResourceType, masterNetworkName))
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

    def getNodes(self, selectedResourceType, masterNetworkName, scenarioName):
        '''
            This method is used to get data of Nodes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried and InstanceName
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType, sq.Instances.InstanceName,
                                        sq.Instances.InstanceNameCV, sq.Scenarios.ScenarioName,
                                        sq.Sources.SourceName, sq.Methods.MethodName,
                                        sq.InstanceCategories.InstanceCategories, sq.Instances.Longitude_x,
                                        sq.Instances.Latitude_y, sq.Instances.Description).\
                    join(sq.ObjectTypes,
                         sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID).\
                    join(sq.Attributes,
                         sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID).\
                    join(sq.Mappings,
                         sq.Mappings.AttributeID == sq.Attributes.AttributeID).\
                    join(sq.Instances,
                         sq.Instances.InstanceID == sq.Mappings.InstanceID).\
                    join(sq.InstanceCategories,
                         sq.InstanceCategories.InstanceCategoryID == sq.Instances.InstanceCategoryID).\
                    join(sq.Connections,
                         sq.Instances.InstanceID == sq.Connections.LinkInstanceID).\
                    join(sq.ScenarioMappings,
                         sq.ScenarioMappings.MappingID == sq.Mappings.MappingID).\
                    join(sq.Scenarios,
                         sq.Scenarios.ScenarioID == sq.ScenarioMappings.ScenarioID).\
                    join(sq.MasterNetworks,
                         sq.MasterNetworks.MasterNetworkID == sq.Scenarios.MasterNetworkID).\
                    join(sq.Methods,
                         sq.Methods.MethodID == sq.Mappings.MethodID).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.Mappings.SourceID).\
                    filter(sq.Attributes.AttributeName == "ObjectTypeInstances").\
                    filter(sq.Scenarios.ScenarioName == scenarioName).all()
            #Get data the remaining data except overlapping InstanceName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.InstanceName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.InstanceName)
                    dataResult.append([row.ObjectType, row.InstanceName,
                                        row.InstanceNameCV, row.ScenarioName,
                                        row.SourceName, row.MethodName,
                                        row.InstanceCategories, row.Longitude_x,
                                        row.Latitude_y, row.Description])

            return nameResult, dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def getLinkes(self, selectedResourceType, masterNetworkName, scenarioName):
        '''
            This method is used to get data of Linkes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried
        '''
        try:
            StartInstance = aliased(sq.Instances)
            MetadataStartNodeInstace = aliased(sq.Mappings)
            EndInstance = aliased(sq.Instances)
            AttStartNodeInstance = aliased(sq.Attributes)
            AttEndNodeInstance = aliased(sq.Attributes)
            AttLinkInstance = aliased(sq.Attributes)
            AttLinkEndInstance = aliased(sq.Attributes)
            ObjectTypeEndNodeInstance = aliased(sq.ObjectTypes)
            ObjectTypeStartNodeInstance = aliased(sq.ObjectTypes)
            MetadataEndNodeInstace = aliased(sq.Mappings)
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType, sq.Instances.InstanceName,
                                        sq.Instances.InstanceNameCV, sq.Scenarios.ScenarioName,
                                        sq.Sources.SourceName, sq.Methods.MethodName,
                                        StartInstance.InstanceName, EndInstance.InstanceName,
                                        sq.InstanceCategories.InstanceCategories, sq.Instances.Description).\
                    join(sq.ObjectTypes,
                         sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID).\
                    join(sq.Attributes,
                         sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID).\
                    join(sq.Mappings,
                         sq.Mappings.AttributeID == sq.Attributes.AttributeID).\
                    join(sq.ScenarioMappings,
                         sq.ScenarioMappings.MappingID == sq.Mappings.MappingID).\
                    join(sq.Scenarios,
                         sq.Scenarios.ScenarioID == sq.ScenarioMappings.ScenarioID).\
                    join(sq.MasterNetworks,
                         sq.MasterNetworks.MasterNetworkID == sq.Scenarios.MasterNetworkID).\
                    join(sq.Instances,
                         sq.Instances.InstanceID == sq.Mappings.InstanceID).\
                    join(sq.InstanceCategories,
                         sq.InstanceCategories.InstanceCategoryID == sq.Instances.InstanceCategoryID).\
                    join(sq.Connections,
                         sq.Instances.InstanceID == sq.Connections.LinkInstanceID).\
                    join(StartInstance,
                         StartInstance.InstanceID == sq.Connections.StartNodeInstanceID).\
                    join(EndInstance,
                         EndInstance.InstanceID == sq.Connections.EndNodeInstanceID).\
                    join(MetadataStartNodeInstace,
                         MetadataStartNodeInstace.InstanceID == StartInstance.InstanceID).\
                    join(AttStartNodeInstance,
                         AttStartNodeInstance.AttributeID == MetadataStartNodeInstace.AttributeID).\
                    join(ObjectTypeStartNodeInstance,
                         ObjectTypeStartNodeInstance.ObjectTypeID == AttStartNodeInstance.ObjectTypeID).\
                    join(AttLinkInstance,
                         AttLinkInstance.AttributeID == AttStartNodeInstance.AttributeID).\
                    join(MetadataEndNodeInstace,
                         MetadataEndNodeInstace.InstanceID == EndInstance.InstanceID).\
                    join(AttEndNodeInstance,
                         AttEndNodeInstance.AttributeID == MetadataEndNodeInstace.AttributeID).\
                    join(ObjectTypeEndNodeInstance,
                         ObjectTypeEndNodeInstance.ObjectTypeID == AttEndNodeInstance.ObjectTypeID).\
                    join(AttLinkEndInstance,
                         AttLinkEndInstance.AttributeID == AttEndNodeInstance.AttributeID).\
                    join(sq.Methods,
                         sq.Methods.MethodID == sq.Mappings.MethodID).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.Mappings.SourceID).\
                    filter(AttLinkInstance.AttributeName == "ObjectTypeInstances").\
                    filter(sq.Attributes.AttributeName == "ObjectTypeInstances").\
                    filter(AttLinkEndInstance.AttributeName == "ObjectTypeInstances").all()
            complete_result = list()

            for row in result:
                complete_result.append([row.ObjectType, row[2],
                                        row.InstanceNameCV, row.ScenarioName,
                                        row.SourceName, row.MethodName,
                                        row[7], row[8],
                                        row.InstanceCategories, row.Description])
            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetOrganizations(self, selectedResourceType):
        '''
            This method is used to get data of Organizations by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.Organizations.OrganizationName, sq.Organizations.OrganizationType,
                                        sq.Organizations.OrganizationWebpage, sq.Organizations.Description).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.ResourceTypes.SourceID).\
                    join(sq.People,
                         sq.People.PersonID == sq.Sources.PersonID).\
                    join(sq.Organizations,
                         sq.Organizations.OrganizationID == sq.People.OrganizationID).all()
            #Get data the remaining data except overlapping OrganizationName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.OrganizationName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.OrganizationName)
                    dataResult.append([row.OrganizationName, row.OrganizationType,
                                       row.OrganizationWebpage, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetPeople(self, selectedResourceType):
        '''
            This method is used to get data of People by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.People.PersonName, sq.People.Address,
                                        sq.People.Email, sq.People.Phone, sq.People.PersonWebpage,
                                        sq.People.Position).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.ResourceTypes.SourceID).\
                    join(sq.People,
                         sq.People.PersonID == sq.Sources.PersonID).all()
            #Get data the remaining data except overlapping PersonName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.PersonName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.PersonName)
                    dataResult.append([row.PersonName, row.Address,
                                       row.Email, row.Phone, row.PersonWebpage,
                                       row.Position])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetSources(self, selectedResourceType):
        '''
            This method is used to get data of Sources by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.Sources.SourceName, sq.Sources.SourceWebpage,
                                        sq.Sources.SourceCitation, sq.Sources.Description).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.ResourceTypes.SourceID).all()
            #Get data the remaining data except overlapping SourceName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.SourceName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.SourceName)
                    dataResult.append([row.SourceName, row.SourceWebpage,
                                       row.SourceCitation, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)

    def GetMethods(self, selectedResourceType):
        '''
            This method is used to get data of Methods by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.Methods.MethodName, sq.Methods.MethodWebpage,
                                        sq.Methods.MethodCitation, sq.Methods.MethodTypeCV, sq.Methods.Description).\
                    filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
                    join(sq.Sources,
                         sq.Sources.SourceID == sq.ResourceTypes.SourceID).\
                    join(sq.Methods,
                         sq.Sources.PersonID == sq.Methods.PersonID).all()
            #Get data the remaining data except overlapping MethodName.
            nameResult = list()
            dataResult = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.MethodName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.MethodName)
                    dataResult.append([row.MethodName, row.MethodWebpage,
                                       row.MethodCitation, row.MethodTypeCV, row.Description])

            return dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data Structure.\n' + e.message)