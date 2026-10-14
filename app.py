from flask import Flask, jsonify
app = Flask(__name__)

@app.get('/')
def home():
    return jsonify(application='DevOps CI/CD Demo', status='running', message='Hello! The CI/CD demo application is live.')

@app.get('/health')
def health():
    return jsonify(status='healthy'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
