from .base import BaseCEPDistrict,CEPGroup

class BinCEPDistrict(BaseCEPDistrict):
    ''' Grouping strategy is to compute every possible partition

    * This follows with https://en.wikipedia.org/wiki/Partition_of_a_set
    * We first calculate the Bell Number, as we don't want to break your computer
    https://en.wikipedia.org/wiki/Bell_number  

      '''
    def create_groups(self):
        raise NotImplemented("Some more reading is required..") 
        # For every possible partition:
        #   generate it
        #   if best so far, keep
        # cont.
        # Note compute best as total ISP (possibly later look at reimbursement level)

