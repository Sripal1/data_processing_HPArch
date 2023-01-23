from types import new_class
import pandas as pd
import csv
import numpy as np
from sortingData import *

with open(outFileName, "r") as file:
    headers = file.readline()  # reading headers
    headers = headers.split(",")

obsoleteColumns = []
usefulColumns = []
df2 = pd.read_csv(outFileName)
for header in headers:
    # checking if all cells in a column are same
    if (df2[header.strip()] == df2[header.strip()][0]).all():
        obsoleteColumns.append(header.strip())
    elif(df2[header.strip()].isnull().all()):  # checking if all cells in a column are empty
        obsoleteColumns.append(header.strip())
    else:
        usefulColumns.append(header.strip())

toBeRemoved = ["extra_data", "com.samsung.shealth.calories_burned.create_time",
               "com.samsung.shealth.calories_burned.datauuid", "com.samsung.shealth.calories_burned.day_time"]
for item in toBeRemoved:
    try:
        obsoleteColumns.append(item)
        usefulColumns.remove(item)
    except:
        print("Couldn't remove column from file")

# removing obsolete columns and writing to a new csv file
newFile2 = open("finalDeletedColumns.csv", "w")
for obsoleteHeader in obsoleteColumns:
    df2 = df2.drop(obsoleteHeader, 1)
df2.to_csv(newFile2)
newFile2.close()

with open("finalDeletedColumns.csv", "r") as file:
    headers = file.readline()

df = pd.read_csv("finalDeletedColumns.csv")
newFile = open("sorted"+dataType+"DataFinal.csv", "w")
df = df.drop_duplicates(
    subset="com.samsung.shealth.calories_burned.active_time", keep="first")
groupedDate = df.groupby("start_date")  # groups data by date
numDays = 0
dateList = []
newFile.write(headers)
for date, date_df in groupedDate:
    date_df.to_csv(newFile, mode='a', header=False, index=False)
    newFile.write("\n")  # adds a blank line between 2 grouped data sets
    numDays += 1            # number of days of data- same as len(dateList)
    dateList.append(date)   # list of all dates in the file
newFile.close()
