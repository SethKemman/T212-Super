from dotenv import load_dotenv
import os
import requests
from datetime import datetime

from .endpoints import Endpoints
from .account import Account
from .instruments import Instruments
from .positions import Positions
class Client:
    def __init__(self):
        #Loading environment
        load_dotenv()
        MODE = os.getenv("MODE")
        API_KEY_ID = None
        SECRET = None
        if MODE == "DEMO":
            API_KEY_ID = os.getenv("DEMO_API_KEY_ID")
            SECRET = os.getenv("DEMO_SECRET")
        elif MODE == "LIVE":
            API_KEY_ID = os.getenv("LIVE_API_KEY_ID")
            SECRET = os.getenv("LIVE_SECRET")
        else:
            raise ValueError(f"Unknown MODE: '{MODE}'. Expected 'DEMO' or 'LIVE'.")

        self.session = requests.Session()

        self.session.auth=(API_KEY_ID, SECRET)

        self.account = Account(self)
        self.instruments = Instruments(self)
        self.positions = Positions(self)

    def get(self, endpoint, **kwargs):
        response = self.session.get(endpoint, **kwargs)
        response.raise_for_status()
        currentTime = datetime.now().strftime("%H:%M:%S")
        print(f"Data retrieved at {currentTime}")
        return response.json()
    
    def post(self, endpoint, **kwargs):
        response = self.session.post(endpoint, **kwargs)
        response.raise_for_status()

        return response.json()

    def delete(self, endpoint, **kwargs):
        response = self.session.delete(endpoint, **kwargs)
        response.raise_for_status()

        return response.json()

