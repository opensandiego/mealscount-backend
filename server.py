from flask import Flask, jsonify, render_template
from flask_caching import Cache
from flask_cors import CORS
from werkzeug.routing import BaseConverter

import csv,codecs,os,os.path
from strategies.base import CEPDistrict,CEPSchool
from cep_estimatory import parse_strategy

# From https://stackoverflow.com/questions/5870188/does-flask-support-regular-expressions-in-its-url-routing
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

cache = Cache()

# API Stuff - TODO move to its own module
import csv,codecs
from cep_estimatory import parse_districts   
i = lambda x: int(x.replace(',',''))

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object(__name__)
app.url_map.converters['regex'] = RegexConverter

cache_servers = os.environ.get('MEMCACHIER_SERVERS')
if cache_servers == None:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    cache.init_app(app,
        config={'CACHE_TYPE': 'saslmemcached',
                'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                'CACHE_MEMCACHED_USERNAME': cache_user,
                'CACHE_MEMCACHED_PASSWORD': cache_pass,
                'CACHE_OPTIONS': { 'behaviors': {
                    'tcp_nodelay': True,
                    'tcp_keepalive': True,
                    'connect_timeout': 2000, # ms
                    'send_timeout': 750 * 1000, # us
                    'receive_timeout': 750 * 1000, # us
                    '_poll_timeout': 2000, # ms
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30}}})

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

@app.route('/api/districts/<regex("[a-z]{2}"):state>/<regex("[a-zA-Z0-9]+"):code>/', methods=['POST'])
def district(state,code):
    district_params = request.json 
    district = get_district(state,code,district_params) 

    # TODO allow incoming data to specify strategies and strategy parameters 
    add_strategies(district,"OneToOne","OneGroup","Exhaustive","Binning")
    district.run_strategies() 
    district.evaluate_strategies()
    return jsonify(district.as_dict())

# sanity check route
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
