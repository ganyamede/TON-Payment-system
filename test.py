from core.storage.database import Database
from core.blockchain.payment_checker import SaveWallet, UpdateWallet
db = Database().db

db.execute('''CREATE TABLE IF NOT EXISTS ton (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT,
    mnemonic TEXT,
    value INTEGER,
    state TEXT
)''')

# UpdateWallet(1)

# import requests

# url = "http://127.0.0.1/Check/"
# params = {
#     "address": "EQCvWPnR7VI0FflxHhX1gX2dRxkB9UmFqBg3OgoBnnq7mbbG"
# }

# response = requests.post(url, data=params)

# print(response.json()[0][1])

print(*["state", "shoot", "flip", "open", "protect", "scorpion", "jaguar", "notable", "enter", "elder", "valve", "piano", "tide", "road", "spray", "olive", "cement", "rude", "punch", "lens", "meat", "lock", "drama", "endless"])