from T212_Super import Client
import time
import json

client = Client()

def ReadableJSON(arg):
    return json.dumps(arg, indent=3, sort_keys=False)

x = ReadableJSON(client.positions.getPositions())

#x = ReadableJSON(client.account.summary())

print(x)