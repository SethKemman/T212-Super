from .endpoints import Endpoints

class Account:
    def __init__(self, client):
        self.client = client

    def summary(self):
        return self.client.get(Endpoints.ACCOUNT_SUMMARY)
