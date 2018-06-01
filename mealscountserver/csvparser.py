from .models import School


def parseSchoolInfo(csvLine):
    components = csvLine.split(',')
    return School(components[0], components[1], components[2])


def parseCsv(csvString):
    csvLines = csvString.splitlines()
    mealCountsSchools = []
    # Ignore first line
    csvLines = csvLines[1:]
    for csvLine in csvLines:
        mealCountsSchools = [parseSchoolInfo(csvLine)] + mealCountsSchools
    return mealCountsSchools
