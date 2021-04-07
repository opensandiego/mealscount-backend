Attribute VB_Name = "MealsCount"
' Meals Count VBA Grouping Connector
' Requires https://github.com/VBA-tools/VBA-JSON
' And https://github.com/VBA-tools/VBA-Dictionary/releases
' Expects a range of cells called "MealsCountSchools"
' In the order
' Name,total enrolled, total eligible, breakfast adp, lunch adp, severe neeed, grouping
'
Public Sub GetGroupingsFromMealsCount()

    Dim PollUrl As String
    Dim Result As Object
    Dim SchoolRange As Range
    Dim Countdown As Integer
    
    Set Schools = New Collection
    Set DistrictJson = New Dictionary
    
    On Error Resume Next
    Set SchoolRange = Sheets("3. MEALSCOUNT IMPORT").Range("MealsCountSchools")
    If Err = 1004 Then
        MsgBox "School cells must be in a Named Range called MealsCountSchools"
        Exit Sub
    End If
    
    
    DistrictJson.Add "state_code", "ca"
    DistrictJson.Add "code", "12345"
    DistrictJson.Add "name", "Test District"
    DistrictJson.Add "schools", Schools

    For Each Row In SchoolRange.Rows
        If Not IsEmpty(Row.Cells(1, 1).Value) Then
            Set School = New Dictionary
            School.Add "school_name", Row.Cells(1, 1).Value
            School.Add "school_code", Row.Cells(1, 1).Value
            School.Add "total_enrolled", Row.Cells(1, 2).Value
            School.Add "total_eligible", Row.Cells(1, 3).Value
            School.Add "daily_breakfast_served", Row.Cells(1, 4).Value
            School.Add "daily_lunch_served", Row.Cells(1, 5).Value
            School.Add "severe_need", Row.Cells(1, 6).Value
            Schools.Add School
        End If
    Next

    ' MsgBox JsonConverter.ConvertToJson(DistrictJson)

    With CreateObject("MSXML2.XMLHTTP")
        .Open "POST", "https://www.mealscount.com/api/districts/optimize-async/", False
        .setRequestHeader "Content-Type", "application/json"
        .send JsonConverter.ConvertToJson(DistrictJson)
        Set Result = JsonConverter.ParseJson(.responseText)
        PollUrl = Result("results_url")
        
        MsgBox "Schools sent to MealsCount.com, waiting for grouping result"
        
        Countdown = 60
        Do While Not Result.Exists("code")
            Application.Wait (Now + TimeValue("0:00:5"))
            Countdown = Countdown - 1
            
            Set PollRequest = CreateObject("MSXML2.XMLHTTP")
            PollRequest.Open "GET", PollUrl, False
            PollRequest.send ""
            If PollRequest.Status = 200 Then
                Set Result = JsonConverter.ParseJson(PollRequest.responseText)
                Set Groupings = Result("strategies")(Result("best_index") + 1)("groups")
                num = 0
                Set SchoolGroupMap = New Dictionary
                For Each Group In Groupings:
                    num = num + 1
                    For Each SchoolName In Group("school_codes")
                        SchoolGroupMap.Add SchoolName, num
                    Next
                Next
                For Each Row In SchoolRange.Rows
                    SchoolName = Row.Cells(1, 1).Value
                    If SchoolGroupMap.Exists(SchoolName) Then
                        Row.Cells(1, 7).Value = SchoolGroupMap(SchoolName)
                    End If
                Next
                MsgBox "Groupings Updated!"
                Exit Sub
            End If
        Loop
        
        MsgBox "Sorry, there was an error getting results. Please try again or contact us at mealscount.com/contact"
        
        .abort
    End With

End Sub

