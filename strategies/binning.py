from .base import BaseCEPStrategy,CEPGroup

class BinCEPStrategy(BaseCEPStrategy):
    ''' Grouping strategy is to bin high ISP schools, grouping to maximize average.

    See this SO answer for example:
    https://stackoverflow.com/questions/33334961/algorithm-group-sort-list-to-maximize-minimum-average-group-value/33336017#33336017

    Parameters: ?isp_width=0.02 (where 0.02 is 2%)

    *Note possibly not optimal as we are maximizing for a threshold, not the overall average.
      '''
    name="Binning"
    def create_groups(self,district):
        self.groups = []
        if len(district.schools) == 0: return

        # group all schools with ISP over 62.5%
        THRESHOLD = 0.625
        high_isp = [ s for s in district.schools if s.isp > THRESHOLD ]
        the_rest = [ s for s in district.schools if s.isp <= THRESHOLD ]
        the_rest.sort(key = lambda school: school.isp) # lowest isp first, we will be popping the tail

        # CONSIDER should we even be looking at isp vs re-calculating aggregate isp?
        def new_isp(x): 
            if len(x):
                total_enrolled = sum([s.total_enrolled for s in x])
                total_eligible = sum([s.total_eligible for s in x])
                if total_enrolled: return total_eligible/total_enrolled
            return 0

        def fill_up(target,threshold): 
            while len(the_rest):
                target.append(the_rest.pop()) # take the tail
                if new_isp(target) < threshold: break

        # First create a group with all ISPs over 62.5
        threshold = THRESHOLD

        fill_up(high_isp,threshold)
        self.groups.append( CEPGroup(
            district,
            "High-ISP",
            high_isp
        ))

        # the width of our bins going down
        isp_width = float(self.params.get("isp_width",0.02))
        #print("Binning with isp width of ",isp_width) 
        # TODO to match ,need to split by cumulative ISP, not individual isp..

        # Then gradually reduce the threshold in steps (of size isp_width), filling up each group
        # until the bin is just above the threshold

        while len(the_rest) > 0 and threshold >= self.params.get("isp_threshold",self.isp_threshold):
            threshold = the_rest[-1].isp 
            #print("T",threshold)
            threshold -=  isp_width
            g = []
            fill_up(g,threshold)
            self.groups.append(
                CEPGroup(   
                    district,
                    "ISP-%0.2f_to_%0.2f" % (threshold,isp_width+threshold),
                    g,
                    self.isp_threshold
                )
            )
    
        if len(the_rest):
            self.groups.append(
                CEPGroup(
                    district,
                    "The-Rest-Low-ISP",
                    the_rest,
                    self.isp_threshold,
                )
            )
   


