from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "service": "Order Service",
        "status": "Running",
        "port": 5001
    })


if __name__ == '__main__':
    print("Order Service is starting on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)
