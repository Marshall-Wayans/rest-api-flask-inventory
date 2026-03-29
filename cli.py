import requests

BASE = "http://localhost:5000"

def menu():
    print("\n1. View all  2. View one  3. Add  4. Update  5. Delete  6. Fetch from API  0. Exit")
    return input("Choice: ").strip()

def view_all():
    items = requests.get(f"{BASE}/inventory").json()
    for i in items:
        print(f"[{i['id']}] {i['product_name']} | Qty: {i['quantity']} | ${i['price']}")

def view_one():
    id = input("Item ID: ")
    res = requests.get(f"{BASE}/inventory/{id}").json()
    print(res)

def add():
    name = input("Product name: ")
    qty = input("Quantity: ")
    price = input("Price: ")
    brands = input("Brand (optional): ")
    res = requests.post(f"{BASE}/inventory", json={"product_name": name, "quantity": int(qty), "price": float(price), "brands": brands})
    print(res.json())

def update():
    id = input("Item ID: ")
    qty = input("New quantity (blank to skip): ")
    price = input("New price (blank to skip): ")
    data = {}
    if qty: data["quantity"] = int(qty)
    if price: data["price"] = float(price)
    print(requests.patch(f"{BASE}/inventory/{id}", json=data).json())

def delete():
    id = input("Item ID: ")
    print(requests.delete(f"{BASE}/inventory/{id}").json())

def fetch_api():
    barcode = input("Enter barcode: ")
    res = requests.get(f"{BASE}/fetch-product/{barcode}").json()
    print(res)
    if "product_name" in res:
        if input("Add to inventory? (y/n): ").lower() == "y":
            qty = input("Quantity: ")
            price = input("Price: ")
            requests.post(f"{BASE}/inventory", json={**res, "quantity": int(qty), "price": float(price)})
            print("Added!")

actions = {"1": view_all, "2": view_one, "3": add, "4": update, "5": delete, "6": fetch_api}

while True:
    choice = menu()
    if choice == "0":
        break
    elif choice in actions:
        actions[choice]()
    else:
        print("Invalid choice.")