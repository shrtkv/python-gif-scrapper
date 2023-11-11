import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm

def get_base_url(url):
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
        with tqdm(total=len(gifs), unit='file', desc="Downloading GIFs", ncols=100) as pbar:
            for gif in gifs:
                gif_url = gif['src']
                if not gif_url.startswith(('http://', 'https://')):
                    gif_url = f"{base_url}/{gif_url}"

                try:
                    gif_name = gif_url.split('/')[-1]
                    gif_data = requests.get(gif_url, stream=True)
                    with open(f"{save_path}/{gif_name}", 'wb') as file:
                        for chunk in gif_data.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                file.flush()
                    pbar.update(1)
                except Exception as e:
                    print(f"Failed to download {gif_url}: {e}")

        print(f"Download complete. GIFs saved in {save_path}/")

url = input("Enter the URL of the website: ")
base_url = get_base_url(url)
save_path = create_new_directory("gifs")
download_gifs(url, base_url, save_path)

