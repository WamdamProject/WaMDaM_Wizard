
# Extact the Network

from collections import OrderedDict
import pandas as pd

# Lists all transmission links, including the source and destination.
def Extract_Network(WEAP):

    LinksSheetList = []
    NodesSheetList = []
    Result_list = []
    TimeSeries_ExpressValue_list = []

    SourceName = WEAP.ActiveArea.Name
    for Branch in WEAP.Branches:
        BranchFullName=Branch.FullName



        if Branch.TypeName == 'River' and Branch.Isline:
            RiverNodeFullPath = Branch.FullName
            RiverNodeBranchName = Branch.Name
        if Branch.TypeName == 'River Reach' and Branch.Isline:
            Reach_ObjectType = Branch.TypeName

            # Extract the river name from the Reach full path
            import re

            LinkPath = Branch.FullName
            start = "River"
            end = 'Reaches'
            result = re.search('%s(.*)%s' % (start, end), LinkPath).group(1)
            # remove the '\' from the River Name
            newstr = result.replace("\\", "")
            RiverName = newstr
            #             print LinkPath
            #             m=Branch.Name
            GetReachNameFromPart = Branch.NodeAbove.Name
            GetReachNameToPart = Branch.NodeBelow.Name

            # If the reach upstream start node is a headflow then use the River Name
            if GetReachNameFromPart == '':  # or GetReachNameFromPart==RiverName:
                GetReachNameFromPart = RiverName + ' Headflow'

            if GetReachNameToPart == '':  # or GetReachNameFromPart==RiverName:
                GetReachNameToPart = RiverName + ' Mouth'

            #             print GetReachNameFromPart
            #             print GetReachNameToPart

            # Get the nodes
            startType = Branch.NodeAbove.TypeName
            startName = Branch.NodeAbove.Name
            startFullName = Branch.NodeAbove.FullName
            startLongitude_x = Branch.NodeAbove.x
            startLatitude_y = Branch.NodeAbove.y

            endType = Branch.NodeBelow.TypeName
            endName = Branch.NodeBelow.Name
            endFullName = Branch.NodeBelow.FullName
            endLongitude_x = Branch.NodeBelow.x
            endLatitude_y = Branch.NodeBelow.y

            if startType == 'N/A':
                startType = 'River Headflow'

            if startName == '':
                startName = RiverName + ' Headflow'
                TempBranchName = RiverNodeBranchName
            else:
                TempBranchName = Branch.Name

            if startType == 'Diversion Outflow':  # Swith the Full path from the Start Node Type itself to its River. We need that to get the River Attributes to this node
                startFullName = RiverNodeFullPath

            if endType == 'Diversion Outflow':  # Swith the Full path from the Start Node Type itself to its River. We need that to get the River Attributes to this node
                endFullName = RiverNodeFullPath

            if startFullName == '':
                startFullName = RiverNodeFullPath

            if startLongitude_x == 0.0:
                startLongitude_x = Branch.x

            if startLatitude_y == 0.0:
                startLatitude_y = Branch.y

            if endType == 'N/A':
                endType = 'River Mouth'

            if endName == '':
                endName = RiverName + ' Mouth'

            if endFullName == '':
                endFullName = RiverNodeFullPath + '\Mouth'  # not sure what to replace it with when it is empty. (but I dont think I need it anyway)

            if endLongitude_x == 0.0:
                endLongitude_x = Branch.x2

            if endLatitude_y == 0.0:
                endLatitude_y = Branch.y2

            Reach_LinkInstanceName = "%s from %s to %s" % (RiverName, GetReachNameFromPart, GetReachNameToPart)
            LinkBranch = Reach_LinkInstanceName

            #         print startName
            #         print startFullName

            LinksSheet = OrderedDict()

            LinksSheet['ObjectType'] = Reach_ObjectType
            LinksSheet['ObjectTypology'] = 'Link'

            if len(Reach_LinkInstanceName)>100:
                Reach_LinkInstanceName=Reach_LinkInstanceName[0:100] + "Trimed"

            LinksSheet['InstanceName'] = Reach_LinkInstanceName
            LinksSheet['BranchName'] = Branch.Name
            LinksSheet['FullBranchName'] = Branch.FullName
            LinksSheet['InstanceNameCV'] = ''
            LinksSheet['ScenarioName'] = "USU WEAP Model 2017"

            LinksSheet['SourceName'] = SourceName
            LinksSheet['MethodName'] = "Water Evaluation And Planning System"
            LinksSheet['StartNodeInstanceName'] = GetReachNameFromPart
            LinksSheet['EndNodeInstanceName'] = GetReachNameToPart
            LinksSheet['InstanceCategory'] = ''
            LinksSheet['Description'] = LinkPath

            LinksSheetList.append(LinksSheet)

            NodesSheet1 = OrderedDict()
            # Start
            NodesSheet1['ObjectType'] = startType
            NodesSheet1['ObjectTypology'] = 'Node'

            NodesSheet1['InstanceName'] = startName
            NodesSheet1['BranchName'] = TempBranchName
            NodesSheet1['FullBranchName'] = Branch.FullName

            NodesSheet1['InstanceNameCV'] = ''
            NodesSheet1['ScenarioName'] = "USU WEAP Model 2017"
            NodesSheet1['SourceName'] = SourceName
            NodesSheet1['MethodName'] = "Water Evaluation And Planning System"
            NodesSheet1['InstanceCategory'] = ''
            NodesSheet1['Longitude_x'] = startLongitude_x
            NodesSheet1['Latitude_y'] = startLatitude_y
            NodesSheet1['Description'] = startFullName

            NodesSheetList.append(NodesSheet1)

            # end
            NodesSheet2 = OrderedDict()
            NodesSheet2['ObjectType'] = endType
            NodesSheet2['ObjectTypology'] = 'Node'

            NodesSheet2['InstanceName'] = endName
            NodesSheet2['BranchName'] = Branch.Name
            NodesSheet2['FullBranchName'] = Branch.FullName
            NodesSheet2['InstanceNameCV'] = ''
            NodesSheet2['ScenarioName'] = "USU WEAP Model 2017"
            NodesSheet2['SourceName'] = SourceName
            NodesSheet2['MethodName'] = "Water Evaluation And Planning System"
            NodesSheet2['InstanceCategory'] = ''
            NodesSheet2['Longitude_x'] = endLongitude_x
            NodesSheet2['Latitude_y'] = endLatitude_y
            NodesSheet2['Description'] = endFullName

            NodesSheetList.append(NodesSheet2)

        if Branch.Isline and (
                Branch.TypeName == 'Transmission Link' or Branch.TypeName == 'Return Flow' or Branch.TypeName == 'Runoff and Infiltration'):
            RiverNodeFullPath = Branch.FullName
            Link = Branch.TypeName
            GetReachNameFromPart = Branch.NodeAbove.Name
            GetReachNameToPart = Branch.NodeBelow.Name  # print Reach_LinkInstanceName

            Reach_LinkInstanceName = "%s from %s to %s" % (Link, GetReachNameFromPart, GetReachNameToPart)
            #         print Link
            LinksSheet = OrderedDict()

            LinksSheet['ObjectType'] = Link
            LinksSheet['ObjectTypology'] = 'Link'
            if len(Reach_LinkInstanceName)>100:
                Reach_LinkInstanceName=Reach_LinkInstanceName[0:100] + "Trimed"

            LinksSheet['InstanceName'] = Reach_LinkInstanceName
            LinksSheet['BranchName'] = Branch.Name
            LinksSheet['FullBranchName'] = Branch.FullName

            LinksSheet['InstanceNameCV'] = ''
            LinksSheet['ScenarioName'] = "USU WEAP Model 2017"
            LinksSheet['SourceName'] = SourceName
            LinksSheet['MethodName'] = "Water Evaluation And Planning System"
            LinksSheet['StartNodeInstanceName'] = GetReachNameFromPart
            LinksSheet['EndNodeInstanceName'] = GetReachNameToPart
            LinksSheet['InstanceCategory'] = ''
            LinksSheet['Description'] = RiverNodeFullPath

            LinksSheetList.append(LinksSheet)
            #         print LinksSheet

            LinkBranch = Reach_LinkInstanceName

        # this is a node, it should get me the Diversion outflow (for the Diversion attributes)
        # ######################################################################################################

        if Branch.TypeName == 'Diversion' and Branch.Isline:
            startName = Branch.Name + ' Outflow'
            startFullName = Branch.FullName
            startType = Branch.NodeAbove.TypeName
            startLongitude_x = Branch.NodeAbove.x
            startLatitude_y = Branch.NodeAbove.y
            #         print startName
            #         print startType

            NodesSheet1 = OrderedDict()
            # Start
            NodesSheet1['ObjectType'] = startType
            NodesSheet1['ObjectTypology'] = 'Node'

            NodesSheet1['InstanceName'] = startName
            NodesSheet1['BranchName'] = Branch.Name
            NodesSheet1['FullBranchName'] = Branch.FullName


            #         print startType
            #         print Branch.Name
            #         print startName
            NodesSheet1['InstanceNameCV'] = ''
            NodesSheet1['ScenarioName'] = "USU WEAP Model 2017"
            NodesSheet1['SourceName'] = SourceName
            NodesSheet1['MethodName'] = "Water Evaluation And Planning System"
            NodesSheet1['InstanceCategory'] = ''
            NodesSheet1['Longitude_x'] = startLongitude_x
            NodesSheet1['Latitude_y'] = startLatitude_y
            NodesSheet1['Description'] = startFullName

            NodesSheetList.append(NodesSheet1)

        # Get all the nodes (Reservoir, Demand Site, Catchement)

        if Branch.IsNode:
            startName = Branch.Name
            startFullName = Branch.FullName
            startType = Branch.TypeName
            startLongitude_x = Branch.x
            startLatitude_y = Branch.y

            NodesSheet1 = OrderedDict()
            NodesSheet1['ObjectType'] = startType
            NodesSheet1['ObjectTypology'] = 'Node'

            NodesSheet1['InstanceName'] = startName
            NodesSheet1['BranchName'] = Branch.Name
            NodesSheet1['FullBranchName'] = Branch.FullName

            NodesSheet1['InstanceNameCV'] = ''
            NodesSheet1['ScenarioName'] = "USU WEAP Model 2017"
            NodesSheet1['SourceName'] = SourceName
            NodesSheet1['MethodName'] = "Water Evaluation And Planning System"
            NodesSheet1['InstanceCategory'] = ''
            NodesSheet1['Longitude_x'] = startLongitude_x
            NodesSheet1['Latitude_y'] = startLatitude_y
            NodesSheet1['Description'] = startFullName

            NodesSheetList.append(NodesSheet1)

# print 'done'

# view=pd.DataFrame(NodesSheetList)

# view2=pd.DataFrame(LinksSheetList)

# view2.to_csv('LinksSheetList.csv', sep=',')


# combine the node and link instances to pass them to get variables

# Get unique Branches based on the field InstanceName

    BranchesNew_list = []

    temp_instancename_list = []
    unique_object_types_value_list = []
    unique_branch_name_value_list = []

    for nodeSheet in NodesSheetList:
        if not nodeSheet['InstanceName'] in temp_instancename_list:
            temp_instancename_list.append(nodeSheet['InstanceName'])

            BranchesNew = OrderedDict()
            BranchesNew['ObjectType'] = nodeSheet['ObjectType']
            BranchesNew['ObjectTypology'] = nodeSheet['ObjectTypology']

            BranchesNew['BranchName'] = nodeSheet['BranchName']
            BranchesNew['FullBranchName'] = nodeSheet['FullBranchName']

            BranchesNew['InstanceName'] = nodeSheet['InstanceName']

            BranchesNew_list.append(BranchesNew)

        #         if not nodeSheet['BranchName'] in unique_branch_name_value_list:
        #             unique_branch_name_value_list.append(nodeSheet['BranchName'])
        if not nodeSheet['ObjectType'] in unique_object_types_value_list:
            unique_object_types_value_list.append(nodeSheet['ObjectType'])

    for linksSheet in LinksSheetList:
        if not linksSheet['InstanceName'] in temp_instancename_list:
            temp_instancename_list.append(linksSheet['InstanceName'])

            BranchesNew = OrderedDict()
            BranchesNew['ObjectType'] = linksSheet['ObjectType']
            BranchesNew['ObjectTypology'] = linksSheet['ObjectTypology']

            BranchesNew['BranchName'] = linksSheet['BranchName']
            BranchesNew['FullBranchName'] = linksSheet['FullBranchName']



            BranchesNew['InstanceName'] = linksSheet['InstanceName']

            BranchesNew_list.append(BranchesNew)

        #         if not linksSheet['BranchNa me'] in unique_branch_name_value_list:
        #             unique_branch_name_value_list.append(linksSheet['BranchName'])
        if not linksSheet['ObjectType'] in unique_object_types_value_list:
            unique_object_types_value_list.append(linksSheet['ObjectType'])

    # print BranchesNew_list

    # make BranchesNew_list as a data frame just to view it and  see how its columns and rrows

    view = pd.DataFrame(BranchesNew_list)
    # print BranchesNew_list

    # view.to_csv('this.csv', sep=',')

    return (NodesSheetList,LinksSheetList,unique_object_types_value_list, BranchesNew_list)

