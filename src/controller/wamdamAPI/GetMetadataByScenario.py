
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq
import pandas as pd

'''
This class is used to get data making sheets for meta data.
'''
class GetMetadataByScenario(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()

    def GetOrganizationsByScenario(self, selectedResourceType,selectedNetwork,selectedScenario):
        '''
            This method is used to get data of Organizations by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            Organizations_Sources_sql_command = """
        			Select DISTINCT ResourceTypeAcronym,OrganizationName,OrganizationType,OrganizationWebpage
                    FROM Organizations
                    LEFT JOIN People ON People.OrganizationID=Organizations.OrganizationID
        			LEFT JOIN Sources ON Sources.PersonID=People.PersonID
                    LEFT JOIN Mappings On Mappings.SourceID=Sources.SourceID
                    left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
                    left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
                    left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid
                    LEFT JOIN Attributes on Attributes.AttributeID=Mappings.AttributeID
                    LEFT JOIN ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID
                    LEFT JOIN ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID
                    WHERE 
                    ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(
                selectedResourceType, selectedNetwork, selectedScenario)

            Organizations_Sources_Result_df = pd.DataFrame(list(self.session.execute(Organizations_Sources_sql_command)))


            Organizations_Methods_sql_command = """
                Select DISTINCT ResourceTypeAcronym,OrganizationName,OrganizationType,OrganizationWebpage
                FROM Organizations
                LEFT JOIN People ON People.OrganizationID=Organizations.OrganizationID
                LEFT JOIN Methods ON Methods.PersonID=People.PersonID
                LEFT JOIN Mappings On Mappings.MethodID=Methods.MethodID
                left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
                left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
                left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid
                LEFT JOIN Attributes on Attributes.AttributeID=Mappings.AttributeID
                LEFT JOIN ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID
                LEFT JOIN ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID
                WHERE 
                ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(
                    selectedResourceType, selectedNetwork, selectedScenario)

            Organizations_Methods_Result_df = pd.DataFrame(list(self.session.execute(Organizations_Methods_sql_command)))
            frames=[]
            # combine the Organizations who serve as sources and methods

            frames = [Organizations_Methods_Result_df, Organizations_Sources_Result_df]

            Organizations_Result_df = pd.concat(frames)

            Organizations_Result_df_columns = list(self.session.execute(Organizations_Methods_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel

            Organizations_Result_df.columns = Organizations_Result_df_columns

            return Organizations_Result_df


        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetOrganizationsByScenario .\n' + e.message)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def GetPeopleByScenario(self, selectedResourceType,selectedNetwork,selectedScenario):
        '''
            This method is used to get data of People by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            People_Sources_sql_command = """
            Select DISTINCT PersonName,Address, Email,PersonWebpage,Position 
            FROM People
            LEFT JOIN Sources ON Sources.PersonID=People.PersonID
            LEFT JOIN Mappings On Mappings.SourceID=Sources.SourceID
            left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
            left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
            left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid
            LEFT JOIN Attributes on Attributes.AttributeID=Mappings.AttributeID
            LEFT JOIN ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID
            LEFT JOIN ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID
            WHERE 
            ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)

            People_Sources_Result_df = pd.DataFrame(list(self.session.execute(People_Sources_sql_command)))


            People_Methods_sql_command = """
            Select DISTINCT PersonName,Address, Email,PersonWebpage,Position 
            FROM People
            LEFT JOIN Methods ON Methods.PersonID=People.PersonID
		    LEFT JOIN Mappings On Mappings.MethodID=Methods.MethodID
            left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
            left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
            left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid
            LEFT JOIN Attributes on Attributes.AttributeID=Mappings.AttributeID
            LEFT JOIN ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID
            LEFT JOIN ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID
            
            WHERE 
            ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)

            # combine the people who serve as sources and methods
            People_Methods_Result_df = pd.DataFrame(list(self.session.execute(People_Methods_sql_command)))
            frames = [People_Methods_Result_df, People_Sources_Result_df]

            People_Result_df=pd.concat(frames)

            People_Result_df_columns = list(self.session.execute(People_Methods_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel

            People_Result_df.columns = People_Result_df_columns

            return People_Result_df



        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetPeopleByScenario data.\n' + e.message)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def GetSourcesByScenario(self, selectedResourceType,selectedNetwork,selectedScenario):
        '''
            This method is used to get data of Sources by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            Sources_sql_command = """
                 Select DISTINCT SourceName,SourceWebpage, SourceCitation,PersonName,Sources.Description as Description 
            FROM Sources
            
            LEFT JOIN People ON People.PersonID=Sources.PersonID 
            
            left join Mappings on Mappings.SourceID = Sources.SourceID 
            
            left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
            
            left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
            
            left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  
            
            left join Attributes on Attributes.AttributeID = Mappings.AttributeID 
            
            left join ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID 
            
            left join ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID 
            
            
            WHERE SourceName is not NULL        AND
                ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)


            Sources_Result_df = pd.DataFrame(list(self.session.execute(Sources_sql_command)))
            Sources_Result_df_columns = list(self.session.execute(Sources_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Sources_Result_df.empty:
                Sources_Result_df = pd.DataFrame(columns=Sources_Result_df_columns)
            else:
                Sources_Result_df.columns = Sources_Result_df_columns


            return Sources_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetSourcesByScenario.\n' + e.message)

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def GetMethodsByScenario(self, selectedResourceType,selectedNetwork,selectedScenario):
        '''
            This method is used to get data of Methods by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            Methods_sql_command = """
           Select DISTINCT MethodName,MethodWebpage, MethodCitation,MethodTypeCV,PersonName,Methods.Description as Description 
            FROM Methods
            
            LEFT JOIN People ON People.PersonID=Methods.PersonID 
            
            left join Mappings on Mappings.MethodID = Methods.MethodID 
            
            left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid
            
            left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid
            
            left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  
            
            left join Attributes on Attributes.AttributeID = Mappings.AttributeID 
            
            left join ObjectTypes on ObjectTypes.ObjectTypeID=Attributes.ObjectTypeID 
            
            left join ResourceTypes on ResourceTypes.ResourceTypeID=ObjectTypes.ResourceTypeID 
            
            
            WHERE MethodName is not NULL   AND      
            ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)

            Methods_Result_df = pd.DataFrame(list(self.session.execute(Methods_sql_command)))
            Methods_Result_df_columns = list(self.session.execute(Methods_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Methods_Result_df.empty:
                Sources_Result_df = pd.DataFrame(columns=Methods_Result_df_columns)
            else:
                Methods_Result_df.columns = Methods_Result_df_columns

            return Methods_Result_df


        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetMethodsByScenario.\n' + e.message)

