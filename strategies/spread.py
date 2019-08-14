from .base import BaseCEPStrategy,CEPGroup

class SpreadCEPStrategy(BaseCEPStrategy):
    name="Spread"
    def create_groups(self,district):
        # TODO implement a "spread" algorithm where we try to spread out the highest ISP schools
        # and slowly bring them down to 62.5% aggregate ISP as we add in the slightly lower ISP schools
        self.groups = [
            CEPGroup(district,school.name,[school])
            for school in district.schools
        ]
   


