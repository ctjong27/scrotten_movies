import pandas as pd
import os

print("---")
print("Gender Proessor")
print("---")

data_folder = './data' # replace with your data folder if necessary

# File paths
cast_details_path = os.path.join(data_folder, 'tv_show_cast_details.csv')
image_race_gender_path = os.path.join(data_folder, 'tv_cast_image_race_gender.csv')

# Load dataframes
df_cast_details = pd.read_csv(cast_details_path)[['id', 'gender']] # Only load 'id' and 'gender' columns
df_image_race_gender = pd.read_csv(image_race_gender_path)[['id', 'profile_gender']] # Only load 'id' and 'profile_gender' columns

# Merge the two dataframes on 'id'
df = pd.merge(df_cast_details, df_image_race_gender, on='id', how='left')

# Create a mapping of gender values in the 'gender' column to 'Male', 'Female', and 'Other'
gender_map = {1: 'Female', 2: 'Male', 0: 'Other'}
df['gender'] = df['gender'].map(gender_map)

# Fill in the gender from 'profile_gender' where it's not 'Male' or 'Female' in 'gender'
df.loc[~df['gender'].isin(['Male', 'Female']), 'gender'] = df['profile_gender']

# Filter the dataframe to include only rows where the gender data is available
df = df[df['gender'].notna()]

# Save the dataframe to a new CSV file, only including 'id' and 'gender' columns
df[['id', 'gender']].to_csv(os.path.join(data_folder, 'tv_show_cast_processed_gender.csv'), index=False)
