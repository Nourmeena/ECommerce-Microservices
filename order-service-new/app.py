from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime

app = Flask(__name__)

INVENTORY_SERVICE_URL = "http://localhost:5002"
PRICING_SERVICE_URL = "http://localhost:5003"
CUSTOMER_SERVICE_URL = "http://localhost:5004"

orders = []

@app.route("/api/orders/create", methods=["POST"])
def create_order():
    try:
        data = request.get_json()

        customer_id = data["customer_id"]
        products = data["products"]

        if not products:
            return jsonify({"error": "Order must contain products"}), 400

        # --- Inventory check ---
        for item in products:
            product_id = item["product_id"]
            quantity = item["quantity"]

            inv_resp = requests.get(
                f"{INVENTORY_SERVICE_URL}/api/inventory/check/{product_id}"
            )

            if inv_resp.status_code != 200:
                return jsonify({"error": "Inventory service error"}), 500

            inv_data = inv_resp.json()
            available_qty = inv_data["product"]["quantity_available"]

            if quantity > available_qty:
                return jsonify({
                    "error": f"Product {product_id} only has {available_qty} in stock"
                }), 400

        # --- Pricing ---
        pricing_resp = requests.post(
            f"{PRICING_SERVICE_URL}/api/pricing/calculate",
            json={"products": products}
        )

        if pricing_resp.status_code != 200:
            return jsonify({"error": "Pricing service failed"}), 500

        pricing_data = pricing_resp.json()
        total_amount = pricing_data["final_total"]

        # --- Create order ---
        order_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "products": products,
            "total_amount": total_amount,
            "timestamp": timestamp,
            "status": "CONFIRMED"
        }

        orders.append(order)

        # --- Update inventory ---
        requests.put(
            f"{INVENTORY_SERVICE_URL}/api/inventory/update",
            json={"products": products}
        )

        # --- Update loyalty (+10 points) ---
        requests.put(
            f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/loyalty",
            json={"points": 10}
        )

        return jsonify({
            "message": "Order created successfully",
            "order_id": order_id,
            "total_amount": total_amount,
            "status": "CONFIRMED"
        }), 201

    except KeyError:
        return jsonify({"error": "Invalid request format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders_by_customer():
    customer_id = request.args.get("customer_id")
    if not customer_id:
        return jsonify({"error": "customer_id required"}), 400

    result = [o for o in orders if str(o["customer_id"]) == customer_id]
    return jsonify(result), 200


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    for order in orders:
        if order["order_id"] == order_id:
            return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404


if __name__ == "__main__":
    app.run(port=5001, debug=True)
