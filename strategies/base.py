from abc import ABC,abstractmethod

# Shortcut to deal with commas in integers from csv
i = lambda x: int(x.replace(',',''))

class CEPSchool(object):
    def __init__(self,data):
        self.district = data['District Name']
        self.district_code = data['District Code']
        self.name = data['School Name']
        self.code = data['School Code']
        self.foster = i(data['foster'])
        self.homeless = i(data['homeless'])
        self.migrant = i(data['migrant'])
        self.direct_cert = i(data['direct_cert'])
        self.frpm = i(data['frpm'])
        self.total_eligible = (self.foster + self.homeless + self.migrant + self.direct_cert)
        self.total_enrolled = i(data['total_enrolled'])
        if self.total_eligible > self.total_enrolled:
            self.total_eligible = self.total_enrolled

        self.breakfast_served = self.total_enrolled  # TODO provide as input
        self.lunch_served = self.total_enrolled #TODO provide as input

        if self.total_enrolled == 0:
            self.isp  = self.free_rate = self.paid_rate = 0
        else:
            self.isp = round(self.total_eligible / float(self.total_enrolled), 4)

    def as_dict(self):
        return {
            'school_code': self.code,
            'school_name': self.name,
            'total_enrolled': self.total_enrolled,
            'frpm': self.frpm ,
            'foster': self.foster,
            'homeless': self.homeless,
            'migrant': self.migrant,
            'direct_cert': self.direct_cert,
        }

class CEPGroup(object):
    def __init__(self,district,group_name,schools):
        # Expected Columns:
        # district,school,total_enrolled,frpm,foster,homeless,migrant,direct_cert

        self.district = district
        self.name = group_name
        self.total_eligible,self.total_enrolled = 0,0
        self.school_codes = set([s.code for s in schools])

        # Step 1 - calculate eligible students
        for school in schools:
            self.total_eligible += school.total_eligible
            self.total_enrolled += school.total_enrolled

        # If there are no enrolled students, we just bail       
        if self.total_enrolled == 0:
            self.isp = 0 
        else: 
            # Step 1 - Calculate ISP to 4 decimal places
            self.isp = round(self.total_eligible / float(self.total_enrolled), 4)

        # Then calculate free vs paid rate
        # IF(E11*1.6>=1,1,IF(E11<0.4,0,E11*1.6))
        self.free_rate = self.isp * 1.6
        if self.isp * 1.6 > 1:
            self.free_rate = 1
        elif self.isp < 0.4:
            self.free_rate = 0 

        self.paid_rate = 1.0 - self.free_rate
        if self.free_rate == 0:
            self.paid_rate = 0

    @property
    def covered_students(self):
        return round(self.free_rate * self.total_enrolled,0)

    def __repr__(self):
        if self.isp == None:
            return "%s / %s -- no students enrolled --" % (self.district, self.name)
        return "%s / %s ISP=%0.0f%% ENROLLED=%i FREE_RATE=%0.2f%%" % \
            (self.district,self.name,self.isp*100, self.total_enrolled, self.free_rate*100)

class CEPDistrict(object):
    def __init__(self,name,code,sfa_certified=False,anticipated_rate_change=0.02):
        self.name = name
        self.code = code
        self.schools = [] 
        self.groups = []
        self.sfa_certified = sfa_certified # TODO provide as input
        self.anticipated_rate_change = 0.02
        self.strategies = []
        self.best_strategy = None

    def __lt__(self,other_district):
        return self.total_enrolled < other_district.total_enrolled

    def run_strategies(self):
        for s in self.strategies:
            s.create_groups(self)

    def evaluate_strategies(self):
        best = None
        for s in self.strategies:
            assert(s.groups != None)
            if best == None or s.students_covered > best.students_covered:
                best = s
        self.best_strategy = best

    def __eq__(self,other_district):
        return self.code == other_district.code


    @property
    def total_enrolled(self): 
        return sum([s.total_enrolled for s in self.schools])

    @property
    def students_covered(self):
        return self.best_strategy.students_covered

    @property
    def percent_covered(self):
        return float(self.best_strategy.students_covered)/self.total_enrolled

    def reimbursement(self):
        # TODO calculate reimbursement amount
        raise NotImplemented("Need to calculate based on CEP Estimator")

class BaseCEPStrategy(ABC):
    total_eligible = None
    groups = None
    name = "Abstract Strategy"
    params = {}

    def __init__(self,params={},name=None):
        self.params = params
        self.groups = None
        if name: self.name = name

    @property
    def students_covered(self):
        return sum([g.covered_students for g in self.groups])
    
    @abstractmethod
    def create_groups(self,district):
        raise NotImplemented("Override this with the grouping strategy")

    def matches_grouping_of(self,other_strategy):
        ''' Compare districts by looking to see if their grouped school codes are identical'''
        if len(self.groups) == 0 or len(other_strategy.groups) == 0:
            raise ValueError("Please run create_groups before comparing districts: %s (%i) = %s (%i)" %
                   (self.name,len(self.groups), other_strategy.name, len(other_strategy.groups) ) )

        # Then walk through our groups, and look for an identical group in the other district
        for g in self.groups:
            found = False
            for og in other_strategy.groups:
                if g.school_codes == og.school_codes: 
                    found = True  
                    break
            # If we do not find a matching group, these districts do not have the same grouping
            if not found: return False
        return True

