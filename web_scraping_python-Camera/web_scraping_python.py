import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=camara"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds


for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
phone_cards = soup.find_all("div", class_="s-result-item")

phone_data = []

for phone_card in phone_cards:
    try:
        phone_name = phone_card.find("span", class_="a-text-normal").text.strip()
        phone_price = phone_card.find("span", class_="a-offscreen").text if phone_card.find("span", class_="a-offscreen") else "N/A"
        phone_rating = phone_card.find("span", class_="a-icon-alt").text if phone_card.find("span", class_="a-icon-alt") else "N/A"
        
        phone_data.append({
            "Name": phone_name,
            "Price": phone_price,
            "Rating": phone_rating
        })
    except Exception as e:
        print("Error in extracting phone data:", e)

df = pd.DataFrame(phone_data)
df.to_csv("amazon_Camera.csv", index=False)

print("Data successfully extracted and CSV saved.")