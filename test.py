from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Test Server Running</h1><p>If you can see this, Flask is working correctly.</p>'

if __name__ == '__main__':
    print("Starting test server...")
    app.run(debug=True, host='127.0.0.1', port=5000) 