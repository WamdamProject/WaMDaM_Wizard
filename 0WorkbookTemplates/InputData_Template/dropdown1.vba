'Adel Abdallah, Feb 3, 2017. Utah State University
'WaMDaM workbook template
'This Macro applies to all the spreadsheets in the docuemnt
'It allows a searchable dropdown list, prevents users from over pasting (deleting) validation lists

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
Dim fdvdf As Object
Set fdvdf = ActiveSheet.OLEObjects.Add(ClassType:="Forms.ComboBox.1", Link:=False, _
DisplayAsIcon:=False, Left:=10000, Top:=0.1, _
Width:=0.1, Height:=0.1)
With fdvdf
.Name = "TempCombo"
End With
'2.Change the properties of the ComboBox to make it empty and invisible
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

'3. To allow copy/paste into workbook sheets, a conditional was added to limit the macro.
   'So if the cell which is being DobleClicked has a Data Validation, then the macro will keep running, otherwise it won't do anything
On Error GoTo fin
If Target.SpecialCells(xlCellTypeSameValidation).Cells.Count > 0 Then

'3.1 As the DobleClicked cell has a data validation then the macro only keeps running if the Data Validation is a DropDown List.
    'So, it is, then it formats the ComboBox to makes it visible in the activecell
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
End If
Application.EnableEvents = True
fin:
End Sub




Private Sub Workbook_SheetSelectionChange(ByVal Sh As Object, ByVal Target As Range)
'Every time the selected cell in the sheet is changed, if there's a ComboBox named TempCombo, then it's reset it (Empty and Invisible)
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

Private Sub Workbook_SheetChange(ByVal Sh As Object, ByVal Target As Range)
'This Macro uses the HasValidation function to evaluate the cell which is being changed.
'If the cell has a data validation, then it undo the change and shows a message: Please use the drop-down to enter data instead.
Dim xValue As String
Dim xCheck1 As String
Dim xCheck2 As String
If Target.Count > 1 Then
Exit Sub
End If
Application.EnableEvents = False
xValue = Target.Value
On Error Resume Next
xCheck1 = Target.Validation.InCellDropdown
On Error GoTo 0
Application.Undo
On Error Resume Next
xCheck2 = Target.Validation.InCellDropdown
On Error GoTo 0
If xCheck1 = xCheck2 Then
Target = xValue
Else
'Display this error message
MsgBox "You're trying to paste data over a validation list! Please choose from the dropdown menu"
End If
Application.EnableEvents = True
End Sub



