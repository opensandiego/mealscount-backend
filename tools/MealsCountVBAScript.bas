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
    Set SchoolRange = Range("MealsCountSchools")
    If Err = 1004 Then
        MsgBox "School cells must be in a Named Range called MealsCountSchools"
        Exit Sub
    End If
    
    On Error Resume Next
    Set StateRange = Range("MealsCountState")
    State = "ca"
    If Err = 1004 Then
    Else
        State = StateRange.Cells(1, 1).Value
    End If
    
    On Error Resume Next
    Set DistrictRange = Range("MealsCountDistrict")
    DistrictName = "DistrictName"
    DistrictCode = "DistrictCode"
    If Err = 1004 Then
    Else
        If Not IsEmpty(DistrictRange.Cells(1, 1)) Then
            DistrictName = DistrictRange.Cells(1, 1).Value
            DistrictCode = DistrictRange.Cells(1, 1).Value
        End If
    End If
    
    DistrictJson.Add "state_code", State
    DistrictJson.Add "code", DistrictCode
    DistrictJson.Add "name", DistrictName
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
    
    Dim MealsCountClient As New WebClient
    Dim Response As WebResponse
    Dim Options As Dictionary
        
    Set Response = MealsCountClient.PostJson("https://www.mealscount.com/api/districts/optimize-async/", DistrictJson, Options)
    PollUrl = Response.Data("results_url")
        
    MsgBox "Schools sent to MealsCount.com, waiting for grouping result"
        
    Countdown = 60
    Do While Not Result.Exists("code")
        Application.Wait (Now + TimeValue("0:00:5"))
        Countdown = Countdown - 1
        
        Set Response = MealsCountClient.GetJson(PollUrl)
        If Response.StatusCode = 200 Then
            Set Result = Response.Data
            Set Groupings = Result("strategies")(Result("best_index") + 1)("groups")
            num = 0
            Set SchoolGroupMap = New Dictionary
            Set GroupDict = New Dictionary
            For Each Group In Groupings:
                num = num + 1
                GroupDict.Add num, Group
                For Each SchoolName In Group("school_codes")
                    SchoolGroupMap.Add SchoolName, num
                Next
            Next
            For Each Row In SchoolRange.Rows
                SchoolName = Row.Cells(1, 1).Value
                
                Set Group = GroupDict(SchoolGroupMap(SchoolName))
                If Not SchoolName Like "[]" And SchoolGroupMap.Exists(SchoolName) Then
                    Row.Cells(1, 7).Value = SchoolGroupMap(SchoolName)
                    Row.Cells(1, 8).Value = Group("isp")
                End If
            Next
            MsgBox "Groupings Updated!"
            Exit Sub
        End If
    Loop
    
    MsgBox "Sorry, there was an error getting results. Please try again or contact us at mealscount.com/contact"

End Sub

