# test_connection.py (DÜZELTİLMİŞ VERSİYON - follow_redirects)
import httpx
import ssl
import certifi

url = "https://openlibrary.org/isbn/9780441172719.json"
print(f"Default SSL Certificate Path (ssl): {ssl.get_default_verify_paths().cafile}")
print(f"Certifi SSL Certificate Path: {certifi.where()}")
print("---------------------------------")

# --- TEST 1: NORMAL BAĞLANTI ---
print("--- Running Test 1: Standard HTTPS Connection ---")
try:
    # DOĞRU PARAMETRE: follow_redirects=True
    response = httpx.get(url, timeout=30.0, follow_redirects=True)
    print(f"[TEST 1] Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("[TEST 1] SUCCESS! Standard connection works.")
    else:
        print(f"[TEST 1] FAILED! Server responded with status: {response.status_code}")
        print(f"[TEST 1] Response text: {response.text[:200]}...")

except Exception as exc:
    print(f"[TEST 1] CRITICAL ERROR: Could not connect.")
    print(f"[TEST 1] Error details: {exc}")

print("\n---------------------------------\n")

# --- TEST 2: SSL DOĞRULAMASI OLMADAN BAĞLANTI ---
print("--- Running Test 2: Connection WITHOUT SSL Verification (for debugging) ---")
try:
    # DOĞRU PARAMETRE: follow_redirects=True
    # verify=False parametresi sertifika kontrolünü atlar
    response = httpx.get(url, timeout=30.0, follow_redirects=True, verify=False)
    print(f"[TEST 2] Status Code: {response.status_code}")

    if response.status_code == 200:
        print("[TEST 2] SUCCESS! Connection works when SSL verification is disabled.")
        print("[TEST 2] This strongly indicates a local SSL certificate or firewall issue.")
    else:
        print(f"[TEST 2] FAILED even without SSL verification. Status: {response.status_code}")

except Exception as exc:
    print(f"[TEST 2] CRITICAL ERROR: Could not connect even without SSL verification.")
    print(f"[TEST 2] Error details: {exc}")

print("\n---------------------------------")
print("Test finished.")