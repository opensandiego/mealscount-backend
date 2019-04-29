from .base import BaseCEPDistrict,CEPGroup

class BinCEPDistrict(BaseCEPDistrict):
    ''' Grouping strategy is to bin high ISP schools, grouping to maximize average.

    See this SO answer for example:
    https://stackoverflow.com/questions/33334961/algorithm-group-sort-list-to-maximize-minimum-average-group-value/33336017#33336017

    *Note possibly not optimal as we are maximizing for a threshold, not the overall average.
      '''
    def create_groups(self):
        if len(self.schools) == 0: return

        # group all schools with ISP over 62.5%
        THRESHOLD = 0.625
        high_isp = [ s for s in self.schools if s.isp > THRESHOLD ]
        the_rest = [ s for s in self.schools if s.isp <= THRESHOLD ]
        the_rest.sort(key = lambda school: school.isp) # lowest isp first, we will be popping the tail

        # CONSIDER should we even be looking at isp vs re-calculating aggregate isp?
        new_isp = lambda x: len(x) \
                            and sum([s.total_eligible for s in x])/sum([s.total_enrolled for s in x]) \
                            or 0
       
        def fill_up(target,threshold): 
            while len(the_rest):
                target.append(the_rest.pop()) # take the tail
                if new_isp(target) < threshold: break

        # First create a group with all ISPs over 62.5
        threshold = THRESHOLD

        fill_up(high_isp,threshold)
        self.groups.append( CEPGroup(
            self.name,
            "High-ISP",
            high_isp
        ))

        # the width of our bins going down
        isp_width = float(self.params.get("isp_width",0.02))
        #print("Binning with isp width of ",isp_width) 
        # TODO to match ,need to split by cumulative ISP, not individual isp..

        # Then gradually reduce the threshold in steps (of size isp_width), filling up each group
        # until the bin is just above the threshold

        while len(the_rest) > 0 and threshold >= 0.40:
            threshold = the_rest[-1].isp 
            #print("T",threshold)
            threshold -=  isp_width
            g = []
            fill_up(g,threshold)
            self.groups.append(
                CEPGroup(   
                    self.name,
                    "ISP-%0.2f_to_%0.2f" % (threshold,isp_width+threshold),
                    g
                )
            )
    
        if len(the_rest):
            self.groups.append(
                CEPGroup(
                    self.name,
                    "The-Rest-Low-ISP",
                    the_rest,
                )
            )
   


