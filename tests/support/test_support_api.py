import pytest
from utils.api_client import APIClient
from config import BASE_URL

@pytest.fixture(scope="module")
def client():
    return APIClient(BASE_URL, id_token=None)

def test_faq(client):
    response = client.get("/support/faq")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    faqs = response.json().get("faqs")
    assert isinstance(faqs, list), "FAQs should be a list"
    for i, faq in enumerate(faqs):
        assert "question" in faq, f"FAQ[{i}] should have 'question'"
        assert "answer" in faq, f"FAQ[{i}] should have 'answer'"

def test_contact_form(client):
    form_data = {"name": "Test User", "email": "testuser@example.com", "message": "Help!"}
    response = client.post("/support/contact", json=form_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    result = response.json().get("result")
    assert result == "success", "Contact form should return success"

def test_live_chat(client):
    chat_data = {"message": "Hello, I need help!"}
    response = client.post("/support/chat", json=chat_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    chat = response.json().get("chat")
    assert chat is not None, "Response should contain 'chat' object"
    assert "reply" in chat, "Chat response should contain 'reply'"
