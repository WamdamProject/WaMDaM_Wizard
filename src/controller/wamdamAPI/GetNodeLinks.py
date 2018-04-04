
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq
from sqlalchemy.orm import aliased

'''
This class is used to get data making sheets(Networks&Scenarios, Nodes and Links).
'''
class GetNodeLinks(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
    def GetCV_ObjectType(self):
        '''
        This method is used to get all names of CV_ObjectType.
        :return: list of CV_ObjectType's name
        '''
        result = self.session.query(sq.CV_ObjectType.Name).all()
        # complete_result = list()
        nameResult = list()
        for row in result:
            isExisting = False
            for name in nameResult:
                if name == row.Name:
                    isExisting = True
                    break
            if not isExisting:
                nameResult.append(row.Name)
                # complete_result.append([row.OrganizationName, row.OrganizationType, row.OrganizationWebpage,
                #                         row.Description])
        return nameResult
    def getMasterNetwork(self, CV_ObjectType, xmin, ymin, xmax, ymax):
        '''
        This method is used to get MasterNetwork according to selected CV_ObjectType.
        :param CV_ObjectType: selected CV_ObjectType
        :param xmin: value of Minimum (East)
        :param ymin: value of Minimum (South)
        :param xmax: value of Maximum (West)
        :param ymax: value of Maximum (North)
        :return: list of row (queried)
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType, sq.Attributes.AttributeName,
                            sq.Instances.InstanceName, sq.MasterNetworks.MasterNetworkName, sq.MasterNetworks.SpatialReferenceNameCV,
                            sq.Scenarios.ScenarioName, sq.MasterNetworks.VerticalDatumCV, sq.MasterNetworks.Description,
                            sq.Sources.SourceName, sq.Methods.MethodName)\
                .join(sq.ObjectTypes, sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID)\
                .join(sq.Attributes, sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID)\
                .join(sq.Mappings, sq.Mappings.AttributeID == sq.Attributes.AttributeID)\
                .join(sq.Instances, sq.Instances.InstanceID == sq.Mappings.InstanceID)\
                .join(sq.ScenarioMappings, sq.ScenarioMappings.MappingID == sq.Mappings.MappingID)\
                .join(sq.Scenarios, sq.Scenarios.ScenarioID == sq.ScenarioMappings.ScenarioID)\
                .join(sq.MasterNetworks, sq.MasterNetworks.MasterNetworkID == sq.Scenarios.MasterNetworkID)\
                .join(sq.Methods, sq.Methods.MethodID == sq.Mappings.MethodID)\
                .join(sq.Sources, sq.Sources.SourceID == sq.Mappings.SourceID)\
                .filter(sq.Attributes.AttributeName=='ObjectTypeInstances').\
                filter(sq.Instances.Longitude_x >= xmin).filter(sq.Instances.Latitude_y >= ymin)\
                .filter(sq.Instances.Longitude_x <= xmax).filter(sq.Instances.Latitude_y <= ymax).\
                filter(sq.ObjectTypes.ObjectTypologyCV == 'Node').filter(sq.ObjectTypes.ObjectTypeCV == CV_ObjectType)\
                .all()
            nameResult = list()
            complete_result = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.MasterNetworkName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.MasterNetworkName)
                    complete_result.append([row.MasterNetworkName, row.ResourceTypeAcronym, row.SpatialReferenceNameCV,
                                            row.VerticalDatumCV, row.Description])
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)
    def GetScenaroisResult(self, CV_ObjectType, xmin, ymin, xmax, ymax):
        '''
        This method is used to get Scenarios according to selected CV_ObjectType.
        :param CV_ObjectType: selected CV_ObjectType
        :param xmin: value of Minimum (East)
        :param ymin: value of Minimum (South)
        :param xmax: value of Maximum (West)
        :param ymax: value of Maximum (North)
        :return: list of row (queried)
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType, sq.ObjectTypes.ObjectTypeCV,
                            sq.ObjectTypes.ObjectTypologyCV, sq.Attributes.AttributeName, sq.Instances.InstanceName,
                            sq.Scenarios.ScenarioStartDate, sq.Scenarios.ScenarioEndDate,
                            sq.Scenarios.Description, sq.Scenarios.TimeStepValue, sq.Scenarios.TimeStepUnitCV,
                            sq.MasterNetworks.MasterNetworkName, sq.Scenarios.ScenarioName,
                            sq.Sources.SourceName, sq.Methods.MethodName)\
                .join(sq.ObjectTypes, sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID)\
                .join(sq.Attributes, sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID)\
                .join(sq.Mappings, sq.Mappings.AttributeID == sq.Attributes.AttributeID)\
                .join(sq.Instances, sq.Instances.InstanceID == sq.Mappings.InstanceID)\
                .join(sq.ScenarioMappings, sq.ScenarioMappings.MappingID == sq.Mappings.MappingID)\
                .join(sq.Scenarios, sq.Scenarios.ScenarioID == sq.ScenarioMappings.ScenarioID)\
                .join(sq.MasterNetworks, sq.MasterNetworks.MasterNetworkID == sq.Scenarios.MasterNetworkID)\
                .join(sq.Methods, sq.Methods.MethodID == sq.Mappings.MethodID)\
                .join(sq.Sources, sq.Sources.SourceID == sq.Mappings.SourceID)\
                .filter(sq.Attributes.AttributeName=='ObjectTypeInstances').\
                filter(sq.Instances.Longitude_x >= xmin).filter(sq.Instances.Latitude_y >= ymin)\
                .filter(sq.Instances.Longitude_x <= xmax).filter(sq.Instances.Latitude_y <= ymax).\
                filter(sq.ObjectTypes.ObjectTypologyCV == 'Node').filter(sq.ObjectTypes.ObjectTypeCV == CV_ObjectType)\
                .all()
            nameResult = list()
            complete_result = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.ScenarioName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.ScenarioName)
                    complete_result.append([row.ScenarioName, row.MasterNetworkName, row.SourceName,
                                            row.MethodName, row.ScenarioStartDate, row.ScenarioEndDate,
                                            row.TimeStepValue, row.TimeStepUnitCV, row.Description])
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)
    def GetNodesResult(self, CV_ObjectType, xmin, ymin, xmax, ymax):
        '''
        This method is used to get Instances according to selected CV_ObjectType.
        :param CV_ObjectType: selected CV_ObjectType
        :param xmin: value of Minimum (East)
        :param ymin: value of Minimum (South)
        :param xmax: value of Maximum (West)
        :param ymax: value of Maximum (North)
        :return: list of row (queried)
        '''
        try:
            result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType, sq.Attributes.AttributeName,
                            sq.Instances.InstanceName, sq.Instances.InstanceNameCV, sq.MasterNetworks.MasterNetworkName,
                            sq.Scenarios.ScenarioName, sq.InstanceCategories.InstanceCategory,
                            sq.Sources.SourceName, sq.Methods.MethodName, sq.Instances.Longitude_x,
                            sq.Instances.Latitude_y, sq.Instances.Description)\
                .join(sq.ObjectTypes, sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID)\
                .join(sq.Attributes, sq.Attributes.ObjectTypeID == sq.ObjectTypes.ObjectTypeID)\
                .join(sq.Mappings, sq.Mappings.AttributeID == sq.Attributes.AttributeID)\
                .join(sq.Instances, sq.Instances.InstanceID == sq.Mappings.InstanceID)\
                .join(sq.InstanceCategories, sq.InstanceCategories.InstanceCategoryID == sq.Instances.InstanceCategoryID)\
                .join(sq.ScenarioMappings, sq.ScenarioMappings.MappingID == sq.Mappings.MappingID)\
                .join(sq.Scenarios, sq.Scenarios.ScenarioID == sq.ScenarioMappings.ScenarioID)\
                .join(sq.MasterNetworks, sq.MasterNetworks.MasterNetworkID == sq.Scenarios.MasterNetworkID)\
                .join(sq.Methods, sq.Methods.MethodID == sq.Mappings.MethodID)\
                .join(sq.Sources, sq.Sources.SourceID == sq.Mappings.SourceID)\
                .filter(sq.Attributes.AttributeName=='ObjectTypeInstances').\
                filter(sq.Instances.Longitude_x >= xmin).filter(sq.Instances.Latitude_y >= ymin)\
                .filter(sq.Instances.Longitude_x <= xmax).filter(sq.Instances.Latitude_y <= ymax).\
                filter(sq.ObjectTypes.ObjectTypologyCV == 'Node').filter(sq.ObjectTypes.ObjectTypeCV == CV_ObjectType)\
                .all()
            nameResult = list()
            complete_result = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.InstanceName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.InstanceName)
                    complete_result.append([row.ObjectType, row.InstanceName, row.InstanceNameCV,
                                            row.ScenarioName, row.SourceName, row.MethodName,
                                            row.InstanceCategory, row.Longitude_x, row.Latitude_y, row.Description])
                return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)
    def GetLinksResult(self, CV_ObjectType, xmin, ymin, xmax, ymax):
        '''
        This method is used to get Links according to selected CV_ObjectType.
        :param CV_ObjectType: selected CV_ObjectType
        :param xmin: value of Minimum (East)
        :param ymin: value of Minimum (South)
        :param xmax: value of Maximum (West)
        :param ymax: value of Maximum (North)
        :return: list of row (queried)
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
                                        sq.InstanceCategories.InstanceCategory, sq.Instances.Description).\
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
                         sq.Sources.SourceID == sq.Mappings.SourceID)\
                    .filter(AttLinkInstance.AttributeName == "ObjectTypeInstances").\
                    filter(sq.Attributes.AttributeName == "ObjectTypeInstances").\
                    filter(AttLinkEndInstance.AttributeName == "ObjectTypeInstances")\
                    .all()
            nameResult = list()
            complete_result = list()
            for row in result:
                isExisting = False
                for name in nameResult:
                    if name == row.InstanceName:
                        isExisting = True
                        break
                if not isExisting:
                    nameResult.append(row.InstanceName)
                    complete_result.append([row.ObjectType, row.InstanceName, row.InstanceNameCV,
                                            row.ScenarioName, row.SourceName, row.MethodName,
                                            row[7], row[8],
                                            row.InstanceCategory, row.Description])
                return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)