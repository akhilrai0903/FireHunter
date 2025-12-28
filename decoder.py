import json
import base64
import sys

# PASTE THE TOKEN YOU FOUND IN PHASE 1 HERE
TOKEN = "PASTE_YOUR_EYJ_TOKEN_HERE" 

def analyze_token(token):
    try:
        # Decode the payload (Middle part of the token)
        header, payload, signature = token.split('.')
        
        # Fix padding for Base64 decoding
        payload += '=' * (-len(payload) % 4)
        
        data = json.loads(base64.urlsafe_b64decode(payload))
        
        print("\n[+] --- TOKEN INTELLIGENCE ---")
        print(f"ISSUER:      {data.get('iss', 'Unknown')}")
        print(f"PROJECT ID:  {data.get('aud', 'Unknown')}") # This is your target Project
        print(f"USER ID:     {data.get('sub', 'Unknown')}") # This is your target User
        print(f"EXPIRATION:  {data.get('exp', 'Unknown')}")
        
        # Security Check
        if "securetoken.google.com" in data.get('iss', ''):
            print("\n✅ STATUS: VALID FIREBASE TOKEN. Ready for hacking.")
        elif "accounts.google.com" in data.get('iss', ''):
            print("\n⚠️ STATUS: GOOGLE OAUTH TOKEN DETECTED.")
            print("   This token might NOT work for database writes.")
            print("   Solution: Use 'Reqable' to capture the network request instead.")
        else:
            print("\n❓ STATUS: UNKNOWN TOKEN TYPE.")

    except Exception as e:
        print(f"[-] Invalid Token Format: {e}")

if __name__ == "__main__":
    analyze_token(TOKEN)
