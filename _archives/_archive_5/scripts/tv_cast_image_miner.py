import os
import pandas as pd
from deepface import DeepFace
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

print("---")
print("TV Cast Image Miner")
print("---")

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
input_file_path = os.path.join(cwd, 'data', 'tv_show_season_to_cast.csv')
output_file_path = os.path.join(cwd, 'data', 'tv_cast_image_race_gender.csv')

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
    output_data = pd.DataFrame(columns=['id', 'name', 'profile_path', 'profile_race', 'profile_gender'])

# Create a set for faster lookup
output_data_ids = set(output_data['id'])

# Check if output file has same count as unique actors, if so skip remaining logic
if len(unique_cast_ids) == len(output_data):
    print("Output image proc file already contains all unique actors. Exiting.")
    exit()

# Initialize progress bar
pbar = tqdm(total=len(unique_cast_ids))

# # Reading the API key from a text file
# with open(os.path.join(cwd, 'api_key.txt'), 'r') as file:
#     api_key = file.read().strip()
api_key = config.get('API', 'api_key')

# Process each person in the cast
for i, person_id in enumerate(unique_cast_ids):
    # If person already in output data, skip
    if person_id in output_data_ids:
        pbar.update(1)
        continue

    # Get person data
    person_data = get_person(api_key, person_id)

    if person_data:
        result_dict = {
            'id': person_data['id'],
            'name': person_data['name'],
            'profile_path': person_data['profile_path'],
            'profile_race': None,
            'profile_gender': None,
        }

        # Infer race and gender from image
        try:
            if pd.notna(person_data['profile_path']):
                img_path = f'https://image.tmdb.org/t/p/w300_and_h450_bestv2/{person_data["profile_path"]}'
                response = requests.get(img_path)
                # img = Image.open(BytesIO(response.content))
                result = DeepFace.analyze(img_path, actions=['race', 'gender'], enforce_detection=False)

                if isinstance(result, list):
                    result_dict["profile_race"] = result[0]["dominant_race"]
                    gender_dict = result[0]["gender"]
                else:
                    result_dict["profile_race"] = result["dominant_race"]
                    gender_dict = result["gender"]

                if gender_dict['Man'] >= 75:
                    result_dict["profile_gender"] = "Male"
                elif gender_dict['Woman'] >= 75:
                    result_dict["profile_gender"] = "Female"
                else:
                    result_dict["profile_gender"] = "Undetermined"

        except Exception as e:
            print(f'Error analyzing image for id {person_data["id"]}: {e}')

        # Append the results to the output DataFrame
        result_df = pd.DataFrame([result_dict])
        output_data = pd.concat([output_data, result_df], ignore_index=True)

        # Add the new id to the set
        output_data_ids.add(person_id)

        # Write to CSV every 100 entries or at the end
        if (i + 1) % 100 == 0 or (i + 1) == len(unique_cast_ids):
            output_data.to_csv(output_file_path, index=False)

    # Update progress bar
    pbar.update(1)

# Close progress bar
pbar.close()

# Write any remaining data to CSV
output_data.to_csv(output_file_path, index=False)
