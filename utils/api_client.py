import requests

class APIClient:
    def __init__(self, base_url, id_token=None):
        self.base_url = base_url
        # If id_token is provided, add Authorization header
        self.headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}

    def get(self, endpoint, **kwargs):
        return requests.get(f"{self.base_url}{endpoint}", headers=self.headers, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def patch(self, endpoint, data=None, json=None, **kwargs):
        return requests.patch(f"{self.base_url}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers, **kwargs)
