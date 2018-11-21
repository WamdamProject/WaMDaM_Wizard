import wx
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq
import pandas as pd
from sqlalchemy.orm import aliased
from viewer.Messages_forms.msg_somethigWrong import msg_somethigWrong

'''
    This class is used to get result that query to get needed data in sqlite db.
'''
class GetResourceStructure(object):
    def __init__(self, pathOfSqlite=''):
        self.setup = DB_Setup()

        if self.setup.get_session() == None and pathOfSqlite != '':
            self.setup.connect(pathOfSqlite, db_type='sqlite')

        self.session = self.setup.get_session()

        self.excel_pointer = None

    def get_excel(self):
        pass

    def GetResourceType(self,selectedResourceTypeAcro= None):
        '''
            This method is used to get all data in "ResourceTypes" table of sqlite db.
            :return: list of row
        '''
        try:
            if selectedResourceTypeAcro != None:
                ResourceType_sql_command = """
                       SELECT DISTINCT  ResourceTypeAcronym,ResourceType,ResourceTypes.Description, MethodName 
                                            FROM ResourceTypes 
                                            LEFT JOIN Methods ON Methods.MethodID=ResourceTypes.MethodID 
                                            WHERE
                                           ResourceTypeAcronym = '{}' """.format(selectedResourceTypeAcro)
            else:
                ResourceType_sql_command = """
                                            SELECT DISTINCT  ResourceTypeAcronym,ResourceType,ResourceTypes.Description, MethodName 
                                            FROM ResourceTypes 
                                             LEFT JOIN Methods ON Methods.MethodID=ResourceTypes.MethodID """

            ResourceType_Result_df = pd.DataFrame(list(self.session.execute(ResourceType_sql_command)))
            ResourceType_Result_df_columns = list(self.session.execute(ResourceType_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if ResourceType_Result_df.empty:
                ResourceType_Result_df=pd.DataFrame(columns=ResourceType_Result_df_columns)
            else:
                ResourceType_Result_df.columns = ResourceType_Result_df_columns
            return ResourceType_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetResourceType.\n' + e.message)




    def GetObjectTypesByResource(self, selectedResourceTypeAcro):
        '''
            This method is used to get ObjectTypes by selected ResourceTypeAcronym.
            First, It is filtered ResourceTypes table by selected ResourceTypeAcronym.
            Next, Compare ResourceTypeID of ObjectTypes and ResourceTypes tables and join those result.
            Next, Compare ObjectCategoryID of ObjectCategories and ObjectTypes tables and join those result.
            :param  selectedResourceTypeAcro: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            ObjectTypes_sql_command = """
                      SELECT DISTINCT  ObjectType,ObjectTypologyCV,ResourceTypeAcronym,ObjectTypeCV,Layout,ObjectCategoryName,ObjectTypes.Description 
                                           FROM ResourceTypes 
                                            LEFT JOIN ObjectTypes ON ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID 
                                            LEFT JOIN  ObjectCategories ON ObjectCategories.ObjectCategoryID=ObjectTypes.ObjectCategoryID
                                            WHERE
                                           ResourceTypeAcronym = '{}' """.format(selectedResourceTypeAcro)

            ObjectTypes_Result_df = pd.DataFrame(list(self.session.execute(ObjectTypes_sql_command)))
            ObjectTypes_Result_df_columns = list(self.session.execute(ObjectTypes_sql_command).keys())

            table = list(self.session.execute(ObjectTypes_sql_command))
            if table:

                custom_dict = ['Network', 'Node', 'Link']
                sort_list = {}
                for row in table:
                    if not row[1] in sort_list.keys():
                        sort_list[row[1]] = [row]
                    else:
                        sort_list[row[1]].append(row)

                total_list = []
                for key in custom_dict:
                    if len(total_list) < 1:
                        total_list = sort_list[key]
                    else:
                        total_list.extend(sort_list[key])

                ObjectTypes_Result_df=pd.DataFrame(total_list)



            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if ObjectTypes_Result_df.empty:
                ObjectTypes_Result_df = pd.DataFrame(columns=ObjectTypes_Result_df_columns)
            else:
                ObjectTypes_Result_df.columns = ObjectTypes_Result_df_columns
            return ObjectTypes_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetResourceType.\n' + e.message)




    def GetAttributesByResource(self, selectedResourceTypeAcro = ''):
        '''
            This method is used to get Attributes by selected ResourceTypeAcronym.
            :param  selectedResourceTypeAcro: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            Attributes_sql_command = """
            SELECT  ObjectType,AttributeName,AttributeName_Abstract,AttributeNameCV,UnitName As AttributeUnit,UnitNameCV,AttributeDataTypeCV,AttributeCategoryName As AttributeCategory, 
            ModelInputOrOutput,Attributes.Description as AttributeDescription,AttributeScale
			 
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
            AttributeName!='ObjectTypeInstances' and
                        
            
            
                            ResourceTypeAcronym = '{}' """.format(selectedResourceTypeAcro)

            Attributes_Result_df = pd.DataFrame(list(self.session.execute(Attributes_sql_command)))
            Attributes_Result_df_columns = list(self.session.execute(Attributes_sql_command).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if Attributes_Result_df.empty:
                Attributes_Result_df = pd.DataFrame(columns=Attributes_Result_df_columns)
            else:
                Attributes_Result_df.columns = Attributes_Result_df_columns
            return Attributes_Result_df
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading  GetAttributesByResource.\n' + e.message)





