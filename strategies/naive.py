from .base import BaseCEPStrategy,CEPGroup

class OneToOneCEPStrategy(BaseCEPStrategy):
    ''' Grouping Strategy is each school has its own group '''
    name = "OneToOne"

    def create_groups(self,district):
        self.groups = [
            CEPGroup(school.district,school.name,[school])
            for school in district.schools
        ] 

class OneGroupCEPStrategy(BaseCEPStrategy):
    ''' Grouping Stretegy is creates a single group of all schools in the district ''' 
    name = "OneGroup"
    def create_groups(self,district):
        self.groups = [
            CEPGroup(district,"%s - Consolidated" % district.name,district.schools)
        ]


