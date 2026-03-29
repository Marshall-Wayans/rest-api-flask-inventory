from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mock database
inventory = [
    {"id": 1, "product_name": "Coca-Cola", "brands": "Coca-Cola Co", "quantity": 100, "price": 1.99, "barcode": "0049000028911"},
    {"id": 2, "product_name": "Cheerios", "brands": "General Mills", "quantity": 50, "price": 4.49, "barcode": "016000275188"},
]
next_id = 3

# GET all items
@app.route("/inventory", methods=["GET"])
def get_all():
    return jsonify(inventory), 200

# GET single item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_one(id):
    item = next((i for i in inventory if i["id"] == id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

# POST add item
@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json()
    if not data or not data.get("product_name") or not data.get("quantity") or not data.get("price"):
        return jsonify({"error": "product_name, quantity and price required"}), 400
    item = {"id": next_id, "product_name": data["product_name"], "brands": data.get("brands", ""),
            "quantity": data["quantity"], "price": data["price"], "barcode": data.get("barcode", "")}
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

# PATCH update item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    for key in ["product_name", "brands", "quantity", "price", "barcode"]:
        if key in data:
            item[key] = data[key]
    return jsonify(item), 200

# DELETE item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    inventory.remove(item)
    return jsonify({"message": f"Item {id} deleted"}), 200

# Fetch from OpenFoodFacts
@app.route("/fetch-product/<barcode>", methods=["GET"])
def fetch_product(barcode):
    res = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json", timeout=5)
    data = res.json()
    if data.get("status") != 1:
        return jsonify({"error": "Product not found"}), 404
    p = data["product"]
    return jsonify({"product_name": p.get("product_name"), "brands": p.get("brands"), "barcode": barcode}), 200

if __name__ == "__main__":
    app.run(debug=True)