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


INVENTORY_SERVICE_URL = "http://localhost:5002"

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_db_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

#check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'service': 'pricing Service',
        'status': 'running',
        'port': 5003
    }), 200


#  calculate pricing
@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    data = request.get_json()
    if not data or 'products' not in data:
        return jsonify({'success': False, 'error': 'Missing products data'}), 400
    
    products = data['products']
    result_items = []
    total_before_tax = 0.0

    conn = None
    cursor = None

    try:
        # Connect to DB
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        for product in products:
            product_id = product.get('product_id')
            quantity = product.get('quantity')

            # Call Inventory Service
            inventory_resp = requests.get(f"{INVENTORY_SERVICE_URL}/api/inventory/check/{product_id}")
            if inventory_resp.status_code != 200:
                return jsonify({'success': False, 'error': f"Product {product_id} not found in inventory"}), 404
            
            inventory_data = inventory_resp.json()['product']
            unit_price = inventory_data['unit_price']
            in_stock = inventory_data['in_stock']

            if not in_stock or inventory_data['quantity_available'] < quantity:
                return jsonify({'success': False, 'error': f"Product {product_id} out of stock"}), 400

            subtotal = unit_price * quantity
            discount = 0.0

            # Check for discount rules
            cursor.execute(
                "SELECT * FROM pricing_rules WHERE product_id = %s AND min_quantity <= %s",
                (product_id, quantity)
            )
            rule = cursor.fetchone()
            if rule:
                discount = subtotal * (float(rule['discount_percentage']) / 100)
            
            total_before_tax += (subtotal - discount)

            result_items.append({
                'product_id': product_id,
                'unit_price': unit_price,
                'quantity': quantity,
                'subtotal': subtotal,
                'discount': discount
            })

        # Get tax rate (assuming one region for simplicity)
        cursor.execute("SELECT tax_rate FROM tax_rates LIMIT 1")
        tax_row = cursor.fetchone()
        tax_rate = float(tax_row['tax_rate']) if tax_row else 0.0

        tax = total_before_tax * (tax_rate / 100)
        final_total = total_before_tax + tax

        return jsonify({
            'success': True,
            'items': result_items,
            'tax': tax,
            'final_total': final_total
        }), 200

    except Error as e:
        return jsonify({'success': False, 'error': f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f"Server error: {str(e)}"}), 500
    finally:
        close_db_connection(conn, cursor)

if __name__ == '__main__':
    print("Pricing Service is starting on port 5003...")
    app.run(host='0.0.0.0', port=5003, debug=True)
