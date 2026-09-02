from T212_Super import Client

client = Client()

summary = client.account.summary()

positions = client.positions.getPositions()
print(positions)