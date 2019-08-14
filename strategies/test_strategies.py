from . import STRATEGIES
import unittest
from .base import CEPDistrict,CEPSchool

SCHOOL_DATA_COLS = ["District Code","School Name","School Code",\
                    "foster","homeless","migrant","direct_cert",\
                    "frpm","total_enrolled"]

class StrategyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_districts = []
        self.create_default_districts()

    def mk_school(self,district,code,isp,total_enrolled):
        return CEPSchool({
            "District Name":district.name,
            "District Code":district.code,
            "School Name":"School %s" % code,
            "School Code":"BASIC-%s" % code,
            "direct_cert": isp*total_enrolled,
            "total_enrolled": total_enrolled,
        })

    def create_default_districts(self):
        basic = CEPDistrict(name="Basic District",code="BASIC")
        basic.schools.append(self.mk_school(basic,"A",0.85,1000))
        basic.schools.append(self.mk_school(basic,"A",0.625,1000))
        basic.schools.append(self.mk_school(basic,"B",0.40,1000))
        basic.schools.append(self.mk_school(basic,"C",0.25,1000))
        self.test_districts.append(basic)

    def test_strategies(self):
        for strategy_class in STRATEGIES.values():
            if hasattr(strategy_class,"test_districts"):
                test_districts = strategy_class.test_data 
            else:
                test_districts = self.test_districts

            for d in test_districts:
                d.strategies = [strategy_class()]
                d.run_strategies()
                for s in d.strategies: 
                    # Verify our strategy gave us groups of schools totalling the total number
                    # of schools
                    self.assertEqual(sum([len(g.schools) for g in s.groups]),len(d.schools))

            # TODO how does a strategy define its expected result?
