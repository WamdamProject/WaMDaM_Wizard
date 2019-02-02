

def GetValues_WEAP(WEAP,BranchesNew_list, unique_object_types_value_list):

    from collections import OrderedDict

    Result_list = []
    UniqObjectAtt_list_all= []
    Global_Result_List = []
    GlobalAttributes_List = []

    # TimeSeries_ExpressValue_list = []
    # print unique_object_types_value_list
    # unique_object_types_value_list = ['Reservoir']
    # unique_object_types_value_list = ['Demand Site']
    # unique_object_types_value_list = ['Transmission Link']
    # unique_object_types_value_list = ['Streamflow Gauge']
    # unique_object_types_value_list = ['River Headflow']

    # unique_object_types_value_list = ['River Headflow','Reservoir']
    # unique_object_types_value_list = ['Streamflow Gauge','Reservoir','River Reach','Groundwater']
    # unique_object_types_value_list = ['Streamflow Gauge','River Reach']

    # unique_object_types_value_list = ['Run of River Hydro','Wastewater Treatment Plant']

    # print unique_object_types_value

    # unique_object_types_value_list_shortend= not in 'River Headflow','Return Flow Node','River Withdrawal','Tributary Inflow','River Mouth','Diversion Outflow')



    # these WEAP Object Types have no input variables. They are just used as connections in the network
    exclude_object_type_list = ['Return Flow Node', 'River Withdrawal', 'Tributary Inflow', 'River Mouth']
    # loop over all the WEAP branches to get their variables and values
    atrr_names = {}
    for Branch in WEAP.Branches:
        # Dynamicly get the global attributes under the Key Assumptions branch in WEAP
        BranchFullName = Branch.FullName
        BranchName = Branch.Name

        if 'Key\\' in BranchFullName:
            GlobalAttribute = BranchFullName.split("Key\\")[1]

            GlobalAttributes = OrderedDict()
            GlobalAttributes['ObjectType'] = 'WEAP Global Attributes'
            GlobalAttributes['AttributeName'] = GlobalAttribute

            for V in Branch.Variables:
                ExpresValue = V.Expression
                AttributeUnit = V.ScaleUnitText
                if AttributeUnit == '':
                    AttributeUnit = '-'
                GlobalAttributes['AttributeUnit'] = AttributeUnit
                if 'ReadFromFile' in ExpresValue:
                    GlobalAttributes['AttributeDataTypeCV'] = 'TimeSeries'
                elif 'MonthlyValues' in ExpresValue:
                    GlobalAttributes['AttributeDataTypeCV'] = 'SeasonalNumericValues'
                else:
                    # Numeirc if the value is a float (single value) e.g., "0", "100" etc
                    try:
                        if ExpresValue == '':
                            Numeric_ExpressValue = ''
                        #                                         print Numeric_ExpressValue
                        else:
                            if '.' in ExpresValue:
                                numeric_val = float(ExpresValue)
                            else:
                                numeric_val = int(ExpresValue)
                            Numeric_ExpressValue = ExpresValue

                            GlobalAttributes['AttributeDataTypeCV'] = 'NumericValues'
                    #                                         print Numeric_ExpressValue
                    # Other if the value other than the above (example: "Storage Capacity[AF]")

                    except:
                        FreeText_ExpressValue = ExpresValue

                        GlobalAttributes['AttributeDataTypeCV'] = 'FreeText'

                GlobalAttributes_List.append(GlobalAttributes)


                Global_Result = OrderedDict()
                Global_Result['FullBranch'] = BranchFullName
                Global_Result['BranchType'] = 'WEAP Global Attributes'
                Global_Result['Attribute']=GlobalAttribute
                Global_Result['InstanceName'] = ''
                Global_Result['ExpresValueType'] = GlobalAttributes['AttributeDataTypeCV']
                Global_Result['ExpresValue'] = ExpresValue
                Global_Result['BranchName'] = BranchName  # use it later for verification reasons
                Global_Result_List.append(Global_Result)

            #print Global_Result_List


        for unique_object_types_value in unique_object_types_value_list:
            if unique_object_types_value in exclude_object_type_list:
                continue
            #         print unique_object_types_value_list
            if unique_object_types_value == 'River Headflow':  # if the unique_object_types_value here comes as 'River Headflow', change it to 'River'
                unique_object_types_value = 'River'

            if unique_object_types_value == 'Diversion Outflow':  # if the unique_object_types_value here comes as 'Diversion Outflow', change it to 'Diversion'
                unique_object_types_value = 'Diversion'

            # print unique_object_types_value

            # limit the loop to the unique_object_types_value
            if Branch.TypeName == unique_object_types_value:  # and Branch.TypeName==branch_data['ObjectType']:
                # print Branch.TypeName, unique_object_types_value

                for branch_data in BranchesNew_list:
                    #                 print branch_data['BranchName']
                    # print '''branch_data['ObjectType']=''',branch_data['ObjectType']
                    if branch_data['ObjectType'] == 'River Headflow':
                        branch_data_Value = 'River'

                    elif branch_data['ObjectType'] == 'Diversion Outflow':
                        branch_data_Value = 'Diversion'
                    else:
                        branch_data_Value = branch_data['ObjectType']
                    # narrow the variables search for the branch that is extracted earlier as part of the network
                    # narrow the search further by also matching the ObjectType
                    # there is a case where the same branch name could belong to a Reservoir or a Headflow
                    # this happens when a reservoir is names like this "Hyrum"
                    # print 'Branch.Name=', Branch.Name
                    # print '''branch_data['BranchName']=''',branch_data['BranchName']
                    # print 'Branch.TypeName=',Branch.TypeName
                    # print 'Branch_data_Value=',branch_data_Value

                    if Branch.FullName == branch_data['FullBranchName'] and Branch.TypeName==branch_data_Value:
                        # print 'BranchName='+ Branch.FullName
                        # print '''branch_data['BranchName']'''+branch_data['FullBranchName']
                    # there is an issue in this above if clause that does not allow passing/getting the variables of a river headflow
                    # maybe it has to do with how the headflow word is added to the branch name. check
                        #                     print  branch_data['ObjectType']
                        #                     print  branch_data['BranchName']
                        #                     print  branch_data['InstanceName']
                        BranchType = Branch.TypeName
                        # print BranchType
                        # combinatiion of unique variable for each object type
                        for V in Branch.Variables:
                            if not V.IsResultVariable:# and V.Name in ['Annual Activity Level']:#,'Monthly Demand']:
                                FullBranch = Branch.FullName
                                BranchType = Branch.TypeName
                                VariableName = V.Name
                                # print VariableName

                                #                             print FullBranch
                                if BranchType == 'River':
                                    BranchType = 'River Headflow'

                                if BranchType == 'Diversion':
                                    BranchType = 'Diversion Outflow'

                                BranchName = Branch.Name
                                #                             print BranchName
                                VariableName = V.Name
                                UnitText = V.ScaleUnitText
                                ExpresValue = V.Expression
                                AttributeUnit=V.ScaleUnitText
                                if AttributeUnit == '':
                                    AttributeUnit = '-'
                                Result = OrderedDict()
                                Result['FullBranch'] = FullBranch
                                Result['BranchType'] = BranchType
                                Result['InstanceName'] = branch_data['InstanceName']
                                Result['UnitText'] = UnitText
                                Result['ExpresValueType'] = ''
                                Result['ExpresValue'] = ExpresValue
                                Result['BranchName'] = BranchName # use it later for verification reasons


                                UniqObjectAtt = OrderedDict()
                                # Time Series (CSV) if the value starts with "ReadFromFile"
                                if 'ReadFromFile' in ExpresValue:
                                    # TimeSeries_ExpressValue = ExpresValue

                                    # TimeSeries_ExpressValue_list.append(TimeSeries_ExpressValue)
                                    Result['ExpresValueType'] = 'TimeSeries_ExpressValue'
                                    #                                 print TimeSeries_ExpressValue
                                    UniqObjectAtt['ObjectType']=BranchType

                                    # check if UniqObjectAtt['AttributeName'] and Result['VariableName']
                                    # already has a value ==VariableName + '_TS' or VariableName + '_TS'+_B
                                    # if yes, then add a letter to the new coming value like _B or _C
                                    # char_list = 'ABCD' # good
                                    # here, we need to compare or check the Variable name including the '_TS'
                                    # Thi is a work a round to create unique attribute names as they come with different unit names in WEAP
                                    objectType_names = {}
                                    VariableName = VariableName + '_TS'
                                    if (BranchType, VariableName) in atrr_names.keys():
                                        objectType_names = atrr_names[(BranchType, VariableName)]

                                    updated_VariableName = getValuename(objectType_names, V.Name, '_TS', AttributeUnit) #also here pass the unit
                                    # the function should return updated_VariableName each time. this value can be same like before, or it can be new

                                    UniqObjectAtt['AttributeName']= updated_VariableName
                                    Result['VariableName'] = updated_VariableName
                                    objectType_names[AttributeUnit]=updated_VariableName
                                    atrr_names[(BranchType, VariableName)] = objectType_names


                                    UniqObjectAtt['AttributeUnit']=AttributeUnit
                                    UniqObjectAtt['AttributeDataTypeCV']='TimeSeries'
                                    UniqObjectAtt['attributeName'] = VariableName
                                # Seasonal if the value starts with "MonthlyValues"
                                elif 'MonthlyValues' in ExpresValue:
                                    # Seasonal_ExpressValue = ExpresValue
                                    Result['ExpresValueType'] = 'Seasonal_ExpressValue'
                                #                                 print Seasonal_ExpressValue
                                    UniqObjectAtt['ObjectType'] = BranchType
                                    objectType_names = {}
                                    VariableName = VariableName + '_Se'
                                    if (BranchType, VariableName) in atrr_names.keys():
                                        objectType_names = atrr_names[(BranchType, VariableName)]

                                    #is this updated_VariableName a string? yes?
                                    updated_VariableName = getValuename(objectType_names, V.Name, '_Se', AttributeUnit)

                                    UniqObjectAtt['AttributeName'] = updated_VariableName
                                    Result['VariableName'] = updated_VariableName
                                    objectType_names[AttributeUnit] = updated_VariableName
                                    atrr_names[(BranchType, VariableName)] = objectType_names

                                    # UniqObjectAtt['AttributeName'] = VariableName + '_Se'
                                    # Result['VariableName'] = VariableName + '_Se'
                                    UniqObjectAtt['AttributeUnit']=AttributeUnit
                                    UniqObjectAtt['AttributeDataTypeCV'] = 'SeasonalNumericValues'
                                    UniqObjectAtt['attributeName'] = VariableName
########################################################################################################################
                                # multi columns if the value starts with "VolumeElevation"
                                elif 'VolumeElevation' in ExpresValue:
                                    MultiColumns_ExpressValue = ExpresValue
                                    Result['ExpresValueType'] = 'MultiColumns_ExpressValue'
                                #                                 print MultiColumns_ExpressValue
                                    UniqObjectAtt['ObjectType'] = BranchType

                                    objectType_names = {}
                                    VariableName = VariableName + '_MA'
                                    if (BranchType, VariableName) in atrr_names.keys():
                                        objectType_names = atrr_names[(BranchType, VariableName)]

                                    updated_VariableName = getValuename(objectType_names, V.Name, '_MA', AttributeUnit)
                                    UniqObjectAtt['AttributeName'] = updated_VariableName
                                    Result['VariableName'] = updated_VariableName
                                    objectType_names[AttributeUnit] = updated_VariableName
                                    atrr_names[(BranchType, VariableName)] = objectType_names

                                    # UniqObjectAtt['AttributeName'] = VariableName + '_MA'
                                    #
                                    # Result['VariableName'] = VariableName + '_MA'
                                    # print Result['VariableName']
                                    UniqObjectAtt['AttributeUnit']=AttributeUnit
                                    UniqObjectAtt['AttributeDataTypeCV'] = 'MultiAttributeSeries'
                                    UniqObjectAtt['attributeName'] = VariableName
                                # Numeric if the value is a float (single value) e.g., "0", "100" etc

                                else:
                                    try:
                                        if ExpresValue == '':
                                            Numeric_ExpressValue = ''
                                        #                                         print Numeric_ExpressValue
                                        else:
                                            if '.' in ExpresValue:
                                                numeric_val = float(ExpresValue)
                                            else:
                                                numeric_val = int(ExpresValue)
                                            Numeric_ExpressValue = ExpresValue
                                            Result['ExpresValueType'] = 'Numeric_ExpressValue'

                                            UniqObjectAtt['ObjectType'] = BranchType

                                            objectType_names = {}
                                            VariableName = VariableName + '_Nu'
                                            if (BranchType, VariableName) in atrr_names.keys():
                                                objectType_names = atrr_names[(BranchType, VariableName)]

                                            updated_VariableName = getValuename(objectType_names, V.Name, '_Nu', AttributeUnit)
                                            UniqObjectAtt['AttributeName'] = updated_VariableName
                                            Result['VariableName'] = updated_VariableName
                                            objectType_names[AttributeUnit] = updated_VariableName
                                            atrr_names[(BranchType, VariableName)] = objectType_names
                                            # UniqObjectAtt['AttributeName'] = VariableName + '_Nu'
                                            # Result['VariableName'] = VariableName + '_Nu'

                                            UniqObjectAtt['AttributeUnit'] = AttributeUnit
                                            UniqObjectAtt['AttributeDataTypeCV'] = 'NumericValues'
                                            UniqObjectAtt['attributeName'] = VariableName
                                    #                                         print Numeric_ExpressValue
                                    # Other if the value other than the above (example: "Storage Capacity[AF]")

                                    except:
                                        Descriptor_ExpressValue = ExpresValue
                                        Result['ExpresValueType'] = 'FreeText'

                                        UniqObjectAtt['ObjectType'] = BranchType

                                        objectType_names = {}
                                        VariableName = VariableName + '_Fr'
                                        if (BranchType, VariableName) in atrr_names.keys():
                                            objectType_names = atrr_names[(BranchType, VariableName)]

                                        updated_VariableName = getValuename(objectType_names, V.Name, '_Fr', AttributeUnit)
                                        UniqObjectAtt['AttributeName'] = updated_VariableName
                                        Result['VariableName'] = updated_VariableName
                                        objectType_names[AttributeUnit] = updated_VariableName
                                        atrr_names[(BranchType, VariableName)] = objectType_names
                                        # UniqObjectAtt['AttributeName'] = VariableName + '_Fr'
                                        #
                                        # Result['VariableName'] = VariableName + '_Fr'

                                        UniqObjectAtt['AttributeUnit'] = AttributeUnit
                                        UniqObjectAtt['AttributeDataTypeCV'] = 'FreeText'
                                        UniqObjectAtt['attributeName'] = VariableName
    #                                     print Descriptor_ExpressValue

    #     Bird Refuge,Bird Refuge,Demand Site
    # print 'done'
                                Result_list.append(Result)
                                UniqObjectAtt_list_all.append(UniqObjectAtt)

    # keep unique values only

    UniqObjectAtt_list = []
    AttrSeries=[]
    atrr_name_list = []
    for unique in UniqObjectAtt_list_all:
        # UniqObjectAtt['attributeName'] = VariableName
        if (unique['ObjectType'], unique['AttributeName'],  unique['AttributeUnit']) in atrr_name_list: continue
        UniqObjectAtt_list.append(unique)
        atrr_name_list.append((unique['ObjectType'], unique['AttributeName'], unique['AttributeUnit']))


    # append AttributeSeries for the attributes of the reservoir into the UniqObjectAtt_list
    # these are values for two rows
    for atts in UniqObjectAtt_list:
        if atts['AttributeName']=='Volume Elevation Curve_MA':
            AttrSeries = OrderedDict()
            AttrSeries['ObjectType']='Reservoir'
            AttrSeries['AttributeName']='Volume-Curve'
            AttrSeries['AttributeUnit']='AF'
            AttrSeries['AttributeDataTypeCV']='AttributeSeries'
            UniqObjectAtt_list.append(AttrSeries)

            AttrSeries = OrderedDict()
            AttrSeries['ObjectType']='Reservoir'
            AttrSeries['AttributeName']='Elevation-Curve'
            AttrSeries['AttributeUnit']='AC'
            AttrSeries['AttributeDataTypeCV']='AttributeSeries'

            UniqObjectAtt_list.append(AttrSeries)

        # append the global attributs to the the rest of the attributes
    for g_atts in GlobalAttributes_List:
        g_AttrSeries = OrderedDict()
        g_AttrSeries['ObjectType'] = g_atts['ObjectType']
        g_AttrSeries['AttributeName'] = g_atts['AttributeName']
        g_AttrSeries['AttributeUnit'] = g_atts['AttributeUnit']
        g_AttrSeries['ExpresValueType'] = g_atts['AttributeDataTypeCV']
        UniqObjectAtt_list.append(g_AttrSeries)

    # append the global values into the Result
    for g_Res in Global_Result_List:
        g_Result = OrderedDict()
        g_Result['FullBranch']=g_Res['FullBranch']
        g_Result['BranchType'] = g_Res['BranchType']
        g_Result['InstanceName']=g_Res['InstanceName']
        g_Result['VariableName'] = g_Res['Attribute']
        g_Result['ExpresValueType'] = g_Res['ExpresValueType']
        g_Result['ExpresValue'] = g_Res['ExpresValue']

        Result_list.append(g_Result)



    # sort all of them ascending by value ascending based on first: ObjectType, then AttributeName
    UniqObjectAtt_list = sorted(UniqObjectAtt_list, key = lambda AttrSeries: (AttrSeries['ObjectType'], AttrSeries['AttributeName']))



    return Result_list,UniqObjectAtt_list
        # , TimeSeries_ExpressValue_list
# so create an element that binds the three items together:
# # Key =UpdatedVariableName
# # values: ObjectType, AttributeName, Unit
# the first time, we check, do these three values have a key? if no, then create it. If yes, then reuse it

# return updated_VariableName many times. If the combination changes, then retun the new updated_VariableName
def getValuename(objectType_names, VariableName, added_char, AttributeUnit):
    updated_VariableName = VariableName + added_char

    if len (objectType_names.keys()) < 1:
        return updated_VariableName
    else:
        if AttributeUnit in objectType_names.keys():
            return objectType_names[AttributeUnit]
        else:
            values = []
            for key in objectType_names.keys():
                values.append(objectType_names[key])
            char_list = 'ABCD'
            for char in char_list:
                updated_VariableName = VariableName + '{}_{}'.format(added_char, char)
                if not updated_VariableName in values:
                    return updated_VariableName
                    break
