from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["tip_platform"]

threat_collection = db["threat_intelligence"]

print("[+] Starting risk analysis...")

all_threats = threat_collection.find()

updated_count = 0

for threat in all_threats:

    score = 40

    source = threat.get("source", "")

    indicator = threat.get("indicator", "")

    # trusted feed gets higher confidence
    if source == "AlienVault":
        score += 30

    # suspicious network ranges example
    if indicator.startswith("185."):
        score += 15

    if indicator.startswith("103."):
        score += 10

    # random example logic
    if len(indicator) > 10:
        score += 5

    # maximum limit
    if score > 100:
        score = 100

    threat_collection.update_one(
        {"_id": threat["_id"]},
        {
            "$set": {
                "risk_score": score
            }
        }
    )

    updated_count += 1

print(f"[+] Updated {updated_count} threat scores.")