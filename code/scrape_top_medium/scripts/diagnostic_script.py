import pandas as pd

# Define the file path
file_path = './data/tv_show_cast_details.csv'

# Read the CSV data
data = pd.read_csv(file_path)

# Calculate the number of rows where profile_path is not null
num_with_profile = data['profile_path'].notnull().sum()

# Calculate the percentage of rows where profile_path is populated
percentage = (num_with_profile / len(data)) * 100

print(f"The profile_path is populated in {percentage:.2f}% of the rows.")
