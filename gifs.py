import os
import requests
from bs4 import BeautifulSoup

def get_base_url(url):
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def create_new_directory(base_path):
    counter = 1
    new_path = base_path
    while os.path.exists(new_path):
        new_path = f"{base_path}-{counter}"
        counter += 1
    os.makedirs(new_path)
    return new_path

def download_gifs(url, base_url, save_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gifs = soup.find_all('img', {'src': lambda x: x and x.endswith('.gif')})

    print(f"Found {len(gifs)} GIFs. Proceed with download? (y/n)")
    if input().lower() == 'y':
        for gif in gifs:
            gif_url = gif['src']
            if not gif_url.startswith(('http://', 'https://')):
                gif_url = f"{base_url}/{gif_url}"

            try:
                gif_data = requests.get(gif_url)
                gif_name = gif_url.split('/')[-1]
                with open(f"{save_path}/{gif_name}", 'wb') as file:
                    file.write(gif_data.content)
            except Exception as e:
                print(f"Failed to download {gif_url}: {e}")

        print(f"Download complete. GIFs saved in {save_path}/")

url = input("Enter the URL of the website: ")
base_url = get_base_url(url)
save_path = create_new_directory("gifs")
download_gifs(url, base_url, save_path)

