import datetime

def upload(mealCountsSchool, inputEmail):
	requestDbObject= MC_REQUEST(request_time =datetime.datetime.now(), pending = False, email = inputEmail)
	schoolDbObject = MC_SCHOOL(school_name = mealCountsSchool.schoolName, total_number_of_students = mealCountsSchool.numTotalStudents, identified_student_population = mealCountsSchool.numIdentifiedStudents, request = requestDbObject)
	requestDbObject.save()
	schoolDbObject.save()

# See mealcountsschool.py for a definition of objects in the mealCountsSchoolsArray
def uploadInformation(mealCountsSchoolsArray, inputEmail):
	for mealCountsSchool in mealCountsSchoolsArray:
		upload(mealCountsSchool)
