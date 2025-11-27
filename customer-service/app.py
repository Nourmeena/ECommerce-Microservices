from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import requests

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'secure_password',
    'database': 'ecommerce_system1'
}

ORDER_SERVICE_URL = "http://localhost:5001"

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
        "service": "Customer Service",
        "status": "Running",
        "port": 5004
    })

@app.route('/api/customers/all', methods=['GET'])
def get_all_customers():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "customers": customers,
            "count": len(customers)
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    print("Customer Service is starting on port 5004...")
    app.run(host='0.0.0.0', port=5004, debug=True)
