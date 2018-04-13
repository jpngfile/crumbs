import time
import ocr as ocr
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')
app.config['MONGO_URI'] = "mongodb://admin:123@ds243059.mlab.com:43059/crumbs"
mongo = PyMongo(app)

def scale_image(file): pass
def ml_scan_image(file): pass
def parse_image_json(json): pass
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
    data = {
            'team': team,
            'created': int(time.time()),
            'headers': {
                'some_header': ['sticky1', 'sticky2'],
                'another_one': ['test']
                }
            }
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
    if 'file' not in request.files:
        return jsonify(
            error='No file sent.')

    scaled_file = scale_image(request.files[file])
    image_json = ml_scan_image(scaled_file)
    payload = parse_image_json(image_json)

    cache_payload(payload, request.form['team'])

    return payload

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run()

