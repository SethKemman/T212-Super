from .endpoints import Endpoints

class Instruments:
    def __init__(self, client):
        self.client = client

    def GetMetadataExchanges(self):
        return self.client.get(Endpoints.METADATA_EXCHANGES)
    
    def GetMetadataInstruments(self):
        return self.client.get(Endpoints.METADATA_INSTRUMENTS)