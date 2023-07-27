# Read in data from tv_shows_top_25_yearly.csv
# Export data into tv_export_data.csv

# join data from
# tv_cast_image_race_gender.csv
# id,name,profile_path,profile_race,profile_gender
# 1,George Lucas,/WCSZzWdtPmdRxH9LUCVi2JPCSJ.jpg,white,Undetermined
# 2,Mark Hamill,/2ZulC2Ccq1yv3pemusks6Zlfy2s.jpg,latino hispanic,Male
# 3,Harrison Ford,/ActhM39LTxgx3tnJv3s5nM6hGD1.jpg,white,Male
# 4,Carrie Fisher,/utKPqWm9MAcL6NqN0Kd71dWUmXM.jpg,white,Female
# 6,Anthony Daniels,/7kR4kwXtvXtvrsxWeX3QLX5NS5V.jpg,white,Male
# 11,David Reynolds,/5iKtATPbLpv2lT7q9DPX2v2qPS1.jpg,white,Male

# tv_show_cast_details.csv
# id,imdb_id,name,gender,birthday,deathday,profile_path
# 1,nm0000184,George Lucas,2,1944-05-14,,/WCSZzWdtPmdRxH9LUCVi2JPCSJ.jpg
# 2,nm0000434,Mark Hamill,2,1951-09-25,,/2ZulC2Ccq1yv3pemusks6Zlfy2s.jpg
# 3,nm0000148,Harrison Ford,2,1942-07-13,,/ActhM39LTxgx3tnJv3s5nM6hGD1.jpg
# 4,nm0000402,Carrie Fisher,1,1956-10-21,2016-12-27,/utKPqWm9MAcL6NqN0Kd71dWUmXM.jpg
# 6,nm0000355,Anthony Daniels,2,1946-02-21,,/7kR4kwXtvXtvrsxWeX3QLX5NS5V.jpg
# 11,nm0721675,David Reynolds,2,1966-08-10,,/5iKtATPbLpv2lT7q9DPX2v2qPS1.jpg
# 12,nm1071252,Alexander Gould,2,1994-05-04,,/fe4mUSp0XotA6Ku4Bs69Q9o2lqU.jpg

# tv_show_season_to_cast.csv
# show_id,season_number,cast_id,cast_name,episode_count,known_for_department,season_air_date
# 734,1,15112,Tom Selleck,18,Acting,1980-12-11
# 734,1,12296,John Hillerman,18,Acting,1980-12-11
# 734,1,42156,Roger E. Mosley,18,Acting,1980-12-11
# 734,1,159648,Larry Manetti,18,Acting,1980-12-11
# 734,1,1219196,Jeff MacKay,5,Acting,1980-12-11
# 734,1,6839,Fritz Weaver,2,Acting,1980-12-11
# 734,1,151423,Pamela Susan Shoop,2,Acting,1980-12-11
# 734,1,2249,Clyde Kusatsu,2,Acting,1980-12-11
# 734,1,1162,Robert Loggia,2,Acting,1980-12-11
# 734,1,6972,Ian McShane,1,Acting,1980-12-11

# tv_shows_top_25_yearly.csv
# year,name,id,genres,first_air_date,last_air_date,origin_country,rating,popularity
# 1980,"Magnum, P.I.",734,"10759, 80, 18, 9648",1980-12-11,1988-05-01,US,7.3,42.925
# 1980,Heathcliff,12803,16,1980-10-04,1981-12-05,US,6.2,27.677
# 1980,Shogun,13862,"10759, 18, 10768",1980-09-15,1980-09-19,US,7.7,21.489
# 1980,Richie Rich,3026,16,1980-11-08,1983-09-24,US,6.4,14.064
# 1980,Texas,3150,10766,1980-08-04,1982-12-31,US,5.7,13.302

# join data to retrieve
# tv_shows_top_25_yearly.csv
# show_id, show_name, first_air_date, last_air_date

# tv_show_season_to_cast.csv
# season_number, cast_id, cast_name, episode_count, known_for_department,season_air_date

# tv_show_cast_details.csv
# gender as detail_gender

# tv_cast_image_race_gender.csv
# profile_path,profile_race,profile_gender

import sqlite3
import pandas as pd
import os
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Define your data folder
data_folder = './data' 

# File paths
cast_details_path = os.path.join(data_folder, 'tv_show_cast_details.csv')
image_race_gender_path = os.path.join(data_folder, 'tv_cast_image_race_gender.csv')
top_25_yearly_path = os.path.join(data_folder, f'tv_shows_top_{config.get("General", "total_shows_per_year")}_yearly.csv')
season_to_cast_path = os.path.join(data_folder, 'tv_show_season_to_cast.csv')

# Create a connection to the SQLite database
# Note: This will create the database file if it doesn't exist already
conn = sqlite3.connect('tv_data.db')

# Read the CSV files into DataFrames
df_cast_details = pd.read_csv(cast_details_path)
df_image_race_gender = pd.read_csv(image_race_gender_path)
top_25_yearly_df = pd.read_csv(top_25_yearly_path)
season_to_cast_df = pd.read_csv(season_to_cast_path)

# Write these DataFrames to the SQLite database
df_cast_details.to_sql('cast_details', conn, if_exists='replace', index=False)
df_image_race_gender.to_sql('image_race_gender', conn, if_exists='replace', index=False)
top_25_yearly_df.to_sql('top_25_yearly', conn, if_exists='replace', index=False)
season_to_cast_df.to_sql('season_to_cast', conn, if_exists='replace', index=False)

# Perform SQL queries to merge the tables
query = """
SELECT 
    t.id as show_id, 
    t.name as show_name, 
    s.season_number, 
    s.cast_id, 
    s.cast_name, 
    s.episode_count, 
    s.known_for_department, 
    s.season_air_date, 
    c.gender as detail_gender, 
    i.profile_path, 
    i.profile_race, 
    i.profile_gender
FROM top_25_yearly t
    JOIN season_to_cast s
        ON t.id = s.show_id
    JOIN cast_details c
        ON s.cast_id = c.id
    JOIN image_race_gender i
        ON s.cast_id = i.id;
"""

final_df = pd.read_sql_query(query, conn)

# Clean up the gender data
gender_map = {1: 'Female', 2: 'Male', 0: 'Undetermined'}
final_df['detail_gender'] = final_df['detail_gender'].map(gender_map)
final_df.loc[~final_df['detail_gender'].isin(['Male', 'Female']), 'detail_gender'] = final_df['profile_gender']
final_df = final_df[final_df['detail_gender'].notna()]

# Save the dataframe to a new CSV file
final_df.to_csv(os.path.join(data_folder, 'tv_export_data.csv'), index=False)

# Don't forget to close the connection
conn.close()
