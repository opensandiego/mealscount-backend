        
i = lambda x: int(x.replace(',',''))

class CEPSchool(object):
    def __init__(self,data):
        self.district = data['District Name']
        self.name = data['School Name']
        self.total_eligible = (i(data['foster']) + i(data['homeless']) + i(data['migrant']) + i(data['direct_cert']))
        self.total_enrolled = i(data['total_enrolled'])
        if self.total_enrolled == 0:
            sel.isp  = self.free_rate = self.paid_rate = 0
        else:
            self.isp = round(self.total_eligible / float(self.total_enrolled), 4)

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
    def __init__(self,name):
        self.name = name
        self.schools = [] 
        self.groups = None 

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

class OneToOneCEPDistrict(BaseCEPDistrict):
    def create_groups(self):
        self.groups = [
            CEPGroup(school.district,school.name,[school])
            for school in self.schools
        ] 

# Appears to follow this strategy
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

if __name__=="__main__":
    import csv,sys
    schools = [r for r in csv.DictReader(open(sys.argv[1])) if i(r['total_enrolled']) > 0]

    # Naive Groupings
    DistrictClass = OneToOneCEPDistrict
    
    districts = {}
    for row in schools:
        school = CEPSchool(row)
        districts.setdefault(school.district,DistrictClass(school.district))
        districts[school.district].schools.append(school)

    for d in districts:
        district = districts[d]
        district.create_groups()
        if district.total_enrolled == 0:
            print("%s -- no students enrolled --" % district.name)
            continue
        print( "%s: covered students: %i/%i %0.0f%%" % \
            (district.name,district.students_covered,district.total_enrolled,(district.percent_covered*100) )
        )
    print("%i Schools Processed for %i districts" % (len(schools),len(districts)) )



