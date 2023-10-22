from .base import BaseCEPStrategy,CEPGroup

class OneToOneCEPStrategy(BaseCEPStrategy):
    ''' Grouping Strategy is each school has its own group '''
    name = "OneToOne"

    def create_groups(self,district):
        self.groups = [
            CEPGroup(district,school.name,[school],self.isp_threshold)
            for school in district.schools
        ] 

class OneGroupCEPStrategy(BaseCEPStrategy):
    ''' Grouping Stretegy is creates a single group of all schools in the district ''' 
    name = "OneGroup"
    def create_groups(self,district):
        self.groups = [
            CEPGroup(district,"%s - Consolidated" % district.name,district.schools,self.isp_threshold)
        ]


class CustomGroupsCEPStrategy(BaseCEPStrategy):
    ''' Custom grouping, for juptyer when you have a hand-optimized list'''
    def set_groups(self,group_list):
        ''' Expects list of tuples of (group_id,school_code) '''
        self.groupings = {}
        for g in group_list:
            self.groupings.setdefault(g[0],[])
            self.groupings[g[0]].append(g[1])

    def create_groups(self,district):
        self.groups = []
        for g in self.groupings:
            schools = [ s for s in district.schools if s.code in self.groupings[g]]
            self.groups.append( CEPGroup(district,"Group %s" % g, schools,self.isp_threshold) )


