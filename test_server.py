import unittest
import json
import server
import pytest
import copy
from server import app 

@pytest.fixture
def client(request):
    app.config["TESTING"] = True
    request.cls.client =  app.test_client()

@pytest.mark.usefixtures("client")
class CEPTestCase(unittest.TestCase):
    def test_submit_school(self):
        sobj = oceanside()
        sobj["sfa_certified"] = True
        sobj["hhfka_sixty"] = "less"
        result = self.client.post('/api/districts/optimize/', json = sobj)
        obj = result.json
        self.assertEqual(len(obj["schools"]) ,len(sobj["schools"]))
        self.assertTrue("strategies" in obj)
        self.assertEqual(obj["sfa_certified"],True)
        self.assertEqual(obj["hhfka_sixty"],"less")


    def test_lambda(self):
        from lambda_function import test_run
        import datetime
        sobj = oceanside()
        test_run(sobj,datetime.datetime.now())

    def test_no_district_name(self):
        sobj = oceanside()
        del sobj["name"]
        result = self.client.post('/api/districts/optimize/', json = sobj)

    def test_no_schools(self):
        # empty school list
        sobj = oceanside()
        sobj["schools"] = []
        result = self.client.post('/api/districts/optimize/', json = sobj)

    def test_bad_total_enrolled_field(self):
        sobj = oceanside()
        sobj["schools"][1]['total_enrolled'] = "NA"
        result = self.client.post('/api/districts/optimize/', json = sobj)

                

# Mostly accurate, severe need is not accurate
def oceanside():
    return copy.deepcopy({
    "name":"Oceanside Unified School District",
    "code":"02494",
    "total_enrolled":17990,
    "overall_isp":0.2758198999444136,
    "school_count":25,
    "best_strategy":None,
    "sfa_certified":True,
    "hhfka_sixty": "less",
    "est_reimbursement":0,
    "rates":{"free_lunch":3.41,"paid_lunch":0.32,"free_bfast":1.84,"paid_bfast":0.31},
    "schools":[
        {"school_code":"37735690113522","school_name":"Cesar Chavez Middle","school_type":"n/a","total_enrolled":716,"total_eligible":296,"daily_breakfast_served":107,"daily_lunch_served":394,"isp":0.4134,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"37735696108211","school_name":"CHRISTA MCAULIFFE ELEMENTARY","school_type":"n/a","total_enrolled":545,"total_eligible":97,"daily_breakfast_served":82,"daily_lunch_served":300,"isp":0.178,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"9367","school_name":"Clair W. Burgener Academy","school_type":"n/a","total_enrolled":229,"total_eligible":0,"daily_breakfast_served":34,"daily_lunch_served":126,"isp":0,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"37735696088991","school_name":"DEL RIO ELEMENTARY","school_type":"n/a","total_enrolled":335,"total_eligible":140,"daily_breakfast_served":50,"daily_lunch_served":184,"isp":0.4179,"active":True,"grouping":None,"severe_need":False},
        {"school_code":"8514","school_name":"DITMAR ELEMENTARY","school_type":"n/a","total_enrolled":3,"total_eligible":0,"daily_breakfast_served":0,"daily_lunch_served":2,"isp":0,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"37735696069108","school_name":"E. G. Garrison Elementary","school_type":"n/a","total_enrolled":350,"total_eligible":111,"daily_breakfast_served":53,"daily_lunch_served":193,"isp":0.3171,"active":True,"grouping":None,"severe_need":False},
        {"school_code":"37735693739018","school_name":"El Camino High","school_type":"n/a","total_enrolled":2958,"total_eligible":700,"daily_breakfast_served":444,"daily_lunch_served":1627,"isp":0.2366,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"37735696109995","school_name":"Ivey Ranch Elementary","school_type":"n/a","total_enrolled":700,"total_eligible":98,"daily_breakfast_served":105,"daily_lunch_served":385,"isp":0.14,"active":True,"grouping":None,"severe_need":False},
        {"school_code":"37735696038830","school_name":"Jefferson Middle","school_type":"n/a","total_enrolled":580,"total_eligible":287,"daily_breakfast_served":87,"daily_lunch_served":319,"isp":0.4948,"active":True,"grouping":None,"severe_need":True},
        {"school_code":"37735696038848","school_name":"LAUREL ELEMENTARY","school_type":"n/a","total_enrolled":445,"total_eligible":231,"daily_breakfast_served":67,"daily_lunch_served":245,"isp":0.5191,"active":True,"grouping":None,"severe_need":False},
        {"school_code":"37735696038855","school_name":"Libby Elementary","school_type":"n/a","total_enrolled":500,"total_eligible":222,"daily_breakfast_served":75,"daily_lunch_served":275,"isp":0.444,"active":True,"grouping":None,"severe_need":True}
    ],
    "state_code": "ca"
    })

