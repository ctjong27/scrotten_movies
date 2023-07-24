import os
import pandas as pd
from deepface import DeepFace
import requests
from PIL import Image
from io import BytesIO
from google.colab import drive
import json

# Mount your Google Drive
drive.mount('/content/drive')

# Path to the CSV file on Google Drive
file_path = '/content/drive/MyDrive/Projects/scrotten_movies/tv_show/'
read_file = 'tv_show_cast_details.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path + read_file)

# Counter variables
total_persons = len(data)
persons_analyzed = 0

def process_row(row, results_df):
    # Check if the race and gender for this person have been previously determined
    if not results_df[results_df['id'] == row['id']].empty:
        return results_df

    result_dict = {
        'id': row['id'],
        'name': row['name'],
        'profile_path': row['profile_path'],
        'profile_race': None,
        'profile_gender': None,
    }

    # Infer race and gender from image
    try:
        if pd.notna(row['profile_path']):
            img_path = f'https://image.tmdb.org/t/p/w300_and_h450_bestv2/{row["profile_path"]}'
            response = requests.get(img_path)
            img = Image.open(BytesIO(response.content))
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
        print(f'Error analyzing image for row {row["id"]}: {e}')

    # Append the results to the results DataFrame
    results_df = results_df.append(result_dict, ignore_index=True)

    return results_df


# Initialize or load the results DataFrame
write_file = 'tv_cast_image_race_gender.csv'
results_file_path = file_path + write_file

if os.path.exists(results_file_path):
    # Load the existing results file
    results_df = pd.read_csv(results_file_path)
else:
    # Create an empty DataFrame to store the results
    results_df = pd.DataFrame(columns=['id', 'name', 'profile_path', 'profile_race', 'profile_gender'])

# Process each row in the data frame using a standard loop
for _, row in data.iterrows():
    results_df = process_row(row, results_df)

    # Increment the counter
    persons_analyzed += 1

    # Print progress
    print(f"Persons Analyzed: {persons_analyzed}/{total_persons}")

    # Write the results DataFrame to a CSV file every 100 iterations
    if persons_analyzed % 100 == 0:
        results_df.to_csv(results_file_path, index=False)

# Print newline character after completion
print()

# Save the final results to the file
results_df.to_csv(results_file_path, index=False)
