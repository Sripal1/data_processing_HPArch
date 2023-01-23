import pandas as pd

# Set the time difference (in minutes)
time_difference = 5

# Read the first CSV file into a dataframe
df1 = pd.read_csv('1003_C011_processed.csv', names=["Date","Time","센서당 (mg/dL)","Blood_glucose","Blood_glucose1","mental_recovery","physical_recovery","movement_awakening","efficiency","sleep_score	count","speed","distance","calorie","max_heart_rate","min_heart_rate","avg_heart_rate"], header=1)

# Read the second CSV file into a dataframe
df2 = pd.read_csv('sortedHeartRateData.csv')

df1['Date'] = pd.to_datetime(df1['Date'], format='%y. %m. %d')

# Format the dates in the 'date' column as strings in the desired format
df1['Date'] = df1['Date'].dt.strftime('%Y-%m-%d')

df1['Time'] = pd.to_datetime(df1['Time'], format='%H:%M:%S')

# Format the dates and times in the 'date_time' column as strings in the desired format
df1['Time'] = df1['Time'].dt.strftime('%H:%M:%S.%f')

# Get the time column names for both dataframes
time_col_name1 = df1.columns[1]
time_col_name2 = df2.columns[1]
print(time_col_name1)
print(time_col_name2)

num_rows = df2.shape[0]
df2 = df2.drop(df2.index[num_rows-1])
# Convert the time columns to datetime objects
df1[time_col_name1] = pd.to_datetime(df1[time_col_name1])
df2[time_col_name2] = pd.to_datetime(df2[time_col_name2])

# Create an empty dataframe to store the merged rows
merged_df = pd.DataFrame()

# Iterate through the rows of the first dataframe
for i, row1 in df1.iterrows():
  # Get the time value for this row
  time1 = row1[time_col_name1]

  # Get the rows from the second dataframe that are within the specified time range
  mask = (df2[time_col_name2] >= time1) & (df2[time_col_name2] <= time1 + pd.Timedelta(minutes=time_difference))
  rows2 = df2[mask]

  # If any rows were found
  if rows2.shape[0] > 0:
    # Merge the rows and add them to the merged dataframe
    merged_rows = pd.concat([row1.to_frame().T, rows2])
    merged_df = pd.concat([merged_df, merged_rows])

# Write the merged dataframe to a new CSV file
merged_df.to_csv('merged.csv', index=False)

print('Done!')
