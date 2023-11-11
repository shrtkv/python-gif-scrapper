import requests
from bs4 import BeautifulSoup
import os

def download_gifs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    gif_urls = [img['src'] for img in images if img['src'].endswith('.gif')]

    print(f"Found {len(gif_urls)} GIFs. Proceed with download? (y/n)")
    confirm = input()
    if confirm.lower() != 'y':
        print("Aborted.")
        return

    dir_name = "gifs"
    counter = 1
    while os.path.exists(dir_name):
        dir_name = f"gifs-{counter}"
        counter += 1
    os.makedirs(dir_name)

    for i, gif_url in enumerate(gif_urls):
        try:
            gif_data = requests.get(gif_url).content
            file_path = os.path.join(dir_name, f"gif_{i}.gif")
            with open(file_path, 'wb') as file:
                file.write(gif_data)
        except Exception as e:
            print(f"Failed to download {gif_url}: {e}")

    print(f"Download complete. GIFs saved in {dir_name}/")

input_url = input("Enter the URL of the website: ")
download_gifs(input_url)

