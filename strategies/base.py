from abc import ABC,abstractmethod
from enum import Enum

# Shortcut to deal with commas in integers from csv
def i(x):
    if type(x) != str: return int(x)
    if x.strip() == '': return 0
    try:
        return int(float(x.replace(',','')))
    except ValueError:
        return 0

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
        # TODO move these explicit column names to 
        # separate method, and let us initialize a bit more simply
        self.name = data.get('School Name',data.get('school_name'))
        self.code = data.get('School Code',data.get('school_code',data.get('school_name')))
        self.school_type = data.get('School Type','n/a')
        self.active = data.get("include_in_mealscount","true").lower() == "true"
        self.foster = i(data.get('foster',0))
        self.homeless = i(data.get('homeless',0))
        self.migrant = i(data.get('migrant',0))
        self.direct_cert = i(data.get('direct_cert',0))
        self.frpm = i(data.get('unduplicated_frpm',0))
        self.total_eligible = i(data.get('total_eligible',self.direct_cert ))
        self.severe_need = bool(data.get('severe_need',False))

        # NOTE based upon California data, total eligible is "direct_cert", but still in progress!
        #i(data.get('unduplicated_frpm',0)) # (self.foster + self.homeless + self.migrant + self.direct_cert)
        self.total_enrolled = i(data['total_enrolled'])
        if self.total_eligible > self.total_enrolled:
            self.total_eligible = self.total_enrolled

        if data.get("daily_breakfast_served",""):
            self.bfast_served = int(float(data.get("daily_breakfast_served") or 0))
            self.lunch_served = int(float(data.get("daily_lunch_served") or 0))
        else:
            self.bfast_served = 0 
            self.lunch_served = 0 

        if self.total_enrolled == 0:
            self.isp  = self.free_rate = self.paid_rate = 0
        else:
            self.isp = round(self.total_eligible / float(self.total_enrolled), 4)

    def set_rates(self,district):
        self.rates = CEPRate(district.state,district.sfa_certified,district.hhfka_sixty,self.severe_need)

    def __repr__(self):
        return "%s %s" % (self.name,self.code)

    def as_dict(self,district=None):
        obj = {
            'school_code': self.code,
            'school_name': self.name,
            'school_type': self.school_type,
            'total_enrolled': self.total_enrolled,
            "total_eligible": self.total_eligible,
            "daily_breakfast_served": self.bfast_served,
            "daily_lunch_served": self.lunch_served,
            'isp': self.isp,
            'active': self.active,
            'severe_need': self.severe_need,
        }
        if district:
            self.set_rates(district)
            obj["rates"] = self.rates.as_dict()
        return obj

class CEPGroup(object):
    def __init__(self,district,group_name,schools):
        # Expected Columns:
        # district,school,total_enrolled,frpm,foster,homeless,migrant,direct_cert

        self.district = district
        self.name = group_name
        self.total_eligible,self.total_enrolled = 0,0
        self.schools = schools
        self.calculate()

    def calculate(self):
        # Step 1 - calculate eligible students
        self.school_codes = set([s.code for s in self.schools])

        self.total_eligible,self.total_enrolled = 0,0
        for school in self.schools:
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
        
        self.school_reimbursements = set([ (s.code,self.school_reimbursement(s)) for s in self.schools])

    @property
    def covered_students(self):
        ''' number of students qualified for free rate'''
        return round(self.free_rate * self.total_enrolled,0)

    @property
    def cep_eligible(self):
        return self.free_rate > 0

    @property
    def daily_lunch_served(self):
        return sum([s.lunch_served for s in self.schools])

    @property
    def daily_breakfast_served(self):
        return sum([s.bfast_served for s in self.schools])

    @property
    def free_daily_breakfast_served(self): return self.daily_breakfast_served * self.free_rate
    @property
    def free_daily_lunch_served(self): return self.daily_lunch_served * self.free_rate
    @property
    def paid_daily_breakfast_served(self): return self.daily_breakfast_served * self.paid_rate
    @property
    def paid_daily_lunch_served(self): return self.daily_lunch_served * self.paid_rate

    def school_state_reimbursement(self,school):
        return 0  # TODO calculate the state reimbursement based on this school and the district's state funding class

    def est_state_reimbursement(self):
        return 0 # Todo aggregate state reimbursement

    def school_reimbursement(self,school): 
        ''' Calculate a school's reimbursement given this group's isp free_rate and paid_rate percentages'''
        if not self.cep_eligible: return 0
        school.set_rates(self.district)
        result = school.bfast_served * school.rates.free_breakfast_rate * self.free_rate + \
               school.bfast_served * school.rates.paid_breakfast_rate * self.paid_rate + \
               school.lunch_served * school.rates.free_lunch_rate * self.free_rate + \
               school.lunch_served * school.rates.paid_lunch_rate * self.paid_rate
        if self.district.sfa_certified:
            result += school.lunch_served * 0.07
        return round(result,2)

    def est_reimbursement(self):
        '''basic estimate for daily reimbursement based on the given meal participation estimates
        '''
        return sum([self.school_reimbursement(s) for s in self.schools])

    def __repr__(self):
        if self.isp == None:
            return "%s / %s -- no students enrolled --" % (self.district, self.name)
        return "%s / %s ISP=%0.0f%% ENROLLED=%i FREE_RATE=%0.2f%%" % \
            (self.district,self.name,self.isp*100, self.total_enrolled, self.free_rate*100)
    
    def as_dict(self):
        return {
            "name": self.name,
            "school_codes": list(self.school_codes),
            "school_reimbursements": list(self.school_reimbursements),
            "isp": self.isp,
            "free_rate": self.free_rate,
            "paid_rate": self.paid_rate,
            "total_eligible": self.total_eligible,
            "total_enrolled": self.total_enrolled,
            "free_rate_students": self.covered_students,
            "paid_rate_students": int(self.paid_rate * self.total_enrolled),
            "cep_eligible": self.cep_eligible,
            "est_reimbursement": self.est_reimbursement(),
            "daily_breakfast_served": self.daily_breakfast_served,
            "daily_lunch_served": self.daily_lunch_served,
        } 

class CEPDistrict(object):
    def __init__(self,name,code,sfa_certified=True,hhfka_sixty="more",state="ca"):
        self.name = name
        self.code = code
        self._schools = [] 
        self.groups = []
        self.sfa_certified = sfa_certified # TODO provide as input
        self.hhfka_sixty = hhfka_sixty # Expect "less","more" or "max"
        assert( hhfka_sixty in ("less","more","max") ) 
        self.anticipated_rate_change = 0.02
        self.strategies = []
        self.best_strategy = None
        self.state = state

    def __lt__(self,other_district):
        return self.total_enrolled < other_district.total_enrolled

    def add_school(self,school):
        self._schools.append(school)

    @property
    def schools(self):
        return [ s for s in self._schools if s.active ]

    def run_strategies(self):
        if not self.schools: 
            return
        for s in self.strategies:
            s.create_groups(self)

    def evaluate_strategies(self,evaluate_by="reimbursement"):
        best = None
        for s in self.strategies:
            if s.groups == None:
                continue
            # TODO evaluate on total reimbursement, not students_covered
            if evaluate_by == "reimbursement":
                if best == None or s.reimbursement > best.reimbursement: 
                    best = s
            elif evaluate_by == "coverage":
                if best == None or s.students_covered > best.students_covered: 
                    best = s
            else:
                raise Exception("Unknown evaluation: %s" % evaluate_by)
        self.best_strategy = best

    def __eq__(self,other_district):
        if isinstance(other_district,CEPDistrict):
            return self.code == other_district.code
        return False


    @property
    def total_enrolled(self): 
        return sum([s.total_enrolled for s in self.schools])

    @property
    def overall_isp(self): 
        if not self.total_enrolled: return 0
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
            "sfa_certified": self.sfa_certified,
            "hhfka_sixty": self.hhfka_sixty,
            "best_strategy": self.best_strategy and self.best_strategy.name or None,
            "est_reimbursement": self.best_strategy and self.best_strategy.reimbursement or 0.0,
        }
        if include_schools:
            result["schools"] = [ s.as_dict(self) for s in self._schools]
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
        self.groups = []
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

    @property
    def reimbursement(self):
        r = sum([g.est_reimbursement() for g in self.groups])
        return r

    def school_reimbursement(self,school):
        for g in self.groups:
            if school in g.schools:
                return g.school_reimbursement(school)
        return 0

    def as_dict(self):
        return {
            "name": self.name,
            "groups": self.groups and [g.as_dict() for g in self.groups] or [],
            "isp":  self.isp,
            "total_enrolled": self.total_enrolled,
            "free_rate": isp_to_free_rate(self.isp),
            "total_eligible": self.students_covered,
            "reimbursement": self.reimbursement,
            'basis':  'estimated',
            #"This estimate of reimbursement revenue is based off school meal participation rates from a sample"
            #         "of schools current enrolled in CEP.  Your district's revenue will likely be between the high and"
            #         "low estimates but might be out side of this range.  This is especially likely if your district has"
            #         "few schools  We can provide a more accurate estimate with your district's specific meals data."
        }  # low , high, basis


class AbstractStateFunding(object):
    def get_funding(self,school):
        return 0

# Rates Updated for 2021-2022
class CEPRate(object):
    def __init__(self,state,sfa_certified,hhfka_sixty,severe_need):
        state = state.upper()
        ## ALASKA ##
        if state == "AK":
            # Lunch
            if hhfka_sixty == "less":
                self.free_lunch_rate = 5.94
                self.paid_lunch_rate = 0.57
            elif hhfka_sixty == "more":
                self.free_lunch_rate = 5.96
                self.paid_lunch_rate = 0.59
            else:  #max
                self.free_lunch_rate = 5.94
                self.paid_lunch_rate = 0.65
            # Breakfast 
            if not severe_need:
                self.free_breakfast_rate = 3.15
                self.paid_breakfast_rate = 0.50
            else:
                self.free_breakfast_rate = 3.78 
                self.paid_breakfast_rate = 0.50

        ## Puerto Rico, Guam, Hawaii, Virgin Islands ##
        elif state in ("PR","GM","HI","VI"):
            # Lunch
            if hhfka_sixty == "less":
                self.free_lunch_rate = 4.28
                self.paid_lunch_rate = 0.41
            elif hhfka_sixty == "more":
                self.free_lunch_rate = 4.30
                self.paid_lunch_rate = 0.43
            else:  #max
                self.free_lunch_rate = 4.30
                self.paid_lunch_rate = 0.47
            # Breakfast 
            if not severe_need:
                self.free_breakfast_rate = 2.29 
                self.paid_breakfast_rate = 0.38
            else:
                self.free_breakfast_rate = 2.74 
                self.paid_breakfast_rate = 0.38

        ## Contiguous 48 ##
        else:
            # Lunch
            if hhfka_sixty == "less":
                self.free_lunch_rate = 3.66
                self.paid_lunch_rate = 0.35
            elif hhfka_sixty == "more":
                self.free_lunch_rate = 3.68
                self.paid_lunch_rate = 0.37
            else:  #max
                self.free_lunch_rate = 3.68
                self.paid_lunch_rate = 0.41
            # Breakfast 
            if not severe_need:
                self.free_breakfast_rate = 1.97 
                self.paid_breakfast_rate = 0.33
            else:
                self.free_breakfast_rate = 2.35 
                self.paid_breakfast_rate = 0.33

    def as_dict(self):
        return {
            "free_bfast": self.free_breakfast_rate,
            "paid_bfast": self.paid_breakfast_rate,
            "free_lunch": self.free_lunch_rate,
            "paid_lunch": self.paid_lunch_rate,
        }