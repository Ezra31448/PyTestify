import pytest
import os

@pytest.fixture(scope="session")
def id_token():
    # Temporary: Return None to disable id_token
    return None
