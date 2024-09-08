import datetime
import logging
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from paths import data_dir

from server_addresses import generate_links

logging.basicConfig(level=logging.INFO)

links = generate_links(
    root="https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n3125/",
    months = ['aug'],
    years=['2013', '2014', '2015', '2016', '2017', '2018', '2019',
              '2020', '2021', '2022', '2023', '2024'],
    today=datetime.date.today()
    # months=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
    # years=['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
    #        '2020', '2021', '2022', '2023', '2024']
)

# Directory to save the downloaded files
download_dir = data_dir
os.makedirs(download_dir, exist_ok=True)


for link in links:

    logging.info(f"Downloading {link}...")
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):

        if a['href'].endswith("-v5.4.hdf"):
            file_name = a['href']
            file_url = link + file_name
            file_path = os.path.join(download_dir, file_name)

            # if the file already exists, skip it to be kind to the poor server
            if os.path.exists(file_path):
                logging.info(f"File {file_name} already exists. Skipping...")
                continue

            logging.info(f"Downloading {file_url}...")
            response = requests.get(file_url, stream=True)

            with open(file_path, 'wb') as file:
                #dont use tdqm
                for chunk in response.iter_content(chunk_size=1024*10):
                    file.write(chunk)

