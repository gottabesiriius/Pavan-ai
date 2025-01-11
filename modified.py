import pandas as pd

# Load the dataset
satellite_data = pd.read_csv("satellite_data2.csv")

# Ensure the 'Date' column is in datetime format (DD-MM-YYYY)
satellite_data['Date'] = pd.to_datetime(satellite_data['Date'], format='%d-%m-%Y')

# Modify the 'Date' column to include '00:00' as the time
satellite_data['Date'] = satellite_data['Date'].dt.strftime('%d-%m-%Y 00:00')

# Save the modified dataframe to a new CSV file
satellite_data.to_csv("modified_satellite_data2.csv", index=False)

# Optionally, display the first few rows of the modified data
print(satellite_data.head())