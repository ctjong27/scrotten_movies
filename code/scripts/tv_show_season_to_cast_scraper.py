import requests
import os
import csv
import pandas as pd
from tqdm import tqdm
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

print("---")
print("TV Show Season To Cast Scraper")
print("---")

# Function to get the list of seasons for a TV show
def get_seasons(api_key, show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['seasons']
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to get the list of cast and crew from a TV show season
def get_season_cast(api_key, show_id, season_number):
    url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/aggregate_credits?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['cast'], data['crew']
    else:
        print(f"Error: {response.status_code}")
        return None, None

# Getting the current working directory
cwd = os.getcwd()

# Define output file path
output_file_path = os.path.join(cwd, 'data', 'tv_show_season_to_cast.csv')

# Check if output file already exists, and if so, exit
if os.path.exists(output_file_path):
    print("Output file already exists. Exiting.")
    exit()

# Reading the API key from the configuration
api_key = config.get('API', 'api_key')

# Load the TV show data from the CSV file
tv_shows = pd.read_csv(os.path.join(cwd, 'data', f'tv_shows_top_{config.get("General", "total_shows_per_year")}_yearly.csv'))

# Prepare data for CSV
csv_data = []

# Initialize progress bar
pbar = tqdm(total=len(tv_shows))

# Process each TV show
for _, show in tv_shows.iterrows():
    show_id = int(show['id'])  # 'id' is the column header in the CSV
    seasons = get_seasons(api_key, show_id)

    if seasons:
        for season in seasons:
            season_number = season['season_number']
            season_air_date = season['air_date']
            season_vote_average = season.get('vote_average', 'N/A')  # Fetch vote_average
            cast, crew = get_season_cast(api_key, show_id, season_number)

            if cast:
                for actor in cast:
                    csv_data.append([show_id, season_number, actor['id'], actor['name'], actor['total_episode_count'], actor['known_for_department'], season_air_date, season_vote_average])

            if crew:
                for crew_member in crew:
                    csv_data.append([show_id, season_number, crew_member['id'], crew_member['name'], crew_member['total_episode_count'], crew_member['known_for_department'], season_air_date, season_vote_average])
    
    # Update progress bar
    pbar.update(1)

# Close progress bar
pbar.close()

# Write to CSV
with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['show_id', 'season_number', 'cast_id', 'cast_name', 'episode_count', 'known_for_department', 'season_air_date', 'season_vote_average'])  # Write header
    writer.writerows(csv_data)  # Write data
