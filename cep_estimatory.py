       
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

        self.breakfast_served = self.total_enrolled  # TODO provide as input
        self.lunch_served = self.total_enrolled #TODO provide as input

        if self.total_enrolled == 0:
            sel.isp  = self.free_rate = self.paid_rate = 0
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
        # IF(E11*1.6>=1,1,IF(E11<0.3,0,E11*1.6))
        self.free_rate = self.isp * 1.6
        if self.isp * 1.6 > 1:
            self.free_rate = 1
        elif self.isp < 0.3:
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

class BaseCEPDistrict(object):
    def __init__(self,name,code,sfa_certified=False,anticipated_rate_change=0.02):
        self.name = name
        self.code = code
        self.schools = [] 
        self.groups = []
        self.sfa_certified = sfa_certified # TODO provide as input
        self.anticipated_rate_change = 0.02

    def create_groups(self):
        raise NotImplemented("Override this with the grouping strategy")

    @property
    def total_enrolled(self): 
        return sum([s.total_enrolled for s in self.schools])

    @property
    def students_covered(self):
        return sum([g.covered_students for g in self.groups])

    @property
    def percent_covered(self):
        return float(self.students_covered)/self.total_enrolled

    def reimbursement(self):
        # TODO calculate reimbursement amount
        raise NotImplemented("Need to calculate based on CEP Estimator")


class OneToOneCEPDistrict(BaseCEPDistrict):
    def create_groups(self):
        self.groups = [
            CEPGroup(school.district,school.name,[school])
            for school in self.schools
        ] 

# MC Algo V2 - Appears to follow this strategy
# https://stackoverflow.com/questions/33334961/algorithm-group-sort-list-to-maximize-minimum-average-group-value/33336017#33336017
# HOWEVER, we are optimizing to a threshold, not the overall minimum, so this does not necessarily apply (TBD)
class BinCEPDistrict(BaseCEPDistrict):
    def create_groups(self):
        # group all schools with ISP over 62.5%
        threshold = 0.625
        high_isp = [ s for s in self.schools if s.isp > threshold ]
        the_rest = [ s for s in self.schools if s.isp <= threshold ]         
        the_rest.sort(key="isp") # lowest isp first

        avg_sp = lambda x: sum([s.isp for s in x])/len(x)
        
        while avg_isp(high_isp) >= threshold:
            high_isp.append(the_rest.pop()) # take the tail
        the_rest.append(high_isp.pop()) # put the one back that was over the threshold

        # TODO
        # then bin out the_rest
        isp_width = 0.05
        t = threshold # start with bin at 62.5 - isp_width
        t,bins = t-isp_width,[]

        #TODO test against original algo

# Uses the original algo 
class AlgoV2CEPDistrict(BaseCEPDistrict):
    def create_groups(self):
        from sandbox.mc_algorithm_v2 import mcAlgorithmV2,CEPSchoolGroupGenerator
        from sandbox import config_parser
        from sandbox import backend_utils
        import pandas
        df = pandas.DataFrame([s.as_dict() for s in self.schools])
        class tmpSchoolDistInput(backend_utils.mcSchoolDistInput):
            def to_frame(self): return self.d_df  
            def metadata(self): return {"lea":"tmp","academic_year":"tmp"}
        data = tmpSchoolDistInput()
        data.d_df = df
        cfg = config_parser.mcModelConfig("sandbox/config.json")
        strategy = mcAlgorithmV2()
        grouper = CEPSchoolGroupGenerator(cfg, strategy)
        results = grouper.get_groups(data, "json")
        groups = [g for g in results["school_groups"]["group_summaries"]]
        isp_width = results["model_params"]["isp_width"]

        for g in groups:
            schools = [s for s in self.schools if s.code in g["schools"]]
            self.groups.append(CEPGroup(self.name,"group-%s"%g["group"],schools))


#### MAIN ####
if __name__=="__main__":
    # Import csv
    import csv
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument('cupc_csv_file',type=str,
                        help='''Path of cupc file as csv with modified columns: 
    Required columns:
    District Name,School Name,total_enrolled,foster,migrant,homeless,direct_cert
    **Note** total_enrolled,foster,migrant,homeless,direct_cert renamed from CUPC export
    ''')
    parser.add_argument('--district',type=str,default=None,
                        help='Specific district code to run (if none, all in csv are run)')
    
    args = parser.parse_args()

    schools = [r for r in csv.DictReader(open(args.cupc_csv_file)) if i(r['total_enrolled']) > 0]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
    DistrictClass = AlgoV2CEPDistrict

    districts = {}
    for row in schools:
        if args.district and row["District Code"] != args.district: continue
        school = CEPSchool(row)
        districts.setdefault(school.district,DistrictClass(school.district,school.district_code))
        districts[school.district].schools.append(school)

    for d in districts:
        district = districts[d]
        if args.district and district.code != args.district: continue
        print("Processing District ",district.name)
        district.create_groups()
        if district.total_enrolled == 0:
            print("%s -- no students enrolled --" % district.name)
            continue
        print( "%s: covered students: %i/%i %0.0f%%" % \
            (district.name,district.students_covered,district.total_enrolled,(district.percent_covered*100) )
        )
    print("%i Schools Processed for %i districts" % (len(schools),len(districts)) )



