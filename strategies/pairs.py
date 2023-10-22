from .base import BaseCEPStrategy,CEPGroup

class PairsCEPStrategy(BaseCEPStrategy):
    name="Pairs"
    def create_groups(self,district):
        # TODO implement a "pairing" algorithm where we try pair the high isp schools with a partner that is
        # under the threshold
        self.groups = []
        
        # First we divide up the schools by ISP, those already fully qualified
        # vs those not fully qualified, into two presorted lists desc by isp
        schools = district.schools
        schools.sort(key = lambda s: s.isp,reverse=True)

        # First we pair up the fully covered isp schools (over 62.5%)
        high_isp,low_isp = self.split_on_threshold(schools,0.625)
        self.create_matches(high_isp,low_isp,0.625,district)

        # then with the remaining low_isp schools, we pair up partial coverage (over 40%)
        high_isp,low_isp = self.split_on_threshold(low_isp,self.isp_threshold)
        self.create_matches(high_isp,low_isp,self.isp_threshold,district)

        # Finally, anything below is not CEP Eligible
        if len(low_isp) > 0:
            self.groups.append(CEPGroup(district,"Not CEP Eligible", low_isp,self.isp_threshold))

        assert sum([len(g.schools) for g in self.groups])  == len(schools)

    def split_on_threshold(self,schools,threshold):
        high_isp,low_isp = [],[]
        for school in schools:
            if school.isp > threshold:
                high_isp.append(school) # Separate out schools with full coverage
            else:
                low_isp.append(school)
        low_isp.sort(key = lambda s: s.total_enrolled, reverse=True)
        return high_isp,low_isp

    def create_matches(self,high_isp,low_isp,threshold,district):
    # Walk through the highest isp groups and make them have their own school
        for school in high_isp:
            found_match = False
            for low_school in low_isp:
                g = CEPGroup(district,"Group-of-%s"%school.code,[school,low_school],self.isp_threshold)
                if g.isp > threshold:
                    found_match = True
                    self.groups.append(g)
                    low_isp.remove(low_school)
                    break
            if not found_match:
                g = CEPGroup(district,"Singleton-Group-of-%s"%school.code,[school],self.isp_threshold)
                self.groups.append(g)

