
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq

'''
    This class is used to compare any two scenarios within a MasterNetwork in a selected database file.
'''
class GetComapreScenarios(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
        self.excel_pointer = None

    def GetComapreScenarios(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to compare any two scenarios within a MasterNetwork in a selected database file and make ScenarioComparision table.
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: None
        '''

        # Get ids of selected scenarios.
        result1 = self.session.query(sq.Scenarios.ScenarioID).filter(sq.Scenarios.ScenarioName == scenarioName1).all()
        scenarioID1 = None
        scenarioID2 = None
        if result1.__len__() > 0:
            scenarioID1 = result1[0][0]
        else:
            return

        result2 = self.session.query(sq.Scenarios.ScenarioID).filter(sq.Scenarios.ScenarioName == scenarioName2).all()
        if result2.__len__() > 0:
            scenarioID2 = result2[0][0]
        else:
            return

        # Make SQL command to write data within ScenarioComparision table.
        CompareScenarioSql = 'SELECT "MappingID1ScenarioID1"."MappingID" As MappingID1,"MappingID1ScenarioID1"."ScenarioID" As ScenarioID1,' \
                                       'CAST(NULL AS INTEGER) As MappingID2, CAST(NULL AS INTEGER) As ScenarioID2 ' \
                                'FROM "MappingID1ScenarioID1" ' \
                                'WHERE NOT EXISTS (' \
                                    'SELECT * ' \
                                'FROM "MappingID1ScenarioID2" ' \
                                'WHERE "MappingID1ScenarioID1"."MappingID"="MappingID1ScenarioID2"."MappingID" ) ' \
                                'UNION ALL ' \
                                'SELECT        CAST(NULL AS INTEGER) As MappingID2, CAST(NULL AS INTEGER) As ScenarioID2,' \
                                    '"MappingID1ScenarioID2"."MappingID","MappingID1ScenarioID2"."ScenarioID" ' \
                                'FROM "MappingID1ScenarioID2" ' \
                                'WHERE NOT EXISTS ( ' \
                                    'SELECT * ' \
                                'FROM "MappingID1ScenarioID1" ' \
                                'WHERE "MappingID1ScenarioID1"."MappingID"="MappingID1ScenarioID2"."MappingID" )'
        # Drop those if existing MappingID1ScenarioID1 and MappingID1ScenarioID2 that are temp tables and create those tables.
        self.session.execute('DROP TABLE IF EXISTS MappingID1ScenarioID1')
        self.session.execute('DROP TABLE IF EXISTS MappingID1ScenarioID2')
        self.session.execute('CREATE Table MappingID1ScenarioID1 AS SELECT ScenarioID,MappingID FROM "ScenarioMappings" WHERE "ScenarioID"="{}";'.format(str(scenarioID1)))
        self.session.execute('CREATE Table MappingID1ScenarioID2 AS SELECT ScenarioID,MappingID FROM "ScenarioMappings" WHERE "ScenarioID"="{}";'.format(str(scenarioID2)))
        result = self.session.execute(CompareScenarioSql)

        # Create those if don't exist ScenarioComparision
        self.session.execute('CREATE TABLE IF NOT EXISTS ScenarioComparision(' \
                                'ID INTEGER PRIMARY KEY AUTOINCREMENT,' \
                                'MappingID1 VARCHAR (10),' \
                                'ScenarioID1  VARCHAR (10),' \
                                'MappingID2  VARCHAR (10),' \
                                'ScenarioID2   VARCHAR (10),' \
                                'ReferenceScenarioID  INT NOT NULL,' \
                                'OtherScenarioID   INT NOT NULL' \
                                ');')
        self.session.execute('DELETE FROM "ScenarioComparision" WHERE ReferenceScenarioID={} AND OtherScenarioID={};'.format(scenarioID1, scenarioID2))

        i = 0
        # recordCountResult = self.session.execute('SELECT COUNT(*) FROM ScenarioComparision;')
        # for n in recordCountResult:
        #     i = int(n[0])
        # i += 1
        for row in result:
            recordCountResult = self.session.execute('SELECT COUNT(*) FROM ScenarioComparision;')
            for n in recordCountResult:
                i = int(n[0])
            i += 1
            insertStr = "INSERT INTO ScenarioComparision ( MappingID1, ScenarioID1, MappingID2, ScenarioID2, ReferenceScenarioID, OtherScenarioID) " \
                        "VALUES ( '{}', '{}', '{}', '{}', {}, {});".format( row[0] if row[0] != None else " ",
                                                                  row[1] if row[1] != None else " ",
                                                                  row[2] if row[2] != None else " ",
                                                                  row[3] if row[3] != None else " ", scenarioID1, scenarioID2)
            self.session.execute(insertStr)

            pass
        return []

    def GetUniqueTopology_Scenario2(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to get data making UniqueToFirstScenario table within ChangeInTopology sheet
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: queried result(list)
        '''

        sql = 'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType","ObjectTypologyCV","ScenarioName",' \
                '"MasterNetworkName"' \
                'FROM "ScenarioComparision"' \
                'JOIN "Mappings"' \
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID2"' \
                'JOIN "ScenarioMappings"' \
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID2"' \
                'JOIN "Scenarios"' \
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"' \
                'Left JOIN "MasterNetworks"' \
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"' \
                'Left JOIN "Attributes"' \
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID"' \
                'Left JOIN  "ObjectTypes"' \
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID"' \
                'Left JOIN "ResourceTypes"' \
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID"' \
                'JOIN "Instances"' \
                'ON "Instances"."InstanceID"="Mappings"."InstanceID"'\
                'WHERE "Attributes"."AttributeName"="ObjectTypeInstances" ' \
                      'AND "ResourceTypes"."ResourceTypeAcronym"="{}" ' \
                      'AND "MasterNetworks"."MasterNetworkName"="{}" '.format(selectedDataset, masterNetworkName)


        result = self.session.execute(sql)
        resultData = []
        for row in result:
            if row.ScenarioName == scenarioName1:
                continue
            resultData.append([row.InstanceName, row.ObjectType, row.ObjectTypologyCV])
            pass
        return resultData

    def GetUniqueTopology_Scenario1(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to get data making UniqueToSecondScenario table within ChangeInTopology sheet
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: queried result(list)
        '''

        sql = 'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType",ObjectTypologyCV,"ScenarioName",' \
                '"MasterNetworkName"' \
                'FROM "ScenarioComparision"' \
                'JOIN "Mappings"' \
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID1"' \
                'JOIN "ScenarioMappings"' \
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID1"' \
                'JOIN "Scenarios"'\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"' \
                'Left JOIN "MasterNetworks"' \
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"' \
                'Left JOIN "Attributes"' \
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID"' \
                'Left JOIN  "ObjectTypes"' \
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID"' \
                'Left JOIN "ResourceTypes"' \
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID"'\
                'JOIN "Instances"' \
                'ON "Instances"."InstanceID"="Mappings"."InstanceID"' \
                'WHERE "Attributes"."AttributeName"="ObjectTypeInstances" AND ObjectTypologyCV !="Network" '\
                      'AND "ResourceTypes"."ResourceTypeAcronym"="{}" ' \
                      'AND "MasterNetworks"."MasterNetworkName"="{}" ' \
              'ORDER BY "ScenarioName" desc '.format(selectedDataset, masterNetworkName)


        result = self.session.execute(sql)
        resultData = []
        for row in result:
            if row.ScenarioName == scenarioName2:
                continue
            resultData.append([row.InstanceName, row.ObjectType, row.ObjectTypologyCV])
            pass
        return resultData

    def GetCommonTopology(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to get data making CommonBetweenThem table within ChangeInTopology sheet
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: queried result(list)
        '''
        sql = 'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType",ObjectTypologyCV ' \
                'FROM "ResourceTypes"' \
                'left join "ObjectTypes"' \
                'ON ObjectTypes.ResourceTypeID=ResourceTypes.ResourceTypeID ' \
                'Left JOIN "Attributes"' \
                'ON Attributes.ObjectTypeid = Objecttypes.Objecttypeid ' \
                'Left JOIN "Mappings"'\
                'ON Mappings.Attributeid = Attributes.Attributeid ' \
                'Left JOIN "Instances"' \
                'ON instances.instanceid = Mappings.Instanceid ' \
                'Left JOIN "ScenarioMappings"' \
                'ON ScenarioMappings.Mappingid = Mappings.Mappingid ' \
                'Left JOIN  "Scenarios"' \
                'ON Scenarios.ScenarioId=ScenarioMappings.Scenarioid ' \
                'Left JOIN "MasterNetworks"' \
                'ON MasterNetworks.MasterNetworkid = Scenarios.MasterNetworkid '\
                'Left JOIN "Methods"' \
                'ON Methods.Methodid = Mappings.Methodid ' \
                'Left JOIN Sources on Sources.Sourceid = Mappings.Sourceid '\
                'WHERE "Attributes"."AttributeName"="ObjectTypeInstances" AND ObjectTypologyCV !="Network" and InstanceName IS NOT NULL '\
                      'AND "ResourceTypes"."ResourceTypeAcronym"="{}" ' \
                      'AND "MasterNetworks"."MasterNetworkName"="{}" '\
                      ' ORDER BY "InstanceName" desc '.format(selectedDataset, masterNetworkName)

        result = self.session.execute(sql)
        resultData = []
        for row in result:
            isExist = False
            for item in resultData:
                if item[0] == row.InstanceName and item[1] == row.ObjectType and item[2] == row.ObjectTypologyCV:
                    isExist = True
                    break
            if not isExist:
                resultData.append([row.InstanceName, row.ObjectType, row.ObjectTypologyCV])

        return resultData

    def GetChangeInMetadata_Topology(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to get data making table within ChangeInMetadata_Topology sheet
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: queried result(list)
        '''
        sqlDrop = 'DROP TABLE IF EXISTS ChangeInMetadata_Topology;'
        sql = 'CREATE Table ChangeInMetadata_Topology AS ' \
                'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType","ObjectTypologyCV",' \
                'AttributeName,"ScenarioName",SourceName,MethodName,"MasterNetworkName",ValuesMapperID '\
                'FROM "ScenarioComparision" '\
                'JOIN "Mappings" '\
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID2" '\
                'JOIN "ScenarioMappings" '\
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID2" '\
                'JOIN "Scenarios" '\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
                'Left JOIN "MasterNetworks" '\
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
                'Left JOIN "Attributes" '\
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID" '\
                'Left JOIN  "ObjectTypes" '\
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID" '\
                'Left JOIN "ResourceTypes" '\
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID" '\
                'JOIN "Instances" '\
                'ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
                'Left JOIN "Methods" '\
                'ON "Methods"."MethodID"="Mappings"."MethodID" '\
                'Left JOIN "Sources" '\
                'ON "Sources"."SourceID"="Mappings"."SourceID" '\
                'WHERE "Attributes"."AttributeName"="ObjectTypeInstances" AND "MasterNetworks"."MasterNetworkName"="{}" AND ResourceTypeAcronym="{}" '\
                'UNION ALL '\
                'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType","ObjectTypologyCV",AttributeName,ScenarioName,SourceName,MethodName,"MasterNetworkName",ValuesMapperID '\
                'FROM "ScenarioComparision" '\
                'JOIN "Mappings" '\
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID1" '\
                'JOIN "ScenarioMappings" '\
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID1" '\
                'JOIN "Scenarios" '\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
                'Left JOIN "Attributes" '\
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID" '\
                'Left JOIN  "ObjectTypes" '\
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID" '\
                'Left JOIN "ResourceTypes" '\
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID" '\
                'Left JOIN "MasterNetworks" '\
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
                'JOIN "Instances" '\
                'ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
                'Left JOIN "Methods" '\
                'ON "Methods"."MethodID"="Mappings"."MethodID" '\
                'Left JOIN "Sources" '\
                'ON "Sources"."SourceID"="Mappings"."SourceID" '\
                'WHERE "Attributes"."AttributeName"="ObjectTypeInstances" AND "MasterNetworks"."MasterNetworkName"="{}" AND ResourceTypeAcronym="{}" '\
                'ORDER BY "ScenarioName" desc '.format(masterNetworkName, selectedDataset, masterNetworkName, selectedDataset)

        self.session.execute(sqlDrop)
        result = self.session.execute(sql)
        result = self.session.execute("SELECT * FROM ChangeInMetadata_Topology;")
        resultData = []
        for row in result:
            resultData.append([row.InstanceName, row.ObjectType, row.ObjectTypologyCV, row.AttributeName, row.ScenarioName, row.SourceName, row.MethodName, row.MasterNetworkName, row.ValuesMapperID])
            pass
        return resultData


    def GetChangeInMetaValues_Attributes(self, selectedDataset, masterNetworkName, scenarioName1, scenarioName2):
        '''
        This method is used to get data making table within ChangeInMetadata_Attributes sheet
        :param selectedDataset: value of selected ResourceTypeAcronym.
        :param masterNetworkName: value of selected MasterNetworkName.
        :param scenarioName1: first scenario name
        :param scenarioName2: second scenario name
        :return: queried result(list)
        '''
        sqlDrop = 'DROP TABLE IF EXISTS ChangeInMetavalues_Attributes; '
        sql = 'CREATE Table ChangeInMetavalues_Attributes AS '\
                'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType","ObjectTypologyCV",AttributeName,AttributeDataTypeCV,"ScenarioName",SourceName,MethodName,"MasterNetworkName",ValuesMapperID '\
                'FROM "ScenarioComparision" '\
                'JOIN "Mappings" '\
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID2" '\
                'JOIN "ScenarioMappings" '\
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID2" '\
                'JOIN "Scenarios" '\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
                'Left JOIN "MasterNetworks"  '\
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
                'Left JOIN "Attributes" '\
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID" '\
                'Left JOIN  "ObjectTypes" '\
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID" '\
                'Left JOIN "ResourceTypes" '\
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID" '\
                'JOIN "Instances" '\
                'ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
                'Left JOIN "Methods"  '\
                'ON "Methods"."MethodID"="Mappings"."MethodID" '\
                'Left JOIN "Sources"  '\
                'ON "Sources"."SourceID"="Mappings"."SourceID" '\
                'WHERE "Attributes"."AttributeName"!="ObjectTypeInstances" AND "MasterNetworks"."MasterNetworkName"="{}" AND ResourceTypeAcronym="{}"  '\
                'UNION ALL '\
                'SELECT  DISTINCT  "Instances"."InstanceName","ObjectType","ObjectTypologyCV",AttributeName,AttributeDataTypeCV, ScenarioName,SourceName,MethodName,"MasterNetworkName",ValuesMapperID '\
                'FROM "ScenarioComparision" '\
                'JOIN "Mappings" '\
                'ON "Mappings"."MappingID"="ScenarioComparision"."MappingID1" '\
                'JOIN "ScenarioMappings" '\
                'ON "ScenarioMappings"."MappingID"="ScenarioComparision"."MappingID1" '\
                'JOIN "Scenarios" '\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
                'Left JOIN "Attributes" '\
                'ON "Attributes"."AttributeID"="Mappings"."AttributeID" '\
                'Left JOIN  "ObjectTypes" '\
                'ON "ObjectTypes"."ObjectTypeID"="Attributes"."ObjectTypeID" '\
                'Left JOIN "ResourceTypes" '\
                'ON "ResourceTypes"."ResourceTypeID"="ObjectTypes"."ResourceTypeID" '\
                'Left JOIN "MasterNetworks"  '\
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
                'JOIN "Instances" '\
                'ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
                'Left JOIN "Methods"  '\
                'ON "Methods"."MethodID"="Mappings"."MethodID" '\
                'Left JOIN "Sources"  '\
                'ON "Sources"."SourceID"="Mappings"."SourceID" '\
                'WHERE "Attributes"."AttributeName"!="ObjectTypeInstances" AND "MasterNetworks"."MasterNetworkName"="{}" AND ResourceTypeAcronym="{}"  '\
                'ORDER BY "ScenarioName" desc '.format(masterNetworkName, selectedDataset, masterNetworkName, selectedDataset)

        self.session.execute(sqlDrop)
        result = self.session.execute(sql)
        result = self.session.execute("SELECT * FROM ChangeInMetavalues_Attributes;")
        resultData = []
        for row in result:
            resultData.append([row.InstanceName, row.ObjectType, row.ObjectTypologyCV, row.AttributeName, row.AttributeDataTypeCV, row.ScenarioName, row.SourceName, row.MethodName, row.MasterNetworkName, row.ValuesMapperID])
            pass
        return resultData

    def AllValuesMapperCount(self, selectedDataset, masterNetworkName):
        sql = 'SELECT count(ValuesMapper.ValuesMapperID) AS AllValuesMapperCount '\
                'FROM ResourceTypes '\
                'Left JOIN "ObjectTypes" '\
                'ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
                'Left JOIN "Attributes"'\
                'ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
                'Left JOIN "Mappings" '\
                'ON Mappings.AttributeID= Attributes.AttributeID '\
                'Left JOIN "Instances" '\
                'ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
                'Left JOIN "ScenarioMappings" '\
                'ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" '\
                'Left JOIN "Scenarios" '\
                'ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
                'Left JOIN "MasterNetworks" '\
                'ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
                'Left JOIN "ValuesMapper" ' \
                'ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
                'WHERE InstanceName is not null and MasterNetworkName="{}"' \
                ' and AttributeName!="ObjectTypeInstances"'.format(masterNetworkName)
        result = self.session.execute(sql)
        for row in result:
            return row.AllValuesMapperCount
        return 0
    def AllTopologyMetadataCount(self, selectedDataset, masterNetworkName):
        sql = 'SELECT  count(InstanceName) AS AllTopologyMetadataCount ' \
              'FROM ResourceTypes Left JOIN "ObjectTypes" ' \
              'ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" ' \
              'Left JOIN  "Attributes" ' \
              'ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" ' \
              'Left JOIN "Mappings" ON Mappings.AttributeID= Attributes.AttributeID ' \
              'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" ' \
              'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" ' \
              'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" ' \
              'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
              'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" ' \
              'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" ' \
              'WHERE AttributeName="ObjectTypeInstances" and InstanceName is not null and ' \
              'MasterNetworkName="{}"'.format(masterNetworkName)
        result = self.session.execute(sql)
        for row in result:
            return row.AllTopologyMetadataCount
        return 0

    def AllMetadataAttributesCount(self , selectedDataset, masterNetworkName):
        sql = 'SELECT  count(InstanceName) AS AllMetadataAttributesCount FROM ResourceTypes ' \
              'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" ' \
              'Left JOIN  "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" ' \
              'Left JOIN "Mappings" ON Mappings.AttributeID= Attributes.AttributeID ' \
              'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" ' \
              'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" ' \
              'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" ' \
              'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
              'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" ' \
              'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" ' \
              'WHERE AttributeName!="ObjectTypeInstances" and InstanceName is not null and ' \
              'MasterNetworkName="{}"'.format(masterNetworkName)
        result = self.session.execute(sql)
        for row in result:
            return row.AllMetadataAttributesCount
        return 0