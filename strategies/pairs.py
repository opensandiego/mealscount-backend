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

        high_isp,low_isp = [],[]
        for school in schools:
            if school.isp > 0.625:
                high_isp.append(school)
            else:
                low_isp.append(school)
        low_isp.sort(key = lambda s: s.total_enrolled, reverse=True)

        # Walk through the highest isp groups and make them have their own school
        for school in high_isp:
            found_match = False
            for low_school in low_isp:
                g = CEPGroup(district,"Group-of-%s"%school.code,[school,low_school])
                if g.isp > 0.625:
                    found_match = True
                    self.groups.append(g)
                    low_isp.remove(low_school)
                    break
            if not found_match:
                g = CEPGroup(district,"Singleton-Group-of-%s"%school.code,[school])

        if len(low_isp) > 0:
            self.groups.append(CEPGroup(district,"Remainder", low_isp))

