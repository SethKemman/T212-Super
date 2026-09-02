from .endpoints import Endpoints

class Positions:
    def __init__(self, client):
        self.client = client

    def getPositions(self):
        return self.client.get(Endpoints.POSITIONS)