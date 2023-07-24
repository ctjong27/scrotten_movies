import requests
import os
import csv
import pandas as pd
from tqdm import tqdm

# Function to get information of a person using the TMDb API
def get_person(api_key, person_id):
    url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Getting the current working directory
cwd = os.getcwd()

# Define input and output file paths
input_file_path = os.path.join(cwd, 'data/tv_show_cast.csv')
output_file_path = os.path.join(cwd, 'data/tv_show_cast_details.csv')

# Check if output file already exists, and if so, exit
if os.path.exists(output_file_path):
    print("Output file already exists. Exiting.")
    exit()

# Reading the API key from the text file
with open(os.path.join(cwd, 'api_key.txt'), 'r') as file:
    api_key = file.read().strip()

# Load the cast data from the CSV file
cast_df = pd.read_csv(input_file_path)

# Get all unique cast ids, ordered in ascending order
unique_cast_ids = cast_df['cast_id'].unique()
unique_cast_ids.sort()

# Prepare data for CSV
csv_data = []

# Initialize progress bar
pbar = tqdm(total=len(unique_cast_ids))

# Process each person in the cast
for person_id in unique_cast_ids:
    person_data = get_person(api_key, person_id)

    if person_data:
        csv_data.append([
            person_data['id'],
            person_data['imdb_id'],
            person_data['name'],
            person_data['gender'],
            person_data['birthday'],
            person_data['deathday'],
            person_data['profile_path'],
        ])

    # Update progress bar
    pbar.update(1)

# Close progress bar
pbar.close()

# Write to CSV
with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'imdb_id', 'name', 'gender', 'birthday', 'deathday', 'profile_path'])  # Write header
    writer.writerows(csv_data)  # Write data
