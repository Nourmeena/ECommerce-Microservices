from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)  

# database 
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'secure_password',
    'database': 'ecommerce_system1'
}

def db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

#close connection
def close_db_connection(conn, cursor):
        cursor.close()
        conn.close()


#check stock availability
@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_stock(product_id):
    conn = None
    cursor = None
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        
        if product:
            return jsonify({
                'success': True,
                'product': {
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'quantity_available': product['quantity_available'],
                    'unit_price': float(product['unit_price']),
                    'in_stock': product['quantity_available'] > 0
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
            
    except Error as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    
    finally:
        close_db_connection(conn, cursor)


#Update inventory after order
@app.route('/api/inventory/update', methods=['PUT'])
def update_inventory():
    conn = None
    cursor = None
    
    try:
        # get data from request
        data = request.get_json()
        
        # validate input
        if not data or 'products' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing products data'
            }), 400
        
        products = data['products']
        
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        updated_products = []
        
        # process each product
        for product in products:
            product_id = product.get('product_id')
            quantity = product.get('quantity')
            
            cursor.execute(
                "SELECT quantity_available FROM inventory WHERE product_id = %s",
                (product_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    'success': False,
                    'error': f'Product {product_id} not found'
                }), 404
            
            current_stock = result['quantity_available']
            
            if current_stock < quantity:
                return jsonify({
                    'success': False,
                    'error': f'Cannot proceed for product {product_id}. Available: {current_stock}, Requested: {quantity}'
                }), 400
            
            # Update stock
            new_quantity = current_stock - quantity
            cursor.execute(
                "UPDATE inventory SET quantity_available = %s, last_updated = %s WHERE product_id = %s",
                (new_quantity, datetime.now(), product_id)
            )
            
            updated_products.append({
                'product_id': product_id,
                'previous_stock': current_stock,
                'new_stock': new_quantity,
                'quantity_sold': quantity
            })
        
        # commit changes
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Inventory updated successfully',
            'updated_products': updated_products
        }), 200
        
    except Error as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500
    
    finally:
        close_db_connection(conn, cursor)


# get all product
@app.route('/api/inventory/products', methods=['GET'])
def get_all_products():
    conn = None
    cursor = None
    
    try:
        conn = db_connection()
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory WHERE quantity_available > 0")
        products = cursor.fetchall()
        
        for product in products:
            product['unit_price'] = float(product['unit_price'])
        
        return jsonify({
            'success': True,
            'products': products
        }), 200
        
    except Error as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    
    finally:
        close_db_connection(conn, cursor)


#check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'service': 'Inventory Service',
        'status': 'running',
        'port': 5002
    }), 200


if __name__ == '__main__':
    print("Starting Inventory Service on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)