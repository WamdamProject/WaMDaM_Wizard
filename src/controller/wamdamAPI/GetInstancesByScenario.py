
import pandas as pd
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq

'''
    This class is used to get result that query to get data of instances in sqlite db.
'''

class GetInstancesBySenario(object):
    def __init__(self, pathOfSqlite=''):
        self.setup = DB_Setup()
        if self.setup.get_session() == None and pathOfSqlite != '':
            self.setup.connect(pathOfSqlite, db_type='sqlite')

        self.session = self.setup.get_session()

        self.excel_pointer = None

    def GetMasterNetworks(self, selectedResourceType=''):
        '''
            This method is used to get data from MasterNetworks table by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of MasterNetworkName and set of data queried
        '''
        try:
                # get all data
            Network_sql_command = """
                    Select DISTINCT MasterNetworkName,ResourceTypeAcronym, 
                    SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description'
                    
                    FROM ResourceTypes 
                    
                    left join ObjectTypes 
                    on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  
                    
                    left join Attributes 
                    on Attributes.ObjectTypeid = Objecttypes.Objecttypeid 
                    
                    left join Mappings
                    on Mappings.Attributeid = Attributes.Attributeid  
                    
                    left join Instances 
                    on instances.instanceid = Mappings.Instanceid 
                    
                    left join Scenariomappings
                    on ScenarioMappings.Mappingid = Mappings.Mappingid 
                    
                    left join Scenarios 
                    on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  
                    
                    left join MasterNetworks 
                    on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  
                    
                    WHERE ObjectTypologyCV='Network' and MasterNetworkName is not null
                     AND 
                                                 
                    ResourceTypeAcronym = '{}'""".format(selectedResourceType)

            Network_Result_df = pd.DataFrame(list(self.session.execute(Network_sql_command)))

            Network_Result_df_df_columns = list(self.session.execute(Network_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Network_Result_df.empty:
                Links_Result_df = pd.DataFrame(columns=Network_Result_df_df_columns)
            else:
                Network_Result_df.columns = Network_Result_df_df_columns
            return Network_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetMasterNetworks.\n' + e.message)


    def GetScenarios(self, selectedResourceType='', selectedMasterNetworkName=''):
        '''
            This method is used to get data from Scenarios table by selected ResourceTypeAcronym and MasterNetworkName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :return: list of ScenarioName and set of data queried
        '''
        try:
            # get all data
            Scenarios_sql_command = """
                    Select DISTINCT ScenarioName,MasterNetworkName,SourceName,MethodName,ScenarioStartDate,ScenarioEndDate,TimeStepValue,
                    TimeStepUnitCV,ScenarioParentName,ScenarioType,Scenarios.Description As Description
                                    FROM ResourceTypes 
                                    left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  
                                    left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid 
                                    left join Mappings on Mappings.Attributeid = Attributes.Attributeid  
                                    left join Instances on instances.instanceid = Mappings.Instanceid 
                                    left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
                                    left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  
                                    left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  
                                      left join Methods on Methods.MethodID  = Mappings.MethodID 
                                     left join Sources on Sources.SourceID  = Mappings.SourceID   
                                    WHERE ObjectTypologyCV='Network' 
                                    AND AttributeName='ObjectTypeInstances'
                                    AND 
                                   ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' """.format(selectedResourceType,selectedMasterNetworkName)

            Scenarios_Result_df = pd.DataFrame(list(self.session.execute(Scenarios_sql_command)))
            Scenarios_Result_df_columns = list(self.session.execute(Scenarios_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Scenarios_Result_df.empty:
                Scenarios_Result_df = pd.DataFrame(columns=Scenarios_Result_df_columns)
            else:
                Scenarios_Result_df.columns = Scenarios_Result_df_columns
            return Scenarios_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetScenarios.\n' + e.message)




    def GetNodesByScenario(self, selectedResourceType='', selectedMasterNetworkName='', SelectedScenarioName=''):
        '''
            This method is used to get data of Nodes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried and InstanceName
        '''
        try:
            Nodes_sql_command = """
        Select DISTINCT ObjectType,InstanceName,InstanceNameCV,ScenarioName ,SourceName,MethodName,InstanceCategory,Longitude_x ,Latitude_y,
            Instances.Description
            FROM ResourceTypes 
            left join ObjectTypes on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID  
            left join Attributes on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID 
            left join Mappings on Mappings.AttributeID = Attributes.AttributeID  
            left join Instances on Instances.InstanceID = Mappings.InstanceID 
            left join InstanceCategories on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID 
            left join ScenarioMappings on ScenarioMappings.MappingID = Mappings.MappingID 
            left join Scenarios on Scenarios.ScenarioID=ScenarioMappings.ScenarioID 
            left join MasterNetworks on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID 
            left join Methods on Methods.MethodID  = Mappings.MethodID 
            left join Sources on Sources.SourceID  = Mappings.SourceID   
            WHERE ObjectTypologyCV='Node' AND Attributes.AttributeName='ObjectTypeInstances' ANd ObjectType !='ObjectTypeInstances' AND InstanceName is not null
                    
                     AND ResourceTypeAcronym='{}' AND MasterNetworkName='{}' AND ScenarioName='{}'""".format(selectedResourceType, selectedMasterNetworkName, SelectedScenarioName)

            Nodes_Result_df = pd.DataFrame(list(self.session.execute(Nodes_sql_command)))
            Nodes_Result_df_columns = list(self.session.execute(Nodes_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Nodes_Result_df.empty:
                Nodes_Result_df = pd.DataFrame(columns=Nodes_Result_df_columns)
            else:
                Nodes_Result_df.columns = Nodes_Result_df_columns
            return Nodes_Result_df

        except Exception as e:
        # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetNodesByScenario.\n' + e.message)



    def GetLinksByScenario(self, selectedResourceType='', selectedMasterNetworkName='', SelectedScenarioName=''):
        """
            This method is used to get data of Linkes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried
        """
        try:
            Links_sql_command = """
                    Select ObjectType AS LinkObjectType,
                    Instances.InstanceName As LinkInstanceName, 
                    Instances.InstanceNameCV,
                    ScenarioName,
                    SourceName,
                    MethodName,
                    StartNodeInstance.InstanceName As StartEndNode,
                    EndNodeInstance.InstanceName As EndNodeInstance,
                    InstanceCategory,
                    Instances.Description
                    
                    FROM ResourceTypes
                    
                    left join ObjectTypes 
                    on ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID 
                    
                    left join Attributes 
                    on Attributes.ObjectTypeID = ObjectTypes.ObjectTypeID 
                    
                    left join Mappings 
                    on Mappings.AttributeID = Attributes.AttributeID 
                    
                    left join Instances 
                    on Instances.InstanceID = Mappings.InstanceID 
                     
                    left join InstanceCategories 
                    on InstanceCategories.InstanceCategoryID = Instances.InstanceCategoryID 
                     
                    left join Connections
                    on Connections.LinkInstanceID = Instances.InstanceID 
                    
                    left join Instances AS StartNodeInstance 
                    on StartNodeInstance.InstanceID = Connections.StartNodeInstanceID 
                    
                    left join Mappings AS MappingStartNodeInstance 
                    on MappingStartNodeInstance.InstanceID = StartNodeInstance.InstanceID
                    
                    left join Attributes AS AttributesStartNodeInstance 
                    on AttributesStartNodeInstance.AttributeID = MappingStartNodeInstance.AttributeID
                     
                    left join Instances AS EndNodeInstance 
                    on EndNodeInstance.InstanceID = Connections.EndNodeInstanceID 
                    
                    left join Mappings AS MappingEndNodeInstance
                    on MappingEndNodeInstance.InstanceID = EndNodeInstance.InstanceID 
                     
                    left join Attributes AS AttributesEndNodeInstance 
                    on AttributesEndNodeInstance.AttributeID = MappingEndNodeInstance.AttributeID 
                    
                    left join ScenarioMappings 
                    on ScenarioMappings.MappingID = Mappings.MappingID 
                    
                    left join Scenarios 
                    on Scenarios.ScenarioID=ScenarioMappings.ScenarioID 
                    
                    left join MasterNetworks 
                    on MasterNetworks.MasterNetworkID = Scenarios.MasterNetworkID 
                    
                    left join Methods 
                    on Methods.MethodID  = Mappings.MethodID 
                    
                    left join Sources 
                    On Sources.SourceID  = Mappings.SourceID  
                    
                    WHERE ObjectTypologyCV="Link"
                    
                    AND Attributes.AttributeName='ObjectTypeInstances'
                    AND AttributesStartNodeInstance.AttributeName='ObjectTypeInstances' 
                    AND AttributesEndNodeInstance.AttributeName='ObjectTypeInstances'
                    AND ResourceTypeAcronym='{}' AND MasterNetworkName='{}' AND ScenarioName='{}'""".format(
                    selectedResourceType, selectedMasterNetworkName, SelectedScenarioName)

            Links_Result_df = pd.DataFrame(list(self.session.execute(Links_sql_command)))
            Links_Result_df_columns = list(self.session.execute(Links_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Links_Result_df.empty:
                Links_Result_df = pd.DataFrame(columns=Links_Result_df_columns)
            else:
                Links_Result_df.columns = Links_Result_df_columns

            return Links_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetLinksByScenario.\n' + e.message)