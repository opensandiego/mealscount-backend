from flask import Flask, jsonify, render_template
from flask_caching import Cache
from flask_cors import CORS
import os

cache = Cache()

# API Stuff - TODO move to its own module
import csv,codecs
from cep_estimatory import parse_districts   
i = lambda x: int(x.replace(',',''))

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object(__name__)

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

@app.route('/api/districts/ca/')
@cache.cached(timeout=3600)
def district():
    state = "ca" # TODO make this for other states
    cupc_csv_file = "data/calpads_school_level_1819.csv"  
    schools = [r for r in csv.DictReader(codecs.open(cupc_csv_file)) if i(r['total_enrolled']) > 0]
    district_objects =  parse_districts(schools,[])
    districts = [
        d.as_dict() for d in district_objects
    ]
    return jsonify(districts)

# sanity check route
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()