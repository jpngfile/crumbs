import time
from ocr import scaleImage, getAzureAnalysis, parseAnalysis
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:1234"}})

@app.route('/board/<team>')
def home_boards(team):
    return app.send_static_file('index.html')

app.config['MONGO_URI'] = "mongodb://admin:123@ds243059.mlab.com:43059/crumbs"
mongo = PyMongo(app)

def scale_image(file, size):
    return scaleImage(file, size)

def ml_scan_image(image_data):
    return getAzureAnalysis(image_data)

def parse_image_json(json):
    return parseAnalysis(json)

def cache_payload(json, team):
    scrum_dict = {
        'team': team,
        'created': int(time.time()),
        'headers': json
    }
    mongo.db.boards.insert(scrum_dict)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/<team>')
def get_scrum(team):
    try:
        data = mongo.db.boards.find({'team': team}).sort([('created', -1)]).next()
        data.pop('_id', None)
    except StopIteration:
        data = {}
    return jsonify(data)

@app.route('/api')
def hello_api():
    return jsonify(
            message='Hello, API!')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'team' not in request.form:
        return jsonify(
            error='No team specified.')

    return jsonify({
            'team': request.form['team'],
            'created': int(time.time()),
            'headers': {
                'backlog': ['sleep', 'game'],
                'doing': ['work'],
                'done': ['eat']
            }
        })

    if 'file' not in request.files:
        return jsonify(
            error='No file sent.')

    team_name = request.form['team']
    scaled_file = scale_image(request.files['file'], 3200)
    image_json = ml_scan_image(scaled_file.getvalue())
    payload = parse_image_json(image_json)

    cache_payload(payload, team_name)

    return redirect(url_for('get_scrum', team=team_name))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run()

