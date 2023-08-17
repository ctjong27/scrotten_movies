import pandas as pd
import os
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

print("---")
print("Distinct TV Show Seasons")
print("---")

# Define your data folder
data_folder = './data'

# File paths
season_to_cast_path = os.path.join(data_folder, 'tv_show_season_to_cast.csv')

# Read CSV files into pandas DataFrames
season_to_cast_df = pd.read_csv(season_to_cast_path)

# Extract only the show_id, season_number, season_air_date, and season_vote_average columns
distinct_seasons_df = season_to_cast_df[['show_id', 'season_number', 'season_air_date', 'season_vote_average']].drop_duplicates()

# Save the DataFrame to a new CSV file
output_file_path = os.path.join(data_folder, 'tv_show_season_details.csv')
distinct_seasons_df.to_csv(output_file_path, index=False)

print(f"Distinct TV show seasons data saved to {output_file_path}")
