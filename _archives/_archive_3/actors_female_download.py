import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from tqdm import tqdm

def scrape_page(url):
    names = []
    links = []
    ids = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lister_items = soup.find_all('div', class_='lister-item-content')

    for item in lister_items:
        name_tag = item.find('h3', class_='lister-item-header').find('a')
        name = name_tag.text.strip()
        link = name_tag['href']
        id = link.split('/')[2]
        names.append(name)
        links.append(link)
        ids.append(id)

    return names, links, ids

def get_imdb_info(start_url, output_file, test_mode=False, max_pages=10):
    # Get total number of names (for non-test mode)
    if not test_mode:
        soup = BeautifulSoup(requests.get(start_url).text, "html.parser")  # parser
        desc = soup.find('div', class_='desc').get_text()
        total_names_str = re.search(r"of ([\d,]+)", desc).group(1)  # Extract total number of names
        total_names = int(total_names_str.replace(',', ''))  # Remove comma and convert to int
        max_pages = (total_names // 250) + 1  # Calculate total pages, assuming 250 names per page
        print(f"total_names: {total_names}")
        print(f"max_pages: {max_pages}")

    for page in range(1, max_pages + 1):
        page_url = f"{start_url}&start={250*(page-1)+1}&ref_=adv_nxt"
        names, links, ids = scrape_page(page_url)

        df = pd.DataFrame({
            'ID': ids,
            'Link': links,
            'Name': names,
        })

        # Check if the CSV file already exists
        if os.path.isfile(output_file):
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df.to_csv(output_file, index=False)

        print(f"Page {page} of {max_pages} out of {total_names} names scraped and data appended to CSV file.")

        # # Wait for 2 seconds between requests
        # time.sleep(2)

def main():
    # Specify the gender
    gender = 'female'

    # Specify the start URL based on the gender
    start_url = f'https://www.imdb.com/search/name/?gender={gender}&sort=alpha,asc&count=250'

    # Get the current directory path
    current_directory = os.getcwd()

    # Create a folder based on the gender in the current directory if it doesn't exist
    folder_name = f'{current_directory}/actors_by_gender/{gender}'
    os.makedirs(folder_name, exist_ok=True)

    # Specify the output file path for saving the data
    output_file = f'{folder_name}/{gender}_actors.csv'

    # Scrape the IMDb info
    get_imdb_info(start_url, output_file, test_mode=False)

    print(f"Scraped and saved data for {gender} actors in folder {folder_name}")

if __name__ == "__main__":
    main()
