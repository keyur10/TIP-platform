from pymongo import MongoClient

print("[+] Connecting to MongoDB...")

client = MongoClient("mongodb://localhost:27017/")

db = client["tip_platform"]

collection = db["threat_intelligence"]

test_threat = {

    "ip": "185.220.101.1",

    "source": "AlienVault OTX",

    "threat_type": "Botnet",

    "risk_score": 95
}

collection.insert_one(test_threat)

print("[+] Fake malicious threat inserted successfully")