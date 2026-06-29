from pymongo import MongoClient
from elasticsearch import Elasticsearch
import urllib3
from datetime import datetime

urllib3.disable_warnings()

print("[+] Connecting to Elasticsearch...")

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "UnBte7k5E2Z+gzbEL5Rr"),
    verify_certs=False
)

print("[+] Connecting to MongoDB...")

mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client["tip_platform"]

collection = db["threat_intelligence"]

all_threats = collection.find()

indexed_count = 0

for threat in all_threats:

    try:

        threat.pop("_id", None)

        # Add timestamp for Kibana timeline
        threat["created_at"] = datetime.utcnow()

        es.index(
            index="threat-intelligence",
            document=threat
        )

        indexed_count += 1

        print(f"[+] Indexed Threat: {threat.get('indicator', 'Unknown')}")

    except Exception as error:

        print(f"[-] Failed: {error}")

print(f"\n[+] Successfully Indexed {indexed_count} Threat Records")