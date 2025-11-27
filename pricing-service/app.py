from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'secure_password',
    'database': 'ecommerce_system1'
}


INVENTORY_SERVICE_URL = "http://localhost:5002"

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return jsonify({
        "service": "Pricing Service",
        "status": "Running",
        "port": 5003
    })



if __name__ == '__main__':
    print("Pricing Service is starting on port 5003...")
    app.run(host='0.0.0.0', port=5003, debug=True)
