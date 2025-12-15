from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)

# Inventory Service URLs
INVENTORY_CHECK_URL = "http://localhost:5002/api/inventory/check/"
INVENTORY_UPDATE_URL = "http://localhost:5002/api/inventory/update"

@app.route("/api/orders/create", methods=["POST"])
def create_order():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    # validate required fields
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    customer_id = data.get("customer_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not customer_id or not product_id or not quantity:
        return jsonify({
            "error": "customer_id, product_id, and quantity are required"
        }), 400

    try:
        customer_id = int(customer_id)
        product_id = int(product_id)
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid input types"}), 400

    # 1️⃣ Check inventory
    inventory_response = requests.get(
        f"{INVENTORY_CHECK_URL}{product_id}"
    )

    if inventory_response.status_code != 200:
        return jsonify({
            "error": "Product not found in inventory"
        }), 404

    inventory_data = inventory_response.json()["product"]

    if inventory_data["quantity_available"] < quantity:
        return jsonify({
            "error": "Insufficient stock",
            "available": inventory_data["quantity_available"]
        }), 400

    unit_price = inventory_data["unit_price"]
    total_amount = unit_price * quantity

    # 2️⃣ Update inventory
    update_payload = {
        "products": [
            {
                "product_id": product_id,
                "quantity": quantity
            }
        ]
    }

    update_response = requests.put(
        INVENTORY_UPDATE_URL,
        json=update_payload
    )

    if update_response.status_code != 200:
        return jsonify({
            "error": "Failed to update inventory"
        }), 500

    # 3️⃣ Create order
    order_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"

    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "product": {
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price
        },
        "total_amount": total_amount,
        "status": "CONFIRMED",
        "created_at": created_at
    }

    return jsonify(order), 201


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    return jsonify({
        "error": "Order storage not implemented"
    }), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": "Order Service",
        "status": "running",
        "port": 5001
    }), 200


if __name__ == "__main__":
    print("Starting Order Service on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)

