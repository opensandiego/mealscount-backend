from . import STRATEGIES
import unittest
from .base import CEPDistrict,CEPSchool,CEPGroup

SCHOOL_DATA_COLS = ["District Code","School Name","School Code",\
                    "foster","homeless","migrant","direct_cert",\
                    "frpm","total_enrolled"]

class CEPTestMixin(object):
    '''Mixin for reusable school / district building code for tests''' 
    def mk_school(self,district,code,isp,total_enrolled,bkfst,lunch):
        return CEPSchool({
            "District Name":district.name,
            "District Code":district.code,
            "School Name":"School %s" % code,
            "School Code":"BASIC-%s" % code,
            "School Type":"Test (Public)",
            "direct_cert": isp*total_enrolled,
            "total_enrolled": total_enrolled,
            "include_in_mealscount": "true",
            "daily_breakfast_served": bkfst,
            "daily_lunch_served": lunch,
        })

    def create_default_districts(self):
        basic = CEPDistrict(name="Basic District",code="BASIC")
        basic.add_school(self.mk_school(basic,"A",0.85,1000,300,500))
        basic.add_school(self.mk_school(basic,"A",0.625,1000,200,600))
        basic.add_school(self.mk_school(basic,"B",0.40,1000,500,500))
        basic.add_school(self.mk_school(basic,"C",0.25,1000,100,400))
        return basic
 
class CEPTestCase(unittest.TestCase,CEPTestMixin):
    '''Tests basic python data model (CEPSchool,CEPDistrict,CEPGroup)'''

    def test_district(self):
        district = self.create_default_districts()
        self.assertEqual(len(district.schools),4)
        self.assertEqual(district.total_enrolled,4000)
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
            "School Type":"Test (Public)",
            "total_enrolled": 1000,
            "direct_cert": 500,
            "daily_breakfast_served":200,
            "daily_lunch_served": 600,
        }) 
        self.assertEqual(s.total_eligible,500) # We actually are now using direct_cert for baseline eligible
        self.assertEqual(s.isp,0.5)

    def test_reimbursement_calculation(self):
        d = CEPDistrict(name="Test",code="TEST")
        s = CEPSchool( {
            "District Name":d.name,
            "District Code":d.code,
            "School Name":"Test School",
            "School Code": "TEST-S",
            "School Type":"Test (Public)",
            "total_enrolled": 1000,
            "direct_cert": 450,
            "daily_breakfast_served":200,
            "daily_lunch_served": 600,
        }) 
        g = CEPGroup(d,"Test Group",[s])

        # Test Against usda-cep-estimator-worksheet 18-19.xlsx
        self.assertEqual(g.isp,0.45)
        # For some reason the float division doens't get us exactly this
        self.assertAlmostEqual(g.free_rate,0.72)
        self.assertAlmostEqual(g.paid_rate,0.28)

    
    def test_group(self):
        district = self.create_default_districts()
        # Create a singular group to test group metrics
        g = CEPGroup(district, "High ISP", district.schools[:2])
        s1,s2 = g.schools
        self.assertEqual(g.isp, (s1.total_eligible + s2.total_eligible) / (s1.total_enrolled + s2.total_enrolled) )
        self.assertEqual(g.free_rate, 1 ) # We are over 1 for isp * 1.6
        self.assertEqual(g.paid_rate, 0 )

        g2 = CEPGroup(district, "Low ISP", district.schools[2:])
        s1,s2 = g2.schools
        self.assertEqual(g2.isp, (s1.total_eligible + s2.total_eligible) / (s1.total_enrolled + s2.total_enrolled) )
        self.assertEqual(g2.free_rate, 0 )
        self.assertEqual(g2.paid_rate, 0 )



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




