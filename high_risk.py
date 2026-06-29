from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["tip_platform"]

threat_collection = db["threat_intelligence"]

print("[+] Fetching high-risk indicators...\n")

high_risk = threat_collection.find({
    "risk_score": {
        "$gte": 80
    }
})

count = 0

for threat in high_risk:

    print(f"[!] High Risk IP: {threat['indicator']}")

    count += 1

print(f"\n[+] Total high-risk indicators: {count}")