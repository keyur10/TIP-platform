import requests
from pymongo import MongoClient
from datetime import datetime

# AlienVault reputation feed
feed_url = "https://reputation.alienvault.com/reputation.data"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tip_platform"]
threat_collection = db["threat_intelligence"]

print("[+] Downloading threat feed...")

try:

    response = requests.get(feed_url, timeout=10)

    if response.status_code != 200:
        print("[-] Feed request failed")
        exit()

    raw_data = response.text.splitlines()

    added_count = 0

    for line in raw_data:

        # skip comments and empty lines
        if line.startswith("#") or line.strip() == "":
            continue

        try:

            ip_address = line.split("#")[0].strip()

            # basic validation
            if len(ip_address) < 7:
                continue

            threat_data = {
                "indicator": ip_address,
                "type": "ip",
                "source": "AlienVault",
                "risk_score": 85,
                "blocked": False,
                "created_at": datetime.utcnow()
            }

            # avoid duplicate entries
            existing = threat_collection.find_one({
                "indicator": ip_address
            })

            if not existing:

                threat_collection.insert_one(threat_data)
                added_count += 1

        except Exception as inner_error:
            print(f"[!] Skipped line: {inner_error}")

    print(f"[+] Finished. {added_count} new indicators added.")

except Exception as error:
    print(f"[-] Error: {error}")