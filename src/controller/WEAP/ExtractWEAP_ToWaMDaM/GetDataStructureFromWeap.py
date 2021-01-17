
from collections import OrderedDict

from Extract_Network import Extract_Network


'''
    This class is used to get 
'''
class GetDataStructureFromWeap(object):
    def __init__(self, weap):
        self.WEAP = weap

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list, self.BranchesNew_list = Extract_Network(self.WEAP)

    # def getResourceTypes(self):

    ResourceTypes_List=[]
    ResourceTypesFields = ['ResourceType', 'ResourceTypeAcronym','ResourceTypeCV','MethodName','Description']

    ResourceTypes = OrderedDict()
    ResourceTypes['ResourceType'] = 'Water Evaluation And Planning'
    ResourceTypes['ResourceTypeAcronym'] = 'WEAP'
    ResourceTypes['ResourceTypeCV'] = 'WEAP'

    ResourceTypes['MethodName'] = 'Water Evaluation And Planning System'
    ResourceTypes['Description'] = 'WEAP (Water Evaluation And Planning" system) is a user-friendly software tool that takes an integrated approach to water resources planning."'

    ResourceTypes_List.append(ResourceTypes)




    # def getObjecttypes(self, selectedResourceType=''):

    ObjectTypeFields = ['ObjectType', 'ObjectTypology','ResourceTypeAcronym','ObjectTypeCV','Layout','ObjectCategory','Description']



    def getAttributes(self, selectedResourceType = ''):
        '''
            This method is used to get Attributes by selected ResourceTypeAcronym.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :return: list of set of data queried
        '''



        try:
            AttributeFields = ['ObjectType', 'AttributeName', 'AttributeName_Abstract','AttributeNameCV','AttributeUnit','AttributeUnitCV', 'AttributeDataTypeCV',
                               'AttributeCategory','ModelInputOrOutput','AttributeDescription','AttributeScale']
            complete_result = list()

            for UniqObjectAtt in self.unique_object_types_value_list:
                keys = UniqObjectAtt.keys()
                complete_result.append([UniqObjectAtt[keys[0]], UniqObjectAtt[keys[1]], UniqObjectAtt[keys[2]], UniqObjectAtt[keys[3]],# 'ObjectType', 'AttributeName', 'AttributeUnit', 'AttributeDataTypeCV'
                                        '', '', '', ''])

            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading getAttributes within StructureFromWeap.\n' + e.message)





