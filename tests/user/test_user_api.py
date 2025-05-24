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

def test_get_user(client):
    expected = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPass123!"
    }
    response = client.get("/user/1")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    user = response.json().get("user")
    assert user is not None, "Response should contain 'user' object"
    assert_with_detail(user, expected, context="[GET /user/1] ")

def test_get_users_list(client):
    expected_users = [
        {"username": "testuser", "email": "testuser@example.com", "password": "TestPass123!"},
        # Add more expected users here if needed
    ]
    response = client.get("/user")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    users = response.json().get("users")
    assert isinstance(users, list), "Response 'users' should be a list"
    for i, user in enumerate(users):
        assert_with_detail(user, expected_users[i], context=f"[GET /user][{i}] ")

def test_create_user(client):
    user_data = load_test_data("user.json")
    expected = user_data.copy()
    response = client.post("/user", json=user_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    created = response.json().get("user")
    assert created is not None, "Response should contain 'user' object"
    assert_with_detail(created, expected, context="[POST /user] ")

def test_user_registration(client):
    user_data = load_test_data("user.json")
    expected = user_data.copy()
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    user = response.json().get("user")
    assert user is not None, "Response should contain 'user' object"
    assert_with_detail(user, expected, context="[POST /user/register] ")

def test_user_login(client):
    login_data = {"email": "testuser@example.com", "password": "TestPass123!"}
    response = client.post("/user/login", json=login_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "token" in data, "Login response should contain 'token'"

def test_profile_update(client):
    update_data = {"username": "updateduser"}
    response = client.put("/user/profile", json=update_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    user = response.json().get("user")
    assert user is not None, "Response should contain 'user' object"
    assert user.get("username") == "updateduser", "Username should be updated"

def test_order_history(client):
    response = client.get("/user/orders")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    orders = response.json().get("orders")
    assert isinstance(orders, list), "Order history should be a list"
    for i, order in enumerate(orders):
        assert "order_id" in order, f"Order[{i}] should have 'order_id'"
        assert "status" in order, f"Order[{i}] should have 'status'"
