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

def test_add_to_cart(client):
    item = {"product_id": "P12345", "quantity": 2}
    response = client.post("/cart/add", json=item)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    cart = response.json().get("cart")
    assert cart is not None, "Response should contain 'cart' object"
    assert any(i["product_id"] == "P12345" for i in cart["items"]), "Product should be in cart"

def test_remove_from_cart(client):
    item = {"product_id": "P12345"}
    response = client.post("/cart/remove", json=item)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    cart = response.json().get("cart")
    assert cart is not None, "Response should contain 'cart' object"
    assert all(i["product_id"] != "P12345" for i in cart["items"]), "Product should not be in cart"

def test_cart_summary(client):
    response = client.get("/cart/summary")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    summary = response.json().get("summary")
    assert summary is not None, "Response should contain 'summary' object"
    assert "total_price" in summary, "Summary should have 'total_price'"
    assert "shipping_cost" in summary, "Summary should have 'shipping_cost'"
