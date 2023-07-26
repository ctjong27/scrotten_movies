import requests
import csv
import os
import pathlib
from tqdm import tqdm
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

print("---")
print("TV Show Detail Miner")
print("---")

# Configuration
num_top_shows = int(config.get('General', 'total_shows_per_year'))  # Desired number of top shows here
start_year = int(config.get('General', 'start_year'))  # Start year for the data
end_year = int(config.get('General', 'end_year'))  # End year for the data

# Get current working directory
cwd = os.getcwd()

# File path for the data
file_path = os.path.join(cwd, f'data/tv_shows_top_{num_top_shows}_yearly.csv')

# Check if file already exists
if os.path.exists(file_path):
    print("File already exists. Skipping...")
else:
    # Create data directory if it does not exist
    os.makedirs(os.path.join(cwd, 'data'), exist_ok=True)

    # with open(os.path.join(cwd, 'api_key.txt'), 'r') as file:
    #     api_key = file.read().strip()
    api_key = config.get('API', 'api_key')

    # Prepare data for CSV
    csv_data = []

    # Initialize progress bar
    pbar = tqdm(total=(end_year-start_year+1)*num_top_shows)

    for year in range(start_year, end_year+1):
        page = 1
        shows_filtered = []

        while len(shows_filtered) < num_top_shows:
            url = f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&language=en-US&sort_by=popularity.desc&first_air_date_year={year}&region=US&page={page}"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                shows = data['results']

                # Filter shows based on original_language and origin_country
                shows_filtered += [show for show in shows if show['original_language'] == 'en' and 'US' in show['origin_country']]

                page += 1
            else:
                print("Error:", response.status_code)
                break

        for i, show in enumerate(shows_filtered[:num_top_shows], start=1):
            # Get last_air_date for the show
            show_url = f"https://api.themoviedb.org/3/tv/{show['id']}?api_key={api_key}"
            show_response = requests.get(show_url)
            if show_response.status_code == 200:
                show_data = show_response.json()
                last_air_date = show_data['last_air_date']
            else:
                print(f"Error getting show details: {show_response.status_code}")
                last_air_date = "NA"

            csv_data.append([year,
                            show['name'],
                            show['id'],
                            ", ".join([str(id) for id in show['genre_ids']]),
                            show['first_air_date'],
                            last_air_date,
                            ", ".join(show['origin_country']), 
                            show['vote_average'], 
                            show['popularity']])
            
            # Update progress bar
            pbar.update(1)

    # Close progress bar
    pbar.close()

    # Write to CSV in the data directory in the root directory
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["year", "name", "id", "genres", "first_air_date", "last_air_date", "origin_country", "rating", "popularity"])  # Write header
        writer.writerows(csv_data)  # Write data
