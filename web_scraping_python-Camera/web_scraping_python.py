import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=camera"  # Corrected the typo in the URL

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

camara_data = []  # Initialize the data list outside the loop

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
camera_cards = soup.find_all("div", class_="s-result-item")

for camera_card in camera_cards:
    try:
        camera_name = camera_card.find("span", class_="a-text-normal").text.strip()
        camera_price = camera_card.find("span", class_="a-price-whole").text if camera_card.find("span", class_="a-price-whole") else "N/A"  # Corrected the class name for price
        camera_rating = camera_card.find("span", class_="a-icon-alt").text if camera_card.find("span", class_="a-icon-alt") else "N/A"
        
        camara_data.append({
            "Name": camera_name,
            "Price": camera_price,
            "Rating": camera_rating
        })
    except Exception as e:
        print("Error in extracting camera data:", e)

df = pd.DataFrame(camara_data)  # Corrected variable name from camara_data to camera_data
df.to_csv("amazon_Camera.csv", index=False)

print("Data successfully extracted and CSV saved.")
