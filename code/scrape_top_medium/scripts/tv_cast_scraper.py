import requests
import os
import pandas as pd
from tqdm import tqdm
import concurrent.futures

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
input_file_path = os.path.join(cwd, 'data', 'tv_show_to_cast.csv')
output_file_path = os.path.join(cwd, 'data', 'tv_show_cast_details.csv')

# Load the cast data from the CSV file
cast_df = pd.read_csv(input_file_path)

# Get all unique cast ids, ordered in ascending order
unique_cast_ids = cast_df['cast_id'].unique()
unique_cast_ids.sort()

# Load the existing data if file exists
if os.path.exists(output_file_path):
    output_data = pd.read_csv(output_file_path)
else:
    # Prepare DataFrame for output data
    output_data = pd.DataFrame(columns=['id', 'imdb_id', 'name', 'gender', 'birthday', 'deathday', 'profile_path'])

# Check if output file has same count as unique actors, if so skip remaining logic
if len(unique_cast_ids) == len(output_data):
    print("Output file already contains all unique actors. Exiting.")
    exit()

# Reading the API key from a text file
with open(os.path.join(cwd, 'api_key.txt'), 'r') as file:
    api_key = file.read().strip()

# Initialize progress bar
pbar = tqdm(total=len(unique_cast_ids))

# Define function to be run in a thread
def process_person(person_id):
    # If person already in output data, skip
    if person_id in output_data['id'].values:
        return None

    # Get person data
    person_data = get_person(api_key, person_id)

    if person_data:
        return person_data
    else:
        return None

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start threads for each person in the cast
    future_results = {executor.submit(process_person, person_id): person_id for person_id in unique_cast_ids}

    for future in concurrent.futures.as_completed(future_results):
        person_data = future.result()
        if person_data is not None:
            # Add data to DataFrame
            output_data.loc[len(output_data)] = [
                person_data['id'],
                person_data['imdb_id'],
                person_data['name'],
                person_data['gender'],
                person_data['birthday'],
                person_data['deathday'],
                person_data['profile_path']
            ]
        # Update progress bar
        pbar.update(1)

# Close progress bar
pbar.close()

# Write any remaining data to CSV
output_data.to_csv(output_file_path, index=False)
