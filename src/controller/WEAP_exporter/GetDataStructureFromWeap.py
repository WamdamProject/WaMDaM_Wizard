

from Extract_Network import Extract_Network


'''
    This class is used to get result that query to get needed data in sqlite db.
'''
class GetDataStructureFromWeap(object):
    def __init__(self, weap):
        self.WEAP = weap

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list, self.BranchesNew_list = Extract_Network(self.WEAP)

    # def getResourceTypes(self):
    #     '''
    #         This method is used to get all data in "ResourceTypes" table of sqlite db.
    #         :return: list of row
    #     '''
    #     try:
    #         result = self.session.query(sq.ResourceTypes).all()
    #         return result
    #     except Exception as e:
    #         # define.logger.error('Failed metAData load.\n' + e.message)
    #         raise Exception('Could not open ResourceTypes table.\n' + e.message)
    #         print(e)
    #     # for row in result:
    #     #     print row.ResourceType
    #
    # def get_excel(self):
    #     pass
    # def getResourceType(self, selectedResourceType =''):
    #     if selectedResourceType== None:
    #         try:
    #             result = self.session.query(sq.ResourceTypes).all()
    #             return result
    #         except Exception as e:
    #             # define.logger.error('Failed metAData load.\n' + e.message)
    #             raise Exception('Could not open ResourceTypes table.\n' + e.message)
    #             print(e)
    #     else:
    #         '''
    #             This method is used to get DatasetTypes by selected ResourceTypeAcronym.
    #             First, It is filtered ResourceTypes table by selected ResourceTypeAcronym.
    #             Next, Get data by comparing SourceID of Sources and ResourceTypes.
    #             :param  selectedResourceType: value of selected ResourceTypeAcronym.
    #             :return: list of set of ResourceType, ResourceTypeAcronym, SourceName and Description queried
    #         '''
    #         try:
    #             sql_command = "SELECT DISTINCT  ResourceTypeAcronym,ResourceType,ResourceTypes.Description, MethodName " \
    #                                         "FROM ResourceTypes " \
    #                                         "LEFT JOIN Methods ON Methods.MethodID=ResourceTypes.MethodID " \
    #                                         "WHERE ResourceTypeAcronym='{}'".format(selectedResourceType)
    #             if selectedResourceType == '' or selectedResourceType == None:
    #                 # get all data
    #                 sql_command = "SELECT DISTINCT  ResourceTypeAcronym,ResourceType,ResourceTypes.Description, MethodName " \
    #                                         "FROM ResourceTypes " \
    #                                         "LEFT JOIN Methods ON Methods.MethodID=ResourceTypes.MethodID "
    #
    #             result = self.session.execute(sql_command)
    #             # result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ResourceTypes.ResourceType,
    #             #                             sq.ResourceTypes.Description, sq.Methods.MethodName).filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
    #             #         join(sq.Methods,
    #             #              sq.Methods.MethodID == sq.ResourceTypes.MethodID).all()
    #             complete_result = list()
    #
    #             nameResult = list()
    #             for row in result:
    #                 isExisting = False
    #                 for name in nameResult:
    #                     if name == row.ResourceTypeAcronym:
    #                         isExisting = True
    #                         break
    #                 if not isExisting:
    #                     nameResult.append(row.ResourceTypeAcronym)
    #                     complete_result.append([row.ResourceType, row.ResourceTypeAcronym, row.MethodName, row.Description])
    #
    #             return complete_result
    #         except Exception as e:
    #             # define.logger.error('Failed metAData load.\n' + e.message)
    #             raise Exception('Error occurred in reading Data Structure.\n' + e.message)
    #         pass
    # def getObjecttypes(self, selectedResourceType=''):
    #     '''
    #         This method is used to get ObjectTypes by selected ResourceTypeAcronym.
    #         First, It is filtered ResourceTypes table by selected ResourceTypeAcronym.
    #         Next, Compare ResourceTypeID of ObjectTypes and ResourceTypes tables and join those result.
    #         Next, Compare ObjectCategoryID of ObjectCategories and ObjectTypes tables and join those result.
    #         :param  selectedResourceType: value of selected ResourceTypeAcronym.
    #         :return: list of set of data queried
    #     '''
    #     try:
    #         sql_command = "SELECT DISTINCT  ResourceTypeAcronym,ObjectType,ObjectTypologyCV,ObjectTypeCV,ObjectCategoryName, ObjectTypes.Description " \
    #                                         "FROM ResourceTypes " \
    #                                         "LEFT JOIN ObjectTypes ON ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID " \
    #                                         "LEFT JOIN  ObjectCategories ON ObjectCategories.ObjectCategoryID=ObjectTypes.ObjectCategoryID "\
    #                                         "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network'".format(selectedResourceType)
    #         if selectedResourceType == '' or selectedResourceType == None:
    #             # get all data
    #             sql_command = "SELECT DISTINCT  ResourceTypeAcronym,ObjectType,ObjectTypologyCV,ObjectTypeCV,ObjectCategoryName, ObjectTypes.Description " \
    #                                         "FROM ResourceTypes " \
    #                                         "LEFT JOIN ObjectTypes ON ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID " \
    #                                         "LEFT JOIN  ObjectCategories ON ObjectCategories.ObjectCategoryID=ObjectTypes.ObjectCategoryID "\
    #                                         "WHERE ObjectTypologyCV='Network'"
    #         result = self.session.execute(sql_command)
    #         # result = self.session.query(sq.ResourceTypes.ResourceTypeAcronym, sq.ObjectTypes.ObjectType,
    #         #                             sq.ObjectTypes.ObjectTypologyCV, sq.ObjectTypes.ObjectTypeCV,
    #         #                             sq.ObjectCategories.ObjectCategoryName,
    #         #                             sq.ObjectTypes.Description).filter(sq.ResourceTypes.ResourceTypeAcronym == selectedResourceType).\
    #         #         join(sq.ObjectTypes,
    #         #              sq.ObjectTypes.ResourceTypeID == sq.ResourceTypes.ResourceTypeID).\
    #         #         join(sq.ObjectCategories, sq.ObjectCategories.ObjectCategoryID == sq.ObjectTypes.ObjectCategoryID).all()
    #
    #         complete_result1 = list()
    #
    #         nameResult = list()
    #         for row in result:
    #             isExisting = False
    #             for name in nameResult:
    #                 if name == row.ObjectType:
    #                     isExisting = True
    #                     break
    #             if not isExisting:
    #                 nameResult.append(row.ObjectType)
    #                 complete_result1.append([row.ObjectType, row.ObjectTypologyCV, row.ResourceTypeAcronym,
    #                                         row.ObjectTypeCV, "", "",
    #                                         row.ObjectCategoryName, row.Description])
    #
    #         return complete_result1
    #     except Exception as e:
    #         # define.logger.error('Failed metAData load.\n' + e.message)
    #         raise Exception('Error occurred in reading Data Structure.\n' + e.message)
    def getAttributes(self, selectedResourceType = ''):
        '''
            This method is used to get Attributes by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''
        try:
            AttributeFields = ['ObjectType', 'AttributeName', 'AttributeUnit', 'AttributeDataTypeCV']
            complete_result = list()

            for UniqObjectAtt in self.unique_object_types_value_list:
                keys = UniqObjectAtt.keys()
                complete_result.append([UniqObjectAtt[keys[0]], UniqObjectAtt[keys[1]], UniqObjectAtt[keys[2]], UniqObjectAtt[keys[3]],# 'ObjectType', 'AttributeName', 'AttributeUnit', 'AttributeDataTypeCV'
                                        '', '', '', ''])

            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data StructureFromWeap.\n' + e.message)





