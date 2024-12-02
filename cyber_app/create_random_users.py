import json
import random
import string

common_passwords = [
    "123456", "password", "123456789", "12345678", "12345", "1234567", "qwerty", "abc123", "111111", "123123"
]

def generate_simple_password():
    return random.choice(common_passwords)

def generate_medium_password():
    length = random.randint(6, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_strong_password():
    length = random.randint(10, 15)
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

def generate_users(num_users=3000):
    users = []
    categories = {"simple": [], "medium": [], "strong": []}

    for i in range(1, num_users + 1):
        login = f"user{i}"
        email = f"user{i}@example.com"

        complexity = random.choices(["simple", "medium", "strong"], weights=[0.4, 0.4, 0.2], k=1)[0]

        if complexity == "simple":
            password = generate_simple_password()
        elif complexity == "medium":
            password = generate_medium_password()
        else:
            password = generate_strong_password()

        users.append({"login": login, "password": password, "email": email})
        categories[complexity].append(login)

    return users, categories

def save_to_json(users, filename="users.json"):
    with open(filename, "w") as file:
        json.dump(users, file, indent=4)

def save_to_text_report(categories, filename="password_complexity_report.txt"):
    with open(filename, "w") as file:
        for category, logins in categories.items():
            file.write(f"Category: {category.capitalize()} ({len(logins)} users)\n")
            file.write("\n".join(logins))
            file.write("\n\n")

if __name__ == "__main__":
    num_users = 3000
    users, categories = generate_users(num_users)
    save_to_json(users)
    save_to_text_report(categories)
    print(f"{num_users} users generated and saved to 'users.json' and 'password_complexity_report.txt'.")
