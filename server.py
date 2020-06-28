from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug.routing import BaseConverter
from urllib.parse import urlparse
import os,os.path,datetime,time
import us

import csv,codecs,os,os.path
from strategies.base import CEPDistrict,CEPSchool
from cep_estimatory import parse_strategy

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

# Do i want this?
#CORS(app, resources={r'/api/*': {'origins': '*'}})

def get_district(state,code,district_params):
    # NOTE assumes we have ensured state and code are a-zA-Z0-9+,
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
            district = CEPDistrict(school.district,school.district_code)
        district.add_school(school)

    return district

def add_strategies(district,*strategies):
    for s in strategies:
        Klass,params,name = parse_strategy(s) 
        district.strategies.append( Klass(params,name) )

@app.route("/api/districts/optimize/", methods=['POST'])
def optimize():
    d_obj = request.json
    schools = d_obj["schools"]
    district = CEPDistrict(d_obj["name"],d_obj["code"],reimbursement_rates=d_obj["rates"])

    state = d_obj["state_code"]

    i = 1 
    for row in schools:
        # Expecting { school_code: {active, daily_breakfast_served,daily_lunch_served,total_eligible,total_enrolled }}
        # TODO rework how we initialize CEPSchool
        row["School Name"] = row.get("school_name","School %i"%i)
        row["School Code"] = row.get("school_code","school-%i"%i)
        row["School Type"] = row.get("school_type","")
        row['include_in_mealscount'] = row.get('active','true') and 'true' or 'false'
        i += 1
        district.add_school(CEPSchool(row))

    # TODO allow this as a param
    add_strategies(
        district,
        *["Pairs","OneToOne","Exhaustive","OneGroup","Spread","Binning","NYCMODA?fresh_starts=10"]
    )

    t0 = time.time()
    district.run_strategies()
    district.evaluate_strategies()

    result = district.as_dict()
    result["state_code"] = state
    result["optimization_info"] = {
        "timestamp":str(datetime.datetime.now()),
        "time": time.time() - t0
    }
    return result

@app.route('/api/districts/<regex("[a-z]{2}"):state>/<regex("[a-zA-Z0-9]+"):code>/', methods=['POST'])
def district(state,code):
    district_params = request.json 
    district = get_district(state,code,district_params) 

    # TODO allow incoming data to specify strategies and strategy parameters 
    add_strategies(district,"OneToOne","OneGroup","Exhaustive","Binning")
    district.run_strategies() 
    district.evaluate_strategies()
    return jsonify(district.as_dict())

@app.route('/api/states/', methods=['GET'])
def states():
    states = {} # keyed by lowercase abbr (e.g. "ca"), with "name", "district_data", "about"
    DATA_FOLDER = os.path.join(os.path.dirname(__file__),'data')
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__),'dist','static')

    for state in os.listdir(DATA_FOLDER):
        if os.path.exists(os.path.join(DATA_FOLDER,state)):
            state_info = us.states.lookup(state)
            if state_info:
                s = { "name":state_info.name, "fips":state_info.fips }
                if os.path.exists(os.path.join(DATA_FOLDER,state,"about.html")):
                    s["about"] = open(os.path.join(DATA_FOLDER,state,"about.html")).read()[:1024]
                # District data is loaded through /api/districts/state/
                if os.path.exists(os.path.join(STATIC_FOLDER,state,"districts.json")):
                    s["district_list"] = os.path.join("/static/",state,"districts.json")
                    states[state] = s
    return jsonify(states)

# sanity check route
@app.route('/', defaults={'path':''})
#@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html', 
        analytics_id=os.environ.get("GOOGLE_ANALYTICS_ID",False),
        source_version=os.environ.get("SOURCE_VERSION","XYZ")
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

if __name__ == '__main__':
    app.run()
