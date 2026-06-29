from pymongo import MongoClient
import subprocess
import time

print("[+] Dynamic Policy Enforcer Started")

mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client["tip_platform"]

collection = db["threat_intelligence"]

already_blocked = set()

while True:

    print("\n[+] Checking database for threats...")

    try:

        total_records = collection.count_documents({})

        print(f"[+] Total Threat Records Found: {total_records}")

        threats = collection.find({
            "risk_score": {"$gte": 1}
        })

        found_any = False

        for threat in threats:

            found_any = True

            ip = threat.get("ip") or threat.get("indicator")

            if not ip:

                print("[-] No IP found in record")
                continue

            source = threat.get("source", "Unknown Source")

            print(f"[+] Threat detected from source: {source}")

            if ip in already_blocked:

                print(f"[!] Already blocked: {ip}")
                continue

            print(f"[!] Blocking malicious IP: {ip}")

            try:

                command = (
                    f'netsh advfirewall firewall add rule '
                    f'name="BLOCK_{ip}" dir=in action=block remoteip={ip}'
                )

                subprocess.run(command, shell=True)

                already_blocked.add(ip)

                print(f"[+] Successfully blocked {ip}")

            except Exception as error:

                print(f"[-] Failed to block {ip}: {error}")

        if not found_any:

            print("[-] No matching threats found")

    except Exception as database_error:

        print(f"[-] MongoDB Error: {database_error}")

    print("[+] Waiting 30 seconds...\n")

    time.sleep(30)