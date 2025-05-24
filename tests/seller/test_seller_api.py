import pytest
from utils.api_client import APIClient
from config import BASE_URL

@pytest.fixture(scope="module")
def client():
    return APIClient(BASE_URL, id_token=None)

def assert_with_detail(actual, expected, context=""):
    for key, value in expected.items():
        actual_value = actual.get(key)
        assert actual_value == value, (
            f"{context}Field '{key}' mismatch: expected '{value}', got '{actual_value}'"
        )

def test_create_product_listing(client):
    product_data = {"name": "Designer Dress", "description": "Handmade.", "price": 120.0}
    response = client.post("/seller/products", json=product_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    product = response.json().get("product")
    assert product is not None, "Response should contain 'product' object"
    assert_with_detail(product, product_data, context="[POST /seller/products] ")

def test_inventory_management(client):
    response = client.get("/seller/inventory")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    inventory = response.json().get("inventory")
    assert isinstance(inventory, list), "Inventory should be a list"
    for i, item in enumerate(inventory):
        assert "product_id" in item, f"Inventory[{i}] should have 'product_id'"
        assert "stock" in item, f"Inventory[{i}] should have 'stock'"

def test_order_fulfillment(client):
    response = client.get("/seller/orders")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    orders = response.json().get("orders")
    assert isinstance(orders, list), "Orders should be a list"
    for i, order in enumerate(orders):
        assert "order_id" in order, f"Order[{i}] should have 'order_id'"
        assert "status" in order, f"Order[{i}] should have 'status'"
