from .base import BaseCEPDistrict,CEPGroup

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

