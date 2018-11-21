

from Extract_Network import Extract_Network

from collections import OrderedDict
'''
    This class is used to get result that query to get data of instances in sqlite db.
'''

class GetInstancesFromWeap(object):
    def __init__(self, weap):
        self.WEAP = weap

        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list, self.BranchesNew_list = Extract_Network(self.WEAP)

    # def getMasterNetwork(self, selectedResourceType=''):
    #     '''
    #         This method is used to get data from MasterNetworks table by selected ResourceTypeAcronym.
    #         :param  selectedResourceType: value of selected ResourceTypeAcronym.
    #         :return: list of MasterNetworkName and set of data queried
    #     '''
    #     try:
    #         if selectedResourceType == '':
    #             # get all data
    #             result = self.session.execute("Select ResourceTypeAcronym,MasterNetworkName, SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description' "\
    #                                             "FROM ResourceTypes "\
    #                                             "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
    #                                             "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
    #                                             "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
    #                                             "left join Instances on instances.instanceid = Mappings.Instanceid "\
    #                                             "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
    #                                             "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
    #                                             "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
    #                                             "WHERE ObjectTypologyCV='Network' ")
    #         else:
    #             result = self.session.execute("Select ResourceTypeAcronym,MasterNetworkName, SpatialReferenceNameCV, VerticalDatumCV,'MasterNetworks'.'Description' "\
    #                                             "FROM ResourceTypes "\
    #                                             "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
    #                                             "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
    #                                             "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
    #                                             "left join Instances on instances.instanceid = Mappings.Instanceid "\
    #                                             "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
    #                                             "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
    #                                             "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
    #                                             "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network' ".format(selectedResourceType))
    #         #Get data the remaining data except overlapping MasterNetworkName.
    #         nameResult = list()
    #         dataResult = list()
    #         for row in result:
    #             if row.MasterNetworkName == None:
    #                 continue
    #             isExisting = False
    #             for name in nameResult:
    #                 if name == row.MasterNetworkName:
    #                     isExisting = True
    #                     break
    #             if not isExisting:
    #                 nameResult.append(row.MasterNetworkName)
    #                 dataResult.append([row.MasterNetworkName, row.ResourceTypeAcronym,
    #                                   row.SpatialReferenceNameCV, row.VerticalDatumCV,
    #                                   row.Description])
    #
    #
    #         return nameResult, dataResult
    #     except Exception as e:
    #         # define.logger.error('Failed metAData load.\n' + e.message)
    #         raise Exception('Error occurred in reading Data Structure.\n' + e.message)
    #
    # def getScenario(self, selectedResourceType='', masterNetworkName=''):
    #     '''
    #         This method is used to get data from Scenarios table by selected ResourceTypeAcronym and MasterNetworkName.
    #         :param  selectedResourceType: value of selected ResourceTypeAcronym.
    #         :param  masterNetworkName: value of selected MasterNetworkName.
    #         :return: list of ScenarioName and set of data queried
    #     '''
    #     try:
    #         if selectedResourceType == '' and masterNetworkName == '':
    #             sql_command = "Select ResourceTypeAcronym,ObjectType,ObjectTypologyCV,AttributeName,InstanceName,MasterNetworkName,ScenarioName, "\
    #                                       "ScenarioEndDate,Sourcename, TimeStepValue, TimeStepUnitCV, 'Scenarios'.'Description', Methodname ,ScenarioStartDate "\
    #                                         "FROM ResourceTypes "\
    #                                         "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
    #                                         "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
    #                                         "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
    #                                         "left join Instances on instances.instanceid = Mappings.Instanceid "\
    #                                         "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
    #                                         "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
    #                                         "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
    #                                         "left join Methods on Methods.Methodid = Mappings.Methodid "\
    #                                         "left join Sources on Sources.Sourceid = Mappings.Sourceid  "\
    #                                         "WHERE ObjectTypologyCV='Network'"
    #         else:
    #             sql_command = "Select ResourceTypeAcronym,ObjectType,ObjectTypologyCV,AttributeName,InstanceName,MasterNetworkName,ScenarioName, "\
    #                                           "ScenarioEndDate,Sourcename, TimeStepValue, TimeStepUnitCV, 'Scenarios'.'Description', Methodname ,ScenarioStartDate "\
    #                                             "FROM ResourceTypes "\
    #                                             "left join ObjectTypes on ObjectTypes.ResourceTypeid=ResourceTypes.ResourceTypeid  "\
    #                                             "left join Attributes on Attributes.ObjectTypeid = Objecttypes.Objecttypeid "\
    #                                             "left join Mappings on Mappings.Attributeid = Attributes.Attributeid  "\
    #                                             "left join Instances on instances.instanceid = Mappings.Instanceid "\
    #                                             "left join Scenariomappings on ScenarioMappings.Mappingid = Mappings.Mappingid "\
    #                                             "left join Scenarios on Scenarios.ScenarioId=ScenarioMappings.Scenarioid  "\
    #                                             "left join MasterNetworks on MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid  "\
    #                                             "left join Methods on Methods.Methodid = Mappings.Methodid "\
    #                                             "left join Sources on Sources.Sourceid = Mappings.Sourceid  "\
    #                                             "WHERE ResourceTypeAcronym='{}' AND ObjectTypologyCV='Network' AND MasterNetworkName='{}'"\
    #                                             "ORDER BY InstanceName DESC".format(selectedResourceType, masterNetworkName)
    #         result = self.session.execute(sql_command)
    #         #Get data the remaining data except overlapping ScenarioName.
    #         nameResult = list()
    #         dataResult = list()
    #         for row in result:
    #             if row.ScenarioName == None:
    #                 continue
    #             isExisting = False
    #             for name in nameResult:
    #                 if name == row.ScenarioName:
    #                     isExisting = True
    #                     break
    #             if not isExisting:
    #                 nameResult.append(row.ScenarioName)
    #                 dataResult.append([row.ScenarioName, row.MasterNetworkName,
    #                                    row.SourceName, row.MethodName,
    #                                    row.ScenarioStartDate, row.ScenarioEndDate,
    #                                    row.TimeStepValue, row.TimeStepUnitCV,
    #                                    row.Description])
    #
    #         return nameResult, dataResult
    #     except Exception as e:
    #         # define.logger.error('Failed metAData load.\n' + e.message)
    #         raise Exception('Error occurred in reading Data StructureFromWeap.\n' + e.message)

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