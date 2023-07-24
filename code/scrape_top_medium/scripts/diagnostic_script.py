import pandas as pd

# Load all dataframes
df_image_race_gender = pd.read_csv('./data/tv_cast_image_race_gender.csv')
df_cast_details = pd.read_csv('./data/tv_show_cast_details.csv')
df_show_cast = pd.read_csv('./data/tv_show_to_cast.csv')
df_shows = pd.read_csv('./data/tv_shows_top_25_yearly.csv')



# Filter the dataframes
df_cast_details_with_pics = df_cast_details[df_cast_details['profile_path'].notna()]
df_image_race_gender_with_pics = df_image_race_gender[df_image_race_gender['profile_path'].notna()]

# Count genders
original_genders = df_cast_details_with_pics['gender'].map({1: 'Female', 2: 'Male', 0: 'Undetermined'}).value_counts()
searched_genders = df_image_race_gender_with_pics['profile_gender'].value_counts()

print("Original data:")
print(original_genders)
print("\nSearched data:")
print(searched_genders)

# Merge dataframes
df_gender_corr = pd.merge(df_cast_details_with_pics, df_image_race_gender_with_pics, on=['id', 'name', 'profile_path'], how='inner')

# Replace gender codes with names
df_gender_corr['gender'] = df_gender_corr['gender'].map({1: 'Female', 2: 'Male', 0: 'Undetermined'})

# Create a crosstab
gender_crosstab = pd.crosstab(df_gender_corr['gender'], df_gender_corr['profile_gender'])

print(gender_crosstab)

# import seaborn as sns
# import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 7))
# sns.heatmap(gender_crosstab, annot=True, fmt="d", cmap="YlGnBu")
# plt.title("Gender Correlation Heatmap")
# plt.xlabel("Searched Gender")
# plt.ylabel("Original Gender")
# plt.show()



# Join on appropriate indexes
df_merged = pd.merge(df_cast_details, df_image_race_gender, on=['id', 'name', 'profile_path'], how='inner')
df_merged = pd.merge(df_merged, df_show_cast, left_on='id', right_on='cast_id', how='inner')

# Check if the genders from two files are the same
df_merged['gender_check'] = df_merged['gender'].map({1: 'Female', 2: 'Male', 0: 'Undetermined'}) == df_merged['profile_gender']

# Print the result
print(df_merged['gender_check'].value_counts())

# Calculate the aggregated total number of appearances in episodes for each actor
df_appearances = df_show_cast.groupby('cast_id')['episode_count'].sum().reset_index()
df_appearances.columns = ['id', 'total_appearances']
df_merged = pd.merge(df_merged, df_appearances, on='id', how='left')

# Print the results
print(df_merged[['name', 'total_appearances']])

# Merge df_cast_details and df_appearances on 'id'
df_appearances_with_details = pd.merge(df_cast_details, df_appearances, on='id', how='left')

# Fill NA values in 'total_appearances' with 0
df_appearances_with_details['total_appearances'] = df_appearances_with_details['total_appearances'].fillna(0)

# Calculate the total appearances for cast members with and without profile pictures
total_appearances_with_pics = df_appearances_with_details[df_appearances_with_details['profile_path'].notna()]['total_appearances'].sum()
total_appearances_without_pics = df_appearances_with_details[df_appearances_with_details['profile_path'].isna()]['total_appearances'].sum()

print(f"Total number of episode appearances for people with profile pictures: {total_appearances_with_pics}")
print(f"Total number of episode appearances for people without profile pictures: {total_appearances_without_pics}")
