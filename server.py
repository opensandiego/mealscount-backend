from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug.routing import BaseConverter
from urllib.parse import urlparse
import os,os.path,datetime,time
import us,uuid,json
import zipfile
from io import BytesIO

import boto3
import base64
import requests

import csv,codecs,os,os.path
from strategies.base import CEPDistrict,CEPSchool
from strategies.naive import CustomGroupsCEPStrategy
from cep_estimatory import parse_strategy,add_strategies

# If we have specified AWS keys, this is where we will tell the client where
# the results will be on S3
S3_RESULTS_URL = os.environ.get("S3_RESULTS_URL","https://mealscount-results.s3-us-west-1.amazonaws.com")

# From https://stackoverflow.com/questions/5870188/does-flask-support-regular-expressions-in-its-url-routing
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# API Stuff - TODO move to its own module
import csv,codecs
from cep_estimatory import parse_districts   
i = lambda x: int(x.replace(',',''))

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object(__name__)
app.url_map.converters['regex'] = RegexConverter

def get_district(state,code,district_params):
    # NOTE assumes we have ensured state and code are a-zA-Z0-9+ (which we do in the handler below)
    # BEWARE of dangerous paths! (e.g. '..')
    path ="data/%s/latest.csv" % state
    if not os.path.exists(path): return None # we may not have this state yet

    # Here we kind of yet-again duplicate the loading of a district from the csv
    # TODO centralize this in a loader somewhere
    # we filter out rows that match the district code
    i = lambda x: int(x.replace(',','')) # Quick function to make "123,123" into an int 123123
    schools_data = [
        r for r in 
        csv.DictReader(codecs.open(path)) 
        if i(r['total_enrolled']) > 0  and r['District Code'] == code # ignore 0 student schools
    ] 
    district = None
    for row in schools_data:
        # TODO check for updated row data in district_params!
        school = CEPSchool(row)
        if district == None:
            district = CEPDistrict(school.district,school.district_code,state=state)
        district.add_school(school)

    return district


@app.route("/api/districts/optimize-async/", methods=['POST'])
def optimize_async():
    if not os.environ.get("AWS_ACCESS_KEY_ID",False):
       return optimize() 

    # Generate a key to publish the resulting file to
    event = request.json

    if not event:
        return {"error":"Invalid JSON data, please ensure all data fields are active"}

    n = datetime.datetime.now()
    key = "data/%i/%02i/%02i/%s-%s.json" % (
        n.year,n.month,n.day,
        event.get("code","unspecified"),
        uuid.uuid1(),
    )
    event["key"] = key

    max_groups,evaluate_by = int(event.get("max_groups",10)),event.get("evaluate_by","reimbursement")
    if not event.get("strategies_to_run",False):
        event["strategies_to_run"] = [
            "Pairs",
            "OneToOne",
            "Exhaustive?evaluate_by=%s" % evaluate_by,
            "OneGroup",
            "Spread",
            "Binning",
        ] 
        if len(event["schools"]) > 11:
            event["strategies_to_run"].append("NYCMODA?fresh_starts=50&iterations=1000&ngroups=%s&evaluate_by=%s" % (max_groups,evaluate_by))
            event["strategies_to_run"].append("GreedyLP")

    # Large school districts (LA) don't fit in our 256kb Event Invocation limit on Lambda,
    # So sneak it in via ZipFile
    if len(event["schools"]) > 500: 
        with BytesIO() as mf:
            with zipfile.ZipFile(mf, mode='w',compression=zipfile.ZIP_BZIP2) as zf:
                zf.writestr('data.json', json.dumps(event) )
            event = {"zipped": base64.b64encode(mf.getvalue()).decode('utf-8') }

    # Invoke our Lambda Function

    client = boto3.client('lambda') 
    response = client.invoke(
        FunctionName=os.environ.get("LAMBDA_FUNCTION_NAME","mealscount-optimize"),
        InvocationType="Event",
        Payload=json.dumps(event),
    )
    result = {
        "function_status": response["StatusCode"],
        "key": key,
        "results_url": "%s/%s" % (S3_RESULTS_URL,key),
    }
    if response.get("FunctionError",None):
        result["function_error"] = response.get("FunctionError")

    if os.environ.get("GOOGLE_ANALYTICS_ID",False):
        if "vba-web" in request.headers.get("User-Agent","").lower():
            params = {
                "v":1,
                "tid":os.environ.get("GOOGLE_ANALYTICS_ID"),
                "cid":555,
                "t":"pageview",
                "dp":"/xls-calculator/%s/" % event.get("state_code","unknown"),
            }
            requests.post("https://www.google-analytics.com/collect",params,headers={"user-agent":request.headers.get("User-Agent")})

    return result

@app.route("/api/districts/optimize/", methods=['POST'])
def optimize():
    d_obj = request.json

    if not d_obj:
        return {"error":"Invalid JSON data, please ensure all data fields are active"}

    schools = d_obj["schools"]
    state = d_obj["state_code"]
    district = CEPDistrict(
        d_obj.get("name","DistrictName"),
        d_obj.get("code","DistrictCode"),
        state=state,
        sfa_certified=d_obj.get("sfa_certified",True),
        hhfka_sixty=d_obj.get("hhfka_sixty","more")
    )

    i = 1 
    for row in schools:
        # Expecting { school_code: {active, daily_breakfast_served,daily_lunch_served,total_eligible,total_enrolled }}
        # TODO rework how we initialize CEPSchool
        if not row.get("school_code",None) or not row.get("total_enrolled",None):
            continue
        row["School Name"] = row.get("school_name","School %i"%i)
        row["School Code"] = row.get("school_code","school-%i"%i)
        row["School Type"] = row.get("school_type","")
        row['include_in_mealscount'] = row.get('active','true') and 'true' or 'false'
        i += 1
        district.add_school(CEPSchool(row))

    if not district.schools:
        return {"error":"No schools provided"}

    # TODO allow this as a param
    max_groups,evaluate_by = int(d_obj.get("max_groups",10)),d_obj.get("evaluate_by","reimbursement")
    add_strategies(
        district,
        *[
            "Pairs",
            "OneToOne",
            "Exhaustive?evaluate_by=%s"%evaluate_by,
            "OneGroup",
            "Spread",
            "Binning",
            "NYCMODA?fresh_starts=50&iterations=1000&ngroups=%s&evaluate_by=%s"%(max_groups,evaluate_by),
            "GreedyLP"
        ]
    )

    t0 = time.time()
    district.run_strategies()
    district.evaluate_strategies(max_groups=max_groups,evaluate_by=evaluate_by)

    result = district.as_dict()
    result["state_code"] = state
    result["evaluate_by"] = evaluate_by
    result["max_groups"] = max_groups
    result["optimization_info"] = {
        "timestamp":str(datetime.datetime.now()),
        "time": time.time() - t0
    }
    return result

@app.route("/api/districts/calculate/", methods=['POST'])
def calculate():
    d_obj = request.json

    if not d_obj:
        return {"error":"Invalid JSON data, please ensure all data fields are active"}

    schools = d_obj["schools"]
    state = d_obj["state_code"]
    district = CEPDistrict(
        d_obj.get("name","DistrictName"),
        d_obj.get("code","DistrictCode"),
        state=state,
        sfa_certified=d_obj.get("sfa_certified",True),
        hhfka_sixty=d_obj.get("hhfka_sixty","more")
    )

    # TODO consolidate with optimize() above
    i = 1 
    groupings = {}
    for row in schools:
        # Expecting { school_code: {active, daily_breakfast_served,daily_lunch_served,total_eligible,total_enrolled }}
        # TODO rework how we initialize CEPSchool
        if not row.get("school_code",None) or not row.get("total_enrolled",None):
            continue
        row["School Name"] = row.get("school_name","School %i"%i)
        row["School Code"] = row.get("school_code","school-%i"%i)
        row["School Type"] = row.get("school_type","")
        row['include_in_mealscount'] = row.get('active','true') and 'true' or 'false'
        i += 1
        school = CEPSchool(row)
        district.add_school(school)
        groupings.setdefault(row.get('grouping',None),[])
        groupings[row.get('grouping')].append(school.code)

    # CONSIDER district validate
    if not district.schools:
        return {"error":"No schools provided"}

    # We direct this into the custom groups strategy which doesn't actually
    # do any optimization

    custom = CustomGroupsCEPStrategy(params={},name="Custom Grouping")
    custom.groupings = groupings # not really official way to set this
    district.strategies.append(custom)
    district.run_strategies()
    district.evaluate_strategies(max_groups=len(custom.groupings)+1)

    result = district.as_dict()
    result["state_code"] = state

    return result

@app.route('/api/districts/<regex("[a-z]{2}"):state>/<regex("[a-zA-Z0-9]+"):code>/', methods=['POST'])
def district(state,code):
    district_params = request.json 
    district = get_district(state,code,district_params) 

#    # TODO allow incoming data to specify strategies and strategy parameters 
#    add_strategies(district,"OneToOne","OneGroup","Exhaustive","Binning")
#    district.run_strategies() 
#    district.evaluate_strategies()

    return jsonify(district.as_dict())

# TODO set aggressive cache header
@app.route('/api/states/', methods=['GET'])
def states():
    states = {} # keyed by lowercase abbr (e.g. "ca"), with "name", "district_data", "about"
    DATA_FOLDER = os.path.join(os.path.dirname(__file__),'data')
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__),'dist','static')

    for state in os.listdir(DATA_FOLDER):
        if os.path.exists(os.path.join(DATA_FOLDER,state)):
            state_info = us.states.lookup(state)
            if state_info:
                s = { "name":state_info.name, "fips":state_info.fips, "state_code": state }
                if os.path.exists(os.path.join(DATA_FOLDER,state,"about.html")):
                    s["about"] = open(os.path.join(DATA_FOLDER,state,"about.html")).read()[:1024]
                if os.path.exists(os.path.join(DATA_FOLDER,state,"faq.html")):
                    s["faq"] = open(os.path.join(DATA_FOLDER,state,"faq.html")).read()[:1024]
                if os.path.exists(os.path.join(DATA_FOLDER,state,"contact.json")):
                    try:
                        s["contact"] = json.loads(open(os.path.join(DATA_FOLDER,state,"contact.json")).read())
                    except ValueError: pass
                # District data is loaded through /api/districts/state/
                if os.path.exists(os.path.join(STATIC_FOLDER,state,"districts.json")):
                    s["district_list"] = os.path.join("/static/",state,"districts.json")
                    states[state] = s
    return jsonify(states)

# sanity check route
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html', 
        analytics_id=os.environ.get("GOOGLE_ANALYTICS_ID",False),
        olark_id = os.environ.get("OLARK_ID",False),
    )

if "DYNO" in os.environ:
    # INiti Sentry
    import sentry_sdk
    sentry_sdk.init(os.environ["SENTRY_DSN"])

    # If we are in the heroku environment
    # Let's do some productiony things
    # Force SSL
    Talisman(app,content_security_policy=None) 
    # TODO get webpack and vue sorted for CSP

    # And force www.mealscount.com
    @app.before_request
    def redirect_nonwww():
        """Redirect non-www requests to www."""
        urlparts = urlparse(request.url)
        if urlparts.netloc != 'www.mealscount.com':
            return redirect('https://www.mealscount.com/', code=301)

# Allow all origins for integration with Excel Add-On
# from https://stackoverflow.com/a/59906139
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

if __name__ == '__main__':
    app.run()
