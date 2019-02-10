

from Extract_Network import Extract_Network

from collections import OrderedDict
'''
    This class is used to get result that query to get data of instances in sqlite db.
'''

class GetInstancesFromWeap(object):
    def __init__(self, weap):
        self.WEAP = weap

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list, self.BranchesNew_list = Extract_Network(self.WEAP)


    def getNodes(self, selectedResourceType='', masterNetworkName='', scenarioName=''):
        '''
            This method is used to get data of Nodes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried and InstanceName
        '''
        try:
            nameResult = list()
            dataResult = list()

            for nds in self.NodesSheetList:
                nameResult.append(nds['InstanceName'])
                dataResult.append([nds['ObjectType'], nds['InstanceName'],
                                        nds['InstanceNameCV'], nds['ScenarioName'],
                                         nds['SourceName'], nds['MethodName'],
                                        nds['InstanceCategory'], nds['Longitude_x'],
                                        nds['Latitude_y'], nds['Description']])

            return nameResult, dataResult
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data StructureFromWeap.\n' + e.message)

    def getLinkes(self, selectedResourceType='', masterNetworkName='', scenarioName=''):
        """
            This method is used to get data of Linkes by selected ResourceTypeAcronym, MasterNetworkName and ScenarioName.
            :param  selectedResourceType: value of selected ResourceTypeAcronym.
            :param  masterNetworkName: value of selected MasterNetworkName.
            :param  scenarioName: value of selected ScenarioName.
            :return: list of set of data queried
        """
        try:
            complete_result = list()

            for lks in self.LinksSheetList:
                complete_result.append([lks['ObjectType'], lks['InstanceName'],
                                        lks['InstanceNameCV'], lks['ScenarioName'],
                                        lks['SourceName'], lks['MethodName'],
                                        lks['StartNodeInstanceName'], lks['EndNodeInstanceName'],
                                        lks['InstanceCategory'], lks['Description']])
            return complete_result
        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading Data StructureFromWeap.\n' + e.message)