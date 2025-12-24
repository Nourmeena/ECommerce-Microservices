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

@app.route('/health')
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
    
@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM customers WHERE customer_id = %s",
            (customer_id,)
        )
        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({
            "success": True,
            "customer": customer
        }), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    # Get orders for a specific customer
# Calls the Order Service API
@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    try:
        response = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/customer/{customer_id}"
        )

        # Order Service returned error
        if response.status_code != 200:
            return jsonify({
                "success": False,
                "error": "Failed to fetch orders from Order Service",
                "status_code": response.status_code,
                "raw_response": response.text
            }), 502

        # Try parsing JSON safely
        try:
            orders = response.json()
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Order Service did not return JSON",
                "raw_response": response.text
            }), 500

        return jsonify({
            "success": True,
            "orders": orders
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": "Order Service not reachable",
            "details": str(e)
        }), 500
 
 # Update loyalty points for a customer
# Expects JSON payload: { "points": 10 }
@app.route('/api/customers/<int:customer_id>/loyalty', methods=['PUT'])
def update_loyalty_points(customer_id):
    try:
        data = request.get_json()
        points = data.get("points")

        if points is None:
            return jsonify({"error": "points is required"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE customers
            SET loyalty_points = loyalty_points + %s
            WHERE customer_id = %s
            """,
            (points, customer_id)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "success": True,
            "message": "Loyalty points updated successfully"
        }), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    print("Customer Service is starting on port 5004...")
    app.run(host='0.0.0.0', port=5004, debug=True)
