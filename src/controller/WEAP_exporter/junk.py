# Dynamicly get the global attributes under the Key Assumptions branch in WEAP
if 'Key\\' in BranchFullName:
    GlobalAttribute = BranchFullName.split("Key\\")[1]

    GlobalAttributes = OrderedDict()
    GlobalAttributes_List = []
    GlobalAttributes['ObjectType'] = 'WEAP Global Attributes'
    GlobalAttributes['AttributeName'] = GlobalAttribute

    GlobalAttributes_List.append(GlobalAttributes)