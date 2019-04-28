import csv
import click 
import tabulate

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
        # IF(E11*1.6>=1,1,IF(E11<0.3,0,E11*1.6))
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

class BaseCEPDistrict(object):
    def __init__(self,name,code,sfa_certified=False,anticipated_rate_change=0.02):
        self.name = name
        self.code = code
        self.schools = [] 
        self.groups = []
        self.sfa_certified = sfa_certified # TODO provide as input
        self.anticipated_rate_change = 0.02

    def __lt__(self,other_district):
        return self.total_enrolled < other_district.total_enrolled


    def __eq__(self,other_district):
        return self.code == other_district.code

    def matches_grouping_of(self,other_district):
        ''' Compare districts by looking to see if their grouped school codes are identical'''
        if len(self.groups) == 0 or len(other_district.groups) == 0:
            raise ValueError("Please run create_groups before comparing districts: %s (%i) = %s (%i)" %
                   (self.name,len(self.groups), other_district.name, len(other_district.groups) ) )

        # Must be the same district code
        if self.code != other_district.code: return False 

        # Then walk through our groups, and look for an identical group in the other district
        for g in self.groups:
            found = False
            for og in other_district.groups:
                if g.school_codes == og.school_codes: 
                    found = True  
                    break
            # If we do not find a matching group, these districts do not have the same grouping
            if not found: return False
        return True

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
    ''' Grouping Strategy is each school has its own group '''
    def create_groups(self):
        self.groups = [
            CEPGroup(school.district,school.name,[school])
            for school in self.schools
        ] 

class OneGroupCEPDistrict(BaseCEPDistrict):
    ''' Grouping Stretegy is creates a single group of all schools in the district ''' 
    def create_groups(self):
        self.groups = [
            CEPGroup(self.name,"%s - Consolidated" % self.name,self.schools)
        ]

class BinCEPDistrict(BaseCEPDistrict):
    ''' Grouping strategy is to bin high ISP schools, grouping to maximize average.

    See this SO answer for example:
    https://stackoverflow.com/questions/33334961/algorithm-group-sort-list-to-maximize-minimum-average-group-value/33336017#33336017

    *Note possibly not optimal as we are maximizing for a threshold, not the overall average.
      '''
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
    ''' Wraps MealsCount "Algo v2", which follows the binning strategy, for comparison '''

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

STRATEGIES = {
    "OneToOne":OneToOneCEPDistrict,
    "OneGroup":OneGroupCEPDistrict,
    "Bin":BinCEPDistrict,
    "AlgoV2":AlgoV2CEPDistrict,
}

#### CLI ####

def parse_districts(school_data,DistrictClass=OneToOneCEPDistrict):
    districts = {}
    for row in school_data:
        school = CEPSchool(row)
        districts.setdefault(school.district,DistrictClass(school.district,school.district_code))
        districts[school.district].schools.append(school)
    districts = list(districts.values())
    districts.sort()
    return districts

@click.command()
@click.option("--target_district",default=None,help="Specific district code to run")
@click.option("--strategy",default="OneToOne",help="Grouping strategy")
@click.option("--baseline",default=None,help="Baseline Grouping strategy to compare")
@click.argument("cupc_csv_file",nargs=1)
def cli(cupc_csv_file,baseline=None,target_district=None,strategy="OneToOne"):
    schools = [r for r in csv.DictReader(open(cupc_csv_file)) if i(r['total_enrolled']) > 0]

    # Reduce to target district if specified
    if target_district != None:
        schools = [s for s in schools if s["District Code"] == target_district]

    # Naive Groupings
    #DistrictClass = OneToOneCEPDistrict
    
    DistrictClass = STRATEGIES[strategy]
    districts = parse_districts(schools,DistrictClass)

    click.secho("\nParsed {:,} schools in {:,} districts representing {:,} students\n".format( 
            len(schools),
            len(districts), 
            sum([i(s["total_enrolled"]) for s in schools]),
         ),
        fg="blue"
    )
    
    # Process target strategy
    with click.progressbar(districts,label='Grouping Districts with %s' % DistrictClass) as bar:
        for district in bar:
            district.create_groups() 
    
    if baseline:
        BaselineDistrictClass = STRATEGIES[baseline]
        baseline_districts = parse_districts(schools,BaselineDistrictClass)
        with click.progressbar(baseline_districts,label='Grouping District Baseline with %s' % BaselineDistrictClass) as bar:
            for district in bar:
                district.create_groups() 
        
        results = [] 
        for d1 in districts:
            d0 = [d for d in baseline_districts if d == d1][0]
            results.append([
                d1.code,
                d1.name[:64],
                d1.matches_grouping_of(d0) and "*" or "",
                float(d0.total_enrolled),
                float(d1.students_covered) - float(d0.students_covered),
                (d0.percent_covered*100),
                (d1.percent_covered*100),
            ])

        print( tabulate.tabulate(
            results,
            [   'code',
                'district',
                'same groups',
                'total enrolled',
                'change in students covered',
                'base % covered',
                'opt % covered',
            ],
            tablefmt="pipe",
            floatfmt=("","","",",.0f","+,.0f",",.0f",".0f",".0f"),
        ))
    else:       
        print( tabulate.tabulate(
            [ (
                district.code,
                district.name[:64],
                float(district.students_covered),
                float(district.total_enrolled),
                (district.percent_covered*100) ) for district in districts ],
            ['code','district','students covered','total enrolled','% covered'],
            tablefmt="pipe",
            floatfmt=("","",",.0f",",.0f",".0f"),
        ))

    click.secho(    "{:,} Schools Processed for {:,} districts".format(len(schools),len(districts)) ,
                    fg="blue", bold=True )
    click.secho(DistrictClass.__doc__)


if __name__ == '__main__':
    cli()    

