from T212_Super import Client
import time

client = Client()

positions = client.positions.getPositions()
print(positions)