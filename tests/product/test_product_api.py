import pytest
from utils.api_client import APIClient
from utils.data_loader import load_test_data
from config import BASE_URL

@pytest.fixture(scope="module")
def client():
    # Temporary: No id_token required
    return APIClient(BASE_URL, id_token=None)

def assert_with_detail(actual, expected, context=""):
    for key, value in expected.items():
        actual_value = actual.get(key)
        assert actual_value == value, (
            f"{context}Field '{key}' mismatch: expected '{value}', got '{actual_value}'"
        )

def test_get_product(client):
    expected = {
        "product_id": "P12345",
        "name": "Test Product",
        "price": 19.99
    }
    response = client.get("/product/1")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    product = response.json().get("product")
    assert product is not None, "Response should contain 'product' object"
    assert_with_detail(product, expected, context="[GET /product/1] ")

def test_get_products_list(client):
    expected_products = [
        {"product_id": "P12345", "name": "Test Product", "price": 19.99},
        # Add more expected products here if needed
    ]
    response = client.get("/product")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    products = response.json().get("products")
    assert isinstance(products, list), "Response 'products' should be a list"
    for i, product in enumerate(products):
        assert_with_detail(product, expected_products[i], context=f"[GET /product][{i}] ")

def test_create_product(client):
    product_data = load_test_data("product.json")
    expected = product_data.copy()
    response = client.post("/product", json=product_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    created = response.json().get("product")
    assert created is not None, "Response should contain 'product' object"
    assert_with_detail(created, expected, context="[POST /product] ")

def test_browse_products(client):
    response = client.get("/products?category=dresses")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    products = response.json().get("products")
    assert isinstance(products, list), "Products should be a list"
    for i, product in enumerate(products):
        assert "product_id" in product, f"Product[{i}] should have 'product_id'"
        assert "name" in product, f"Product[{i}] should have 'name'"
        assert "price" in product, f"Product[{i}] should have 'price'"

def test_product_details(client):
    expected = {"product_id": "P12345", "name": "Test Product", "price": 19.99}
    response = client.get("/product/P12345")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    product = response.json().get("product")
    assert product is not None, "Response should contain 'product' object"
    assert_with_detail(product, expected, context="[GET /product/P12345] ")

def test_recommendations(client):
    response = client.get("/products/recommendations")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    recs = response.json().get("recommendations")
    assert isinstance(recs, list), "Recommendations should be a list"
    for i, rec in enumerate(recs):
        assert "product_id" in rec, f"Recommendation[{i}] should have 'product_id'"
        assert "name" in rec, f"Recommendation[{i}] should have 'name'"
