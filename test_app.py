import pytest
from unittest.mock import patch, MagicMock
from app import app, inventory

@pytest.fixture
def client():
    app.config["TESTING"] = True
    inventory.clear()
    inventory.extend([
        {"id": 1, "product_name": "Coca-Cola", "brands": "Coca-Cola Co", "quantity": 100, "price": 1.99, "barcode": "123"},
        {"id": 2, "product_name": "Cheerios", "brands": "General Mills", "quantity": 50, "price": 4.49, "barcode": "456"},
    ])
    with app.test_client() as c:
        yield c

# GET all
def test_get_all(client):
    res = client.get("/inventory")
    assert res.status_code == 200
    assert len(res.get_json()) == 2

# GET one
def test_get_one(client):
    assert client.get("/inventory/1").status_code == 200

def test_get_one_not_found(client):
    assert client.get("/inventory/99").status_code == 404

# POST
def test_add_item(client):
    res = client.post("/inventory", json={"product_name": "Oats", "quantity": 10, "price": 2.99})
    assert res.status_code == 201
    assert res.get_json()["product_name"] == "Oats"

def test_add_item_missing_fields(client):
    assert client.post("/inventory", json={"product_name": "Oats"}).status_code == 400

# PATCH
def test_update_item(client):
    res = client.patch("/inventory/1", json={"quantity": 999})
    assert res.status_code == 200
    assert res.get_json()["quantity"] == 999

def test_update_not_found(client):
    assert client.patch("/inventory/99", json={"quantity": 1}).status_code == 404

# DELETE
def test_delete_item(client):
    assert client.delete("/inventory/1").status_code == 200
    assert client.get("/inventory/1").status_code == 404

def test_delete_not_found(client):
    assert client.delete("/inventory/99").status_code == 404

# External API (mocked)
def test_fetch_product_success(client):
    mock = MagicMock()
    mock.json.return_value = {"status": 1, "product": {"product_name": "Mock", "brands": "BrandX"}}
    with patch("app.requests.get", return_value=mock):
        res = client.get("/fetch-product/123")
        assert res.status_code == 200
        assert res.get_json()["product_name"] == "Mock"

def test_fetch_product_not_found(client):
    mock = MagicMock()
    mock.json.return_value = {"status": 0}
    with patch("app.requests.get", return_value=mock):
        assert client.get("/fetch-product/000").status_code == 404