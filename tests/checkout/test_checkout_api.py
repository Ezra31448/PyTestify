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

def test_shipping_options(client):
    response = client.get("/checkout/shipping-options")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    options = response.json().get("options")
    assert isinstance(options, list), "Shipping options should be a list"
    for i, opt in enumerate(options):
        assert "method" in opt, f"Option[{i}] should have 'method'"
        assert "cost" in opt, f"Option[{i}] should have 'cost'"

def test_payment(client):
    payment_data = {"method": "credit_card", "amount": 100.0}
    response = client.post("/checkout/pay", json=payment_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    payment = response.json().get("payment")
    assert payment is not None, "Response should contain 'payment' object"
    assert payment.get("status") == "success", "Payment should be successful"

def test_order_confirmation(client):
    response = client.get("/checkout/confirmation?order_id=1")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    confirmation = response.json().get("confirmation")
    assert confirmation is not None, "Response should contain 'confirmation' object"
    assert "order_id" in confirmation, "Confirmation should have 'order_id'"
    assert "details" in confirmation, "Confirmation should have 'details'"
