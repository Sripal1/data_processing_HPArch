import pandas as pd
from itertools import count
import csv
from datetime import datetime

# Read in the CSV file with the correct column headers in the second row
df1 = pd.read_csv('1003_C011_processed.csv', names=["Date","Time","센서당 (mg/dL)","Blood_glucose","Blood_glucose1","mental_recovery","physical_recovery","movement_awakening","efficiency","sleep_score	count","speed","distance","calorie","max_heart_rate","min_heart_rate","avg_heart_rate"], header=1)
# df = pd.read_csv('file.csv', names=['column1', 'column2', 'column3'], header=1)
# Print the keys (column names) of the dataframe

df1['Date'] = pd.to_datetime(df1['Date'], format='%y. %m. %d')

# Format the dates in the 'date' column as strings in the desired format
df1['Date'] = df1['Date'].dt.strftime('%Y-%m-%d')

df1['Time'] = pd.to_datetime(df1['Time'], format='%H:%M:%S')

# Format the dates and times in the 'date_time' column as strings in the desired format
df1['Time'] = df1['Time'].dt.strftime('%H:%M:%S.%f')

df2 = pd.read_csv("sortedHeartRateData.csv")

df2 = df2.rename({"start_date":"Date"},axis = 1)
df_merged = pd.merge(df1,df2,on = "Date",how="outer")
df_merged['time_difference'] = df_merged[''] - df_merged['time_column_2']

# print(df2)

df_merged.to_csv("processedData2.csv")