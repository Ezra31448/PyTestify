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

def test_get_badge(client):
    expected = {
        "id": 1,
        "name": "Sample Badge",
        "description": "Awarded for exemplary performance."
    }
    response = client.get("/badge/1")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    badge = response.json().get("badge")
    assert badge is not None, "Response should contain 'badge' object"
    assert_with_detail(badge, expected, context="[GET /badge/1] ")

def test_get_badges_list(client):
    expected_badges = [
        {"id": 1, "name": "Sample Badge", "description": "Awarded for exemplary performance."},
        # Add more expected badges here if needed
    ]
    response = client.get("/badge")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    badges = response.json().get("badges")
    assert isinstance(badges, list), "Response 'badges' should be a list"
    for i, badge in enumerate(badges):
        assert_with_detail(badge, expected_badges[i], context=f"[GET /badge][{i}] ")

def test_create_badge(client):
    badge_data = load_test_data("badge.json")
    expected = badge_data.copy()
    response = client.post("/badge", json=badge_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    created = response.json().get("badge")
    assert created is not None, "Response should contain 'badge' object"
    assert_with_detail(created, expected, context="[POST /badge] ")
