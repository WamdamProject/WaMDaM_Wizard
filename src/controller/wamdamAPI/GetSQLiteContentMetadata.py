from ..ConnectDB_ParseExcel import DB_Setup


import pandas as pd

class GetSQLiteContentMetadata(object):
    def __init__(self):
        self.setup = DB_Setup()

        self.session = self.setup.get_session()
    def GetResourceTypes(self):
        ResourceTypes_sql_command = """SELECT DISTINCT  ResourceType 
                      FROM ResourceTypes  
                      LEFT JOIN Methods ON Methods.MethodID=ResourceTypes.MethodID 
                      """
        ResourceTypes_Result_df =  pd.DataFrame(list( self.session.execute(ResourceTypes_sql_command)))
        return ResourceTypes_Result_df

    def GetCVObjectTypes(self):
        CVObjectTypes_sql_command = """SELECT DISTINCT  ObjectTypeCV
                            FROM ResourceTypes 
                              LEFT JOIN ObjectTypes ON ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID
                              LEFT JOIN  ObjectCategories ON ObjectCategories.ObjectCategoryID=ObjectTypes.ObjectCategoryID
			                Where ObjectTypeCV!='Network'
                                """
        CVObjectTypes_Result_df = pd.DataFrame(list(self.session.execute(CVObjectTypes_sql_command)))
        return CVObjectTypes_Result_df

    def CVAttributes(self):
        CVAttributes_sql_command ="""SELECT  DISTINCT AttributeNameCV
                           
                            FROM "ResourceTypes"
                            
                            LEFT JOIN "ObjectTypes" 
                            ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
                            
                            LEFT JOIN  "ObjectCategories"
                            ON "ObjectCategories"."ObjectCategoryID"="ObjectTypes"."ObjectCategoryID" 
                            
                            LEFT JOIN  "Attributes"
                            ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                            
                            LEFT JOIN  "AttributeCategories"
                            ON "AttributeCategories"."AttributeCategoryID"="Attributes"."AttributeCategoryID" 
                            
                            WHERE 
                            --exclude the dummy attributes that are just used to connect Object Types with their Instances. 
                            -- Provide the model name 
                            AttributeNameCV!=''
                            """
        CVAttributes_Result_df = pd.DataFrame(list(self.session.execute(CVAttributes_sql_command)))
        return CVAttributes_Result_df

    def MasterNetworks(self):

        # Networks
        MasterNetworks_sql_command ="""
        Select DISTINCT MasterNetworkName
        FROM ResourceTypes 
        left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid 
        left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid 
        left join Mappings on Mappings.Attributeid = Attributes.Attributeid  
        left join Instances on instances.instanceid = Mappings.Instanceid 
        left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid 
        left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  
        left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid 
        
        WHERE MasterNetworkName!=''
        """
        MasterNetworks_Result_df = pd.DataFrame(list(self.session.execute(MasterNetworks_sql_command)))
        return MasterNetworks_Result_df

    def Scenarios(self):

        # Scenarios
        Scenarios_sql_command ="""
        Select DISTINCT ScenarioName
        FROM ResourceTypes
        left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid
        left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid
        left join Mappings on Mappings.Attributeid = Attributes.Attributeid
        left join Instances on instances.instanceid = Mappings.Instanceid
        left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
        left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
        left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid
        left join Methods on Methods.Methodid = Mappings.Methodid
        left join Sources on Sources.Sourceid = Mappings.Sourceid
        WHERE ScenarioName!=''
        """
        Scenarios_Result_df = pd.DataFrame(list(self.session.execute(Scenarios_sql_command)))
        return Scenarios_Result_df


# Extract Coverage



# People





# Sources




# Methods




# Methods

