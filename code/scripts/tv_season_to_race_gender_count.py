import pandas as pd
import os
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Define your data folder
data_folder = './data'

print("---")
print("tv_season_to_race_gender_count")
print("---")

# File paths
cast_details_path = os.path.join(data_folder, 'tv_show_cast_details.csv')
image_race_gender_path = os.path.join(data_folder, 'tv_cast_image_race_gender.csv')
top_shows_yearly_path = os.path.join(data_folder, f'tv_shows_top_{config.get("General", "total_shows_per_year")}_yearly.csv')
season_to_cast_path = os.path.join(data_folder, 'tv_show_season_to_cast.csv')

# Read CSV files into pandas DataFrames
cast_details_df = pd.read_csv(cast_details_path)
image_race_gender_df = pd.read_csv(image_race_gender_path)
top_shows_yearly_df = pd.read_csv(top_shows_yearly_path)
season_to_cast_df = pd.read_csv(season_to_cast_path)

# Merge DataFrames
merged_df = pd.merge(season_to_cast_df, cast_details_df[['id', 'gender']], left_on='cast_id', right_on='id', how='left')
merged_df = pd.merge(merged_df, image_race_gender_df[['id', 'profile_race', 'profile_gender']], left_on='cast_id', right_on='id', how='left')
merged_df = pd.merge(merged_df, top_shows_yearly_df[['id', 'name']], left_on='show_id', right_on='id', how='left')

# Normalize gender column
merged_df['gender'] = merged_df['gender'].map({1: 'Female', 2: 'Male', 0: 'Undetermined'})

# Combine profile_race and profile_gender into one column for the pivot later
merged_df['race_gender'] = merged_df['profile_race'] + "_" + merged_df['profile_gender']

# Get counts of each combination of show_id, season_number, and race_gender
counts_df = merged_df.groupby(['show_id', 'season_number', 'race_gender']).size().reset_index(name='counts')

# Pivot the counts DataFrame to put each unique combination of race and gender into its own column
pivot_df = counts_df.pivot_table(index=['show_id', 'season_number'], columns='race_gender', values='counts', fill_value=0)

# Flatten the MultiIndex in columns and reset the index
pivot_df.columns = pivot_df.columns.get_level_values(0)
pivot_df.reset_index(inplace=True)

# Save the DataFrame to a new CSV file
pivot_df.to_csv(os.path.join(data_folder, 'tv_season_to_race_gender_count.csv'), index=False)
