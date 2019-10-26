from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object(__name__)

# Do i want this?
CORS(app, resources={r'/api/*': {'origins': '*'}})

@app.route('/api/district')
def district():
    resposne = {
        "TODO":"Run District"
    }
    return jsonify(response)

# sanity check route
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()