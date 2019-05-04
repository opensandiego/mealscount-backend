from .base import BaseCEPStrategy,CEPGroup
import sandbox
from sandbox.mc_algorithm_v2 import mcAlgorithmV2,CEPSchoolGroupGenerator
from sandbox import config_parser
from sandbox import backend_utils
import os.path
import pandas

# Uses the original algo 
class AlgoV2CEPStrategy(BaseCEPStrategy):
    ''' Wraps MealsCount "Algo v2", which follows the binning strategy, for comparison '''
    name="AlgoV2"
    def create_groups(self,district):
        self.groups = []
        df = pandas.DataFrame([s.as_dict() for s in district.schools])
        class tmpSchoolDistInput(backend_utils.mcSchoolDistInput):
            def to_frame(self): return self.d_df  
            def metadata(self): return {"lea":"tmp","academic_year":"tmp"}
        data = tmpSchoolDistInput()
        data.d_df = df
        cfg = config_parser.mcModelConfig(os.path.join(os.path.dirname(sandbox.__file__),"config.json"))
        for k in self.params:
            setattr(cfg,k,float(self.params[k]))
        strategy = mcAlgorithmV2()
        grouper = CEPSchoolGroupGenerator(cfg, strategy)
        results = grouper.get_groups(data, "json")
        groups = [g for g in results["school_groups"]["group_summaries"]]
        isp_width = results["model_params"]["isp_width"]

        for g in groups:
            schools = [s for s in district.schools if s.code in g["schools"]]
            self.groups.append(CEPGroup(district,"group-%s"%g["group"],schools))


