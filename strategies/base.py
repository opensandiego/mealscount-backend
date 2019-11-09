from abc import ABC,abstractmethod

# Shortcut to deal with commas in integers from csv
def i(x):
    if type(x) != str: return int(x)
    return int(x.replace(',',''))

# Free Rate from CEP Estimator
# IF(E11*1.6>=1,1,IF(E11<0.4,0,E11*1.6))
def isp_to_free_rate(isp):
    free_rate = isp * 1.6
    if isp * 1.6 > 1:
        free_rate = 1
    elif isp < 0.4:
        free_rate = 0 
    return free_rate

# TODO make this configurable parameter
BREAKFAST_EST_PARTICIPATION = (0.2852,0.8690) # 
LUNCH_EST_PARTICIPATION = (0.5998,0.9285)
EST_BFAST_INCREASE = 1.02 # TODO verify
EST_LUNCH_INCREASE = 1.02 # TODO verify


class CEPSchool(object):
    def __init__(self,data):
        self.district = data['District Name']
        self.district_code = data['District Code']
        self.name = data['School Name']
        self.code = data['School Code']
        self.school_type = data['School Type']
        self.active = data.get("include_in_mealscount","true").lower() == "true"
        self.foster = i(data.get('foster',0))
        self.homeless = i(data.get('homeless',0))
        self.migrant = i(data.get('migrant',0))
        self.direct_cert = i(data.get('direct_cert',0))
        self.frpm = i(data.get('unduplicated_frpm',0))
        self.total_eligible = self.direct_cert 
        # NOTE based upon California data, total eligible is "direct_cert", but still in progress!
        #i(data.get('unduplicated_frpm',0)) # (self.foster + self.homeless + self.migrant + self.direct_cert)
        self.total_enrolled = i(data['total_enrolled'])
        if self.total_eligible > self.total_enrolled:
            self.total_eligible = self.total_enrolled

        if data.get("daily_breakfast_served","").strip():
            self.bfast_served_low = int(data.get("daily_breakfast_served"))
            self.lunch_served_low = int(data.get("daily_lunch_served"))
            self.bfast_served_high = int(self.bfast_served_low * EST_BFAST_INCREASE)
            self.lunch_served_high = int(self.bfast_served_low * EST_LUNCH_INCREASE)
        else:
            self.bfast_served_low = int(self.total_enrolled * BREAKFAST_EST_PARTICIPATION[0])
            self.lunch_served_low = int(self.total_enrolled * LUNCH_EST_PARTICIPATION[0])
            self.bfast_served_high = int(self.total_enrolled * BREAKFAST_EST_PARTICIPATION[1])
            self.lunch_served_high = int(self.total_enrolled * LUNCH_EST_PARTICIPATION[1])

        if self.total_enrolled == 0:
            self.isp  = self.free_rate = self.paid_rate = 0
        else:
            self.isp = round(self.total_eligible / float(self.total_enrolled), 4)

    def as_dict(self):
        return {
            'school_code': self.code,
            'school_name': self.name,
            'school_type': self.school_type,
            'total_enrolled': self.total_enrolled,
            "total_eligible": self.total_eligible,
            "daily_breakfast_served": self.bfast_served_low,
            "daily_lunch_served": self.bfast_served_low,
            'isp': self.isp,
            'active': self.active,
        }

class CEPGroup(object):
    def __init__(self,district,group_name,schools):
        # Expected Columns:
        # district,school,total_enrolled,frpm,foster,homeless,migrant,direct_cert

        self.district = district
        self.name = group_name
        self.total_eligible,self.total_enrolled = 0,0
        self.school_codes = set([s.code for s in schools])

        self.schools = schools

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
        self.free_rate = isp_to_free_rate(self.isp)

        self.paid_rate = 1.0 - self.free_rate
        if self.free_rate == 0:
            self.paid_rate = 0

    @property
    def covered_students(self):
        return round(self.free_rate * self.total_enrolled,0)

    def est_reimbursement(self):
        '''basic estimate for daily reimbursement based on the given meal participation estimates
        '''
        # Identify federal reimbursement rates per this District (see CEP Estimator XLS file)
        bfast_re = (self.free_rate * self.district.fed_reimbursement_rates['free_bfast'] +
                    (1 - self.free_rate) * self.district.fed_reimbursement_rates['paid_bfast'])
        lunch_re = (self.free_rate * self.district.fed_reimbursement_rates['free_lunch'] +
                    (1 - self.free_rate) * self.district.fed_reimbursement_rates['paid_lunch'])

        eligible_breakfast_low = sum([s.bfast_served_low for s in self.schools])
        eligible_lunch_low = sum([s.lunch_served_low for s in self.schools]) 
        eligible_breakfast_high = sum([s.bfast_served_high for s in self.schools])
        eligible_lunch_high = sum([s.lunch_served_high for s in self.schools])
 
        if self.district.sfa_certified:
            return {
                "low": eligible_breakfast_low * (bfast_re + .06) + eligible_lunch_low * (lunch_re + 0.06),
                "high": eligible_breakfast_high * (bfast_re + .06) + eligible_lunch_high * (lunch_re + 0.06)
            }
        else:
            return {
                "low": eligible_breakfast_low * bfast_re + eligible_lunch_low * lunch_re,
                "high": eligible_breakfast_high * bfast_re + eligible_lunch_high * lunch_re
            }

    def __repr__(self):
        if self.isp == None:
            return "%s / %s -- no students enrolled --" % (self.district, self.name)
        return "%s / %s ISP=%0.0f%% ENROLLED=%i FREE_RATE=%0.2f%%" % \
            (self.district,self.name,self.isp*100, self.total_enrolled, self.free_rate*100)
    
    def as_dict(self):
        return {
            "name": self.name,
            "school_codes": list(self.school_codes),
            "isp": self.isp,
            "free_rate": self.free_rate,
            "paid_rate": self.paid_rate,
            "total_eligible": self.total_eligible,
            "total_enrolled": self.total_enrolled,
            "covered_students": self.covered_students,
        } 

class CEPDistrict(object):
    def __init__(self,name,code,sfa_certified=False):
        self.name = name
        self.code = code
        self._schools = [] 
        self.groups = []
        self.sfa_certified = sfa_certified # TODO provide as input
        self.anticipated_rate_change = 0.02
        self.strategies = []
        self.best_strategy = None

        # **Note** there might be a nuance with free_bfast. Ask Heidi
        # make this an input or parameter; will change per district and year-over-year
        self.fed_reimbursement_rates = {'free_lunch': 3.31, 'paid_lunch': 0.31, 'free_bfast': 2.14, 'paid_bfast': 0.31}

    def __lt__(self,other_district):
        return self.total_enrolled < other_district.total_enrolled

    def add_school(self,school):
        self._schools.append(school)

    @property
    def schools(self):
        return [ s for s in self._schools if s.active ]

    def run_strategies(self):
        for s in self.strategies:
            s.create_groups(self)

    def evaluate_strategies(self):
        best = None
        for s in self.strategies:
            assert(s.groups != None)
            if best == None or s.students_covered > best.students_covered: # TODO evaluate on total reimbursement, not students_covered
                best = s
        self.best_strategy = best

    def __eq__(self,other_district):
        return self.code == other_district.code


    @property
    def total_enrolled(self): 
        return sum([s.total_enrolled for s in self.schools])

    @property
    def overall_isp(self): 
        return sum([s.total_eligible for s in self.schools])/self.total_enrolled

    @property
    def students_covered(self):
        return self.best_strategy.students_covered

    @property
    def percent_covered(self):
        return float(self.best_strategy.students_covered)/self.total_enrolled

    def as_dict(self,include_schools=True,include_strategies=True):
        result = {
            "name": self.name,
            "code": self.code, 
            "total_enrolled": self.total_enrolled,
            "overall_isp": self.overall_isp,
            "school_count": len(self.schools),
        }
        if include_schools:
            result["schools"] = [ s.as_dict() for s in self._schools]
        if include_strategies and self.strategies:
            result["strategies"] = [ s.as_dict() for s in self.strategies ]
            result["best_index"] = self.strategies.index(self.best_strategy)
        return result

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

    @property
    def total_enrolled(self):
        return sum([g.total_enrolled for g in self.groups])

    @property
    def isp(self):
        if self.total_enrolled == 0:
            return 0
        return self.students_covered/self.total_enrolled

    @property
    def free_rate(self):
        return self.isp * FREE_RATE_MULTIPLIER
    
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

    def reimbursment(self):
        # TODO differentiate hi/low
        group_reimbursements  = [g.est_reimbursement() for g in self.groups]
        return {
            'low_end_estimate': sum([g["low"] for g in group_reimbursements]),
            'high_end_estimate': sum([g["high"] for g in group_reimbursements])
        }

    def as_dict(self):
        return {
            "name": self.name,
            "groups": [g.as_dict() for g in self.groups],
            "isp":  self.isp,
            "total_enrolled": self.total_enrolled,
            "free_rate": isp_to_free_rate(self.isp),
            "total_eligible": self.students_covered,
            "reimbursement": self.reimbursment(),
            'basis':  'estimated',
            #"This estimate of reimbursement revenue is based off school meal participation rates from a sample"
            #         "of schools current enrolled in CEP.  Your district's revenue will likely be between the high and"
            #         "low estimates but might be out side of this range.  This is especially likely if your district has"
            #         "few schools  We can provide a more accurate estimate with your district's specific meals data."
        }  # low , high, basis

