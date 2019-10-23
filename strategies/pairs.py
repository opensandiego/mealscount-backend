from .base import BaseCEPStrategy,CEPGroup

class PairsCEPStrategy(BaseCEPStrategy):
    name="Pairs"
    def create_groups(self,district):
        # TODO implement a "pairing" algorithm where we try pair the high isp schools with a partner that is
        # under the threshold
        self.groups = []
        
        # First we divide up the schools by ISP, those already fully qualified
        # vs those not fully qualified, into two presorted lists desc by isp
        district.schools.sort(key = lambda s: s.isp,reverse=True)
        high_isp,low_isp = [],[]
        for school in district.schools:
            if school.isp > 0.625:
                high_isp.append(school)
            else:
                low_isp.append(school)

        # Walk through the highest isp groups and make them have their own school
        for school in high_isp:
            # Create a new group
            g = CEPGroup(district,"Group-of-%s"%school.code,[school])
            # Add in the highest isp schools from low_isp, until we just cross the threshold
            while g.isp > 0.625 and len(low_isp) > 0:
                next_school = low_isp.pop(0)
                bigger_g = CEPGroup(district,"Group-of-%s"%school.code,g.schools + [next_school])
                # By adding the next school from low_isp, if we have crossed the threshold
                if bigger_g.isp < 0.625:
                    # put the school back on low_isp, and break
                    low_isp.insert(0,next_school)
                    break
                # otherwise g is now bigger_g
                g = bigger_g
            # And step back and add this to our final groups
            self.groups.append(g)

        if len(low_isp) > 0:
            self.groups.append(CEPGroup(district,"Remainder", low_isp))

