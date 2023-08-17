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
season_to_cast_path = os.path.join(data_folder, 'tv_show_season_to_cast.csv')

# Read CSV files into pandas DataFrames
cast_details_df = pd.read_csv(cast_details_path)
image_race_gender_df = pd.read_csv(image_race_gender_path)
season_to_cast_df = pd.read_csv(season_to_cast_path)

# Filter for only rows where the department is 'Acting'
season_to_cast_df = season_to_cast_df[season_to_cast_df['known_for_department'] == 'Acting']

# Merge DataFrames
merged_df = pd.merge(season_to_cast_df, cast_details_df[['id', 'gender']], left_on='cast_id', right_on='id', how='left')
merged_df = pd.merge(merged_df, image_race_gender_df[['id', 'profile_race', 'profile_gender']], left_on='cast_id', right_on='id', how='left')

# Normalize gender column
merged_df['gender'] = merged_df['gender'].map({1: 'Female', 2: 'Male', 0: 'Undetermined'})

# Combine profile_race and profile_gender into one column for the pivot later
merged_df['race_gender'] = merged_df['profile_race'] + "_" + merged_df['profile_gender']

# 1. Count the number of times each demographic group showed up in each season
counts_df = merged_df.groupby(['show_id', 'season_number', 'race_gender']).size().reset_index(name='counts')
pivot_df = counts_df.pivot_table(index=['show_id', 'season_number'], columns='race_gender', values='counts', fill_value=0)
pivot_df.columns = pivot_df.columns.get_level_values(0)
pivot_df.reset_index(inplace=True)
pivot_df.to_csv(os.path.join(data_folder, 'tv_season_race_gender_count_total.csv'), index=False)

# 2. Count the distinct number of individuals from each demographic group that showed up in each season
distinct_actors_df = merged_df.drop_duplicates(subset=['show_id', 'season_number', 'race_gender', 'cast_id'])
distinct_counts_df = distinct_actors_df.groupby(['show_id', 'season_number', 'race_gender']).size().reset_index(name='distinct_counts')
distinct_pivot_df = distinct_counts_df.pivot_table(index=['show_id', 'season_number'], columns='race_gender', values='distinct_counts', fill_value=0)
distinct_pivot_df.columns = distinct_pivot_df.columns.get_level_values(0)
distinct_pivot_df.reset_index(inplace=True)
distinct_pivot_df.to_csv(os.path.join(data_folder, 'tv_season_race_gender_count_distinct.csv'), index=False)
