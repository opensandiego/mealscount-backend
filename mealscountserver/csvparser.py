from mealcountschool import mealcountschool

def parseSchoolInfo(csvLine):
	components = csvLine.split(',')
	return mealcountschool(components[0], long(components[1]), long(components[2]))


def parseCsv(csvString):
	csvLines = csvString.splitlines()
	mealCountsSchools = []
	for csvLine in csvLines:
		mealCountsSchools = [parseSchoolInfo(csvLine)] + mealCountsSchools
	return mealCountsSchools