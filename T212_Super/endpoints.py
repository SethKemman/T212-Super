import os
from dotenv import load_dotenv

load_dotenv()
MODE = (os.getenv("MODE") or "").upper()
    # Bepaal de juiste base URL
if MODE == "LIVE":
    BASE_URL = "https://live.trading212.com/api/v0"
elif MODE == "DEMO":
    BASE_URL = "https://demo.trading212.com/api/v0"
else:
    raise ValueError(f"Onbekende MODE '{MODE}', kies 'DEMO' of 'LIVE'.")

class Endpoints:
    BASE = BASE_URL

    #Account
    ACCOUNT_SUMMARY = f"{BASE}/equity/account/summary" #GET

    #Instruments
    METADATA_EXCHANGES = f"{BASE}/equity/metadata/exchanges" #GET
    METADATA_INSTRUMENTS = f"{BASE}/equity/metadata/instruments" #GET

    #Orders
    ORDERS = f"{BASE}/equity/orders" #GET
    LIMITORDER = f"{BASE}/equity/orders/limit" #POST; requires payload
    MARKETORDER = f"{BASE}/equity/orders/market" #POST; requires payload
    STOPORDER = f"{BASE}/equity/orders/stop" #POST; requires payload
    STOPLIMITORDER = f"{BASE}/equity/orders/stop_limit" #POST; requires payload
    #CANCELORDER = f"{BASE}/equity/orders/" + id #DELETE; requires id of order. -FIX LATER
    #GETORDER = f"{BASE}/equity/orders/" + id #GET; requires id of order. -FIX LATER

    #Positions
    POSITIONS = f"{BASE}/equity/positions" #GET; requires query

    #Historical Events - TO BE ADDED

