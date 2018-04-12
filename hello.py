from flask import Flask
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api')
def hello_api():
    return 'Hello, API!'

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run()
