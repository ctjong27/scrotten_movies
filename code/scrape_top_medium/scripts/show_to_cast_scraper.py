import requests
import os
import csv
import json
import pandas as pd
from tqdm import tqdm

# Function to get the list of cast members from a TV show
def get_cast(api_key, show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}/aggregate_credits?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['cast']
    else:
        print(f"Error: {response.status_code}")
        return None

# Getting the current working directory
cwd = os.getcwd()

# Reading the API key from the text file
with open(os.path.join(cwd, 'api_key.txt'), 'r') as file:
    api_key = file.read().strip()

# Load the TV show data from the CSV file
tv_shows = pd.read_csv(os.path.join(cwd, 'data', 'tv_shows_top_25_yearly.csv'))

# Prepare data for CSV
csv_data = []

# Initialize progress bar
pbar = tqdm(total=len(tv_shows))

# Process each TV show
for _, show in tv_shows.iterrows():
    show_id = int(show['id'])  # 'id' is the column header in the CSV
    cast = get_cast(api_key, show_id)

    if cast:
        for actor in cast:
            csv_data.append([show_id, actor['name'], actor['total_episode_count']])
    
    # Update progress bar
    pbar.update(1)

# Close progress bar
pbar.close()

# Write to CSV
with open(os.path.join(cwd, 'data', 'tv_show_cast.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Show ID", "Actor Name", "Episode Count"])  # Write header
    writer.writerows(csv_data)  # Write data
