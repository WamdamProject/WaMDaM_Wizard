import win32com.client

WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")

WEAP.ActiveArea = "BearRiverFeb2017_V10.9"
from collections import OrderedDict
import xlsxwriter

Result = {}

Result_list = []

wb = xlsxwriter.Workbook('C:/Users/Adel/Documents/test144.xlsx')
ws = wb.add_worksheet()

row = 0
col = 0

field_names = ['FullBranch', 'BranchType', 'BranchName', 'VariableName', 'UnitText', 'ExpresValue']

for i in range(len(field_names)):
    ws.write(0, i, field_names[i])

row = 1

for Branch in WEAP.Branches:
    if Branch.TypeName == "Return Flows":
        for V in Branch.Variables:
            if not V.IsResultVariable:  # and V.Name=="Demand Priority":
                FullBranch = Branch.FullName
                BranchType = Branch.TypeName
                BranchName = Branch.Name
                VariableName = V.Name
                UnitText = V.ScaleUnitText
                ExpresValue = V.Expression

                Result = OrderedDict()
                Result['FullBranch'] = FullBranch
                Result['BranchType'] = BranchType
                Result['BranchName'] = BranchName
                Result['VariableName'] = VariableName
                Result['UnitText'] = UnitText
                Result['ExpresValue'] = ExpresValue

                Result_list.append(Result)

                col = 0
                for key in Result.keys():
                    ws.write(row, col, Result[key])
                    col += 1
                row += 1

wb.close()

#         {'FullBranch' : FullBranch,'BranchType' : BranchType,'BranchName':BranchName,'VariableName' : VariableName,'UnitText':UnitText,'ExpresValue':ExpresValue}
#         print Result

#         save this result to an excel file

#         print FullBranch
#         print BranchType
#         print BranchName
#         print VariableName
#         print ExpresValue
# pass the values from the result above using the three fields:FullBranch,
# print Result['FullBranch']
# print Result
FullBranch = Result['FullBranch']
for temp_result in Result_list:
    FullBranchValues = temp_result['FullBranch']
    #print Result_list
    WEAP.Branch(FullBranchValues).Variable(temp_result['VariableName']).Expression = temp_result['ExpresValue']
