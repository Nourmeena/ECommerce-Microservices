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
        "service": "Inventory Service",
        "status": "Running",
        "port": 5002
    })

@app.route('/api/inventory/all', methods=['GET'])
def get_all_inventory():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory")
        products = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "success": True,
            "products": products,
            "count": len(products)
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    print("Inventory Service is starting on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)

