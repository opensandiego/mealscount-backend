from . import STRATEGIES
import unittest
from .base import CEPDistrict,CEPSchool

SCHOOL_DATA_COLS = ["District Code","School Name","School Code",\
                    "foster","homeless","migrant","direct_cert",\
                    "frpm","total_enrolled"]

class CEPTestMixin(object):
    '''Mixin for reusable school / district building code for tests''' 
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
        return basic
 
class CEPTestCase(unittest.TestCase,CEPTestMixin):
    '''Tests basic python data model (CEPSchool,CEPDistrict,CEPGroup)'''

    def test_district(self):
        district = self.create_default_districts()
        self.assertEqual( district.total_enrolled, sum([s.total_enrolled for s in district.schools]))
        self.assertEqual(
            district.overall_isp,
            (850+625+400+250)/4000.0
        )

    def test_school(self):
        s = CEPSchool( {
            "District Name":"Test District",
            "District Code":"TEST-D",
            "School Name":"Test School",
            "School Code": "TEST-S",
            "total_enrolled": 1000,
            "direct_cert": 100,
            "foster": 100,
            "homeless": 100,
            "migrant": 100,
        }) 
        self.assertEqual(s.total_eligible,100) # We actually are now using direct_cert for baseline eligible
        self.assertEqual(s.isp,0.4)

    def test_group(self):
        pass


class StrategyTestCase(unittest.TestCase,CEPTestMixin):
    '''Runs through all registerd strategies and tests them. You can add custom per-strategy test
    cases by setting up a test_districts data member
    '''
    def setUp(self):
        self.test_districts = []
        self.create_default_districts()
        self.test_districts.append(self.create_default_districts())

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




