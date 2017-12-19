'Adel Abdallah, May 1 2017. Utah State University
'WaMDaM workbook template
'This Macro applies to all the spreadsheets in the docuemnt
'It allows a searchable dropdown list


Private Sub TempCombo_KeyDown(ByVal KeyCode As MSForms.ReturnInteger, ByVal Shift As Integer)
'While DropDown is active after doble Click, this macro runs for two cases:
Select Case KeyCode
Case 9 '1. If Enter is pressed, then the cell below the activecell is activated
Application.ActiveCell.Offset(0, 1).Activate
Case 13 '2.If Tab is pressed, then the cell to the right is activated
Application.ActiveCell.Offset(1, 0).Activate
End Select
End Sub


Private Sub Workbook_SheetBeforeDoubleClick(ByVal Sh As Object, ByVal Target As Range, Cancel As Boolean)
'When a cell is DobleClicked this macro perform the following tasks:
'1. Add a ComboBox and name it as: TempCombo
Dim xStr As String
Dim xCombox As OLEObject
Dim xWs As Worksheet
Set xWs = Application.ActiveSheet
On Error Resume Next
Application.EnableEvents = False
Set xCombox = xWs.OLEObjects("TempCombo")
With xCombox
.ListFillRange = ""
.LinkedCell = ""
.Visible = False
End With

'2.Change the properties of the ComboBox to make it empty and invisible
If Target.Validation.Type = 3 Then
Cancel = True
xStr = Target.Validation.Formula1
xStr = Right(xStr, Len(xStr) - 1)
With xCombox
.Visible = True
.Left = Target.Left
.Top = Target.Top
.Width = Target.Width + 5
.Height = Target.Height + 5
.ListFillRange = xStr
.LinkedCell = Target.Address
End With
xCombox.Activate
ActiveSheet.TempCombo.DropDown
End If

Application.EnableEvents = True
End Sub

'Every time the selected cell in the sheet is changed, if there's a ComboBox named TempCombo, then it's reset it (Empty and Invisible)
Private Sub Workbook_SheetSelectionChange(ByVal Sh As Object, ByVal Target As Range)
Dim fdvdf As Object
Set fdvdf = ActiveSheet.OLEObjects.Add(ClassType:="Forms.ComboBox.1", Link:=False, _
DisplayAsIcon:=False, Left:=10000, Top:=0.1, _
Width:=0.1, Height:=0.1)
With fdvdf
.Name = "TempCombo"
End With
Dim xCombox As OLEObject
Dim xWs As Worksheet
Set xWs = Application.ActiveSheet
On Error Resume Next
Application.EnableEvents = False
Application.ScreenUpdating = True
Set xCombox = xWs.OLEObjects("TempCombo")
With xCombox
.Top = 10
.Left = 10
.Width = 0
.ListFillRange = ""
.LinkedCell = ""
.Visible = False
.Value = ""
End With
Application.EnableEvents = True

End Sub


