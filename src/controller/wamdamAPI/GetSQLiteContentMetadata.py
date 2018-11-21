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

    def GetCVAttributes(self):
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

    def GetMasterNetworks(self):

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

    def GetScenarios(self):

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



# People

    def GetPeople(self):
        People_sql_command ="""
        Select DISTINCT PersonName
        FROM
        People
        """
        People_Result_df = pd.DataFrame(list(self.session.execute(People_sql_command)))
        return People_Result_df



# Sources

    def GetSources(self):

        Sources_sql_command ="""
        Select DISTINCT SourceName
        FROM Sources
        """
        Sources_Result_df = pd.DataFrame(list(self.session.execute(Sources_sql_command)))
        return Sources_Result_df


# Methods

    def GetMethods(self):

        # Scenarios
        Methods_sql_command ="""
        Select DISTINCT MethodName
        FROM Methods
        """
        Methods_Result_df = pd.DataFrame(list(self.session.execute(Methods_sql_command)))
        return Methods_Result_df

# Organizations

    def GetOrganizations(self):

        # Organizations
        Organizations_sql_command ="""
        Select DISTINCT OrganizationName
        FROM Organizations
        """
        Organizations_Result_df = pd.DataFrame(list(self.session.execute(Organizations_sql_command)))
        return Organizations_Result_df

# Extract Coverage

    def GetSpatialCoverage(self):

        # Coverage
        East_Longitude__sql_command ="""
        Select max(Longitude_x) as East_Longitude
        FROM Instances
        """
        East_Longitude_value = list(self.session.execute(East_Longitude__sql_command))
        #------------------------------------------------------------------------

        West_Longitude_sql_command ="""
        Select min(Longitude_x) as West_Longitude
        FROM Instances
        """
        West_Longitude_value = list(self.session.execute(West_Longitude_sql_command))
        #------------------------------------------------------------------------

        South_Latitude__sql_command ="""
        Select Min(Latitude_y) as South_Latitudee
        FROM Instances
        """
        South_Latitude_value = list(self.session.execute(South_Latitude__sql_command))
        #------------------------------------------------------------------------

        North_Latitude__sql_command ="""
        Select Max(Latitude_y) as North_Latitude
        FROM Instances
        """
        North_Latitude_value = list(self.session.execute(North_Latitude__sql_command))

        return East_Longitude_value,West_Longitude_value,South_Latitude_value,North_Latitude_value


    def GetTemporalCoverage(self):
        start_date_sql_command = """
              Select Min(ScenarioStartDate) as start
              FROM Scenarios
              """
        start_value= list(self.session.execute(start_date_sql_command))
        # ------------------------------------------------------------------------

        end_date_sql_command ="""
                Select Min(ScenarioEndDate) as end
                FROM Scenarios
                """
        end_value = list(self.session.execute(end_date_sql_command))
        #------------------------------------------------------------------------

        return start_value,end_value

