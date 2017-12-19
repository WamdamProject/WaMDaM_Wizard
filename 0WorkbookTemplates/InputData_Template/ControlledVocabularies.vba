'Adel Abdallah, May 1 2017. Utah State University
'WaMDaM workbook template
'Credit: I adapted this script from the script used in updating ODM2 CV terms.
'Thansk to the www.odm2.org team for sharing their code online


Function getVocabulary(url As String, vocabularyname As String) As Boolean
    'Check if the temporary vocabulary worksheet exists and add if necessary
    Dim wsTest As Worksheet
            
    Set wsTest = Nothing
    On Error Resume Next
    Set wsTest = Worksheets(vocabularyname)
    On Error GoTo 0
            
    If wsTest Is Nothing Then
        Worksheets.Add.Name = vocabularyname
    End If

    Worksheets(vocabularyname).Activate

    'Create the query table for the vocabulary
    Application.DisplayAlerts = False
    On Error GoTo ErrRemoteFile
    With ActiveSheet.QueryTables.Add(Connection:=url, Destination:=Range("A1"))
        .Name = "cv_" & vocabularyname
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .TextFilePromptOnRefresh = False
        .TextFilePlatform = xlWindows
        .TextFileStartRow = 1
        .TextFileParseType = xlDelimited
        .TextFileTextQualifier = xlTextQualifierDoubleQuote
        .TextFileConsecutiveDelimiter = False
        .TextFileTabDelimiter = False
        .TextFileSemicolonDelimiter = False
        .TextFileCommaDelimiter = True
        .TextFileSpaceDelimiter = False
        .TextFileColumnDataTypes = Array(1, 1, 1, 1, 1, 1, 1, 1)
        .Refresh BackgroundQuery:=False
        '.UseListObject = False 'This causes an error on Windows
    End With
    Application.DisplayAlerts = True
    
    'Delete the query table after retrieving the CV
    Worksheets(vocabularyname).QueryTables(1).Delete
    
    getVocabulary = True
    Exit Function

ErrRemoteFile:
    'Delete the temporary CV worksheet I just created because it won't be used
    Application.DisplayAlerts = False
    Worksheets(vocabularyname).Delete
    Application.DisplayAlerts = True
    
End Function


Sub ImportCVs()
    'switch off updating to speed up the code & stop irritating flickering
    Application.ScreenUpdating = False
        
    'Don't allow macros that run on changes to worksheets to run
    Allow_Change_Macro = "NO"
     
    'Change the Status Bar to inform  user of the macro's progress and set the cursor to waiting
    Application.Cursor = xlWait
    Application.DisplayStatusBar = True
    Application.StatusBar = "Updating Controlled Vocabularies"

    'Set up links to the vocabulary terms online
    Dim CVWebPath, CVWebAPI, CVWebExtension As String
    'Access the WaMDaM Controlled Vocabulary Registry
    CVWebPath = "http://vocabulary.wamdam.org/"
    CVWebAPI = "api/v1/"
    CVWebExtension = "/?format=csv"
    
    'Find the list of vocabularies from the controlled vocabularies worksheet
    list_of_vocabs = Worksheets("ControlledVocabularies").Range("ControlledVocabularies[#Headers]")
    NumVocabs = Worksheets("ControlledVocabularies").Range("ControlledVocabularies[#Headers]").Count
    
    'Check if workbook is protected and unprotect to be able to add worksheets
    Dim Protection As String
    If ActiveWorkbook.ProtectStructure Then Protection = "YES"
    If Protection = "YES" Then ActiveWorkbook.Unprotect Password:="wamdam"

    'Loop through all of the vocabularies
    Dim i As Integer
    i = 0
    
    For Each vocabulary In list_of_vocabs
    
        i = i + 1
        Application.StatusBar = "Updating Vocabulary " & i & " of " & NumVocabs & " (" & vocabulary & ")"
        Dim FullWebPath As String
        FullWebPath = CVWebPath & CVWebAPI & vocabulary & CVWebExtension
        QTPath = "TEXT;" & CVWebPath & CVWebAPI & vocabulary & CVWebExtension
        
        If getVocabulary(CStr(QTPath), CStr(vocabulary)) <> 0 Then
            
            'Clear the column in the vocabularies table so it's ready for new values
            Worksheets("ControlledVocabularies").Range("ControlledVocabularies[" & vocabulary & "]").ClearContents
        
            'Find the column and row numbers to copy and to paste into
            Dim NameColumn, NumVocabTerms, VocabCol As Integer
            VocabCol = Worksheets("ControlledVocabularies").Range("ControlledVocabularies[" & vocabulary & "]").Column
            NameColumn = Worksheets(vocabulary).Range("A1:H1").Find(What:="name", LookIn:=xlValues, LookAt:=xlWhole).Column
            NumVocabTerms = Worksheets(vocabulary).Range("A2", Worksheets(vocabulary).Range("A2").End(xlDown)).Rows.Count + 1

            'Must copy starting at row two to avoid the header
            Worksheets(vocabulary).Range(Worksheets(vocabulary).Cells(2, NameColumn), Worksheets(vocabulary).Cells(NumVocabTerms, NameColumn)).Copy
        
            'Paste the terms into the controlled vocabularies worksheet
            Worksheets("ControlledVocabularies").Cells(2, VocabCol).PasteSpecial xlPasteValues
            
            'Delete the temporary CV worksheet
            Application.DisplayAlerts = False
            Worksheets(vocabulary).Delete
            Application.DisplayAlerts = True
            
        End If
        
    Next vocabulary

    'Reprotect the workbook if it had been protected before
    If Protection = "YES" Then ActiveWorkbook.Protect Structure:=True, Windows:=False, Password:="wamdam"

    'Put the current date/time into the instructions sheet to let the user know the last vocab update time
    If Worksheets("HomePage").ProtectContents = True Then
        Worksheets("HomePage").Unprotect Password:="wamdam"
        Worksheets("HomePage").Range("VocabUpdate") = Now
        Worksheets("HomePage").Protect Password:="wamdam"
    Else
        Worksheets("HomePage").Range("VocabUpdate") = Now
    End If
        
    'Restore default cursor
    Application.Cursor = xlDefault

    'Give control of the statusbar back to the program
    Application.StatusBar = False
    Allow_Change_Macro = "YES"
    Application.ScreenUpdating = True
    
End Sub

