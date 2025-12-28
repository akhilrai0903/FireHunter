# 🔥 FireHunter - Universal Firebase Exploit Toolkit

**FireHunter** is a proof-of-concept toolkit designed for security researchers and bug hunters to audit Firebase-backed Android applications. It automates the process of extracting authentication tokens, analyzing JWT permissions, and testing Firestore Security Rules for common misconfigurations (e.g., Insecure Direct Object References).

> ⚠️ **Disclaimer:** This tool is for educational purposes and authorized security testing only. Do not use this on applications without the owner's explicit permission.

## 🚀 Features
* **Universal Token Extraction:** Uses Frida to scan the Android file system (`shared_prefs`, `files`) for cached JWT tokens.
* **Token Analysis:** Instantly decodes JWTs to extract `Project ID`, `User ID`, and checks if the token is a valid Firebase Auth token or a Google OAuth token.
* **Blind Write Exploitation:** Exploits insecure Firestore Security Rules by sending "Blind PATCH" requests, bypassing client-side logic and timestamp checks.
* **Interactive CLI:** A user-friendly command-line interface to view data and modify Integer, Boolean, or String fields.

## 🛠️ Prerequisites
* Python 3.x
* Frida (`pip install frida-tools`)
* `requests` library (`pip install requests`)
* A rooted Android device or Emulator (with Frida Server running)

## 📖 Usage Guide

### Step 1: Extract the Token
Run the Frida script while the target app is open on your device.
```bash
frida -U -f com.target.package -l token_hunter.js
```
Copy the output starting with eyJ....

### Step 2: Analyze the Token
Paste the token into decoder.py to extract the Project configuration.

```Bash

python decoder.py
```
This will reveal the PROJECT_ID and USER_ID.

### Step 3: Launch the Attack
Update attack_bot.py with the credentials found in Step 2.

```Bash

python attack_bot.py
```
Option 1: View Profile (Scans for readable data).

Option 2: Blind Write (Forces an update to specific fields like coins, is_vip, etc.).


MIT License
