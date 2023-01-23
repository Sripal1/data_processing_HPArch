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

for header in usefulColumns:
    toBeRemovedHeartRate = ["pkg_name","heart_beat_count","time_offset","binning_data","comment","deviceuuid","custom","end_time","datauuid","create_time","update_time"]
    # checking if all cells in a column are longer than 25 characters
    # if len(str(df2[header][0])) > 25:
    #     obsoleteColumns.append(header.strip())
    #     usefulColumns.remove(header.strip())
    for item in toBeRemovedHeartRate:
        if header.strip() == item:
            obsoleteColumns.append(header.strip())
            usefulColumns.remove(header.strip())
obsoleteColumns.append("datauuid")
usefulColumns.remove("datauuid")
obsoleteColumns.append("update_time")
usefulColumns.remove("update_time")

# removing obsolete columns and writing to a new csv file
newFile2 = open("finalDeletedColumns.csv", "w")
for obsoleteHeader in obsoleteColumns:
    df2 = df2.drop(obsoleteHeader, 1)
df2.to_csv(newFile2)

with open("finalDeletedColumns.csv", "r") as file:
    headers = file.readline()
print(usefulColumns)
file.close()

newFile2 = open("finalDeletedColumns.csv", "w")
newFile2.write(usefulColumns+"\n")
groupedDate = df2.groupby("start_date")  # groups data by date
numDays = 0
dateList = []
# newFile2.write(headers)
for date, date_df in groupedDate:
    date_df.to_csv(newFile2, mode='a', header=False, index=False)
    newFile2.write("\n")    # adds a blank line between 2 grouped data sets
    numDays += 1            # number of days of data- same as len(dateList)
    dateList.append(date)   # list of all dates in the file
newFile2.close()

# df = pd.read_csv("finalDeletedColumns.csv")
# newFile = open("sorted"+dataType+"DataFinal.csv", "w")
# # df=df.drop_duplicates(subset="speed",keep="last")
# groupedDate = df.groupby("start_date")  # groups data by date
# numDays = 0
# dateList = []
# newFile.write(headers)
# for date, date_df in groupedDate:
#     date_df.to_csv(newFile, mode='a', header=False, index=False)
#     newFile.write("\n")  # adds a blank line between 2 grouped data sets
#     numDays += 1            # number of days of data- same as len(dateList)
#     dateList.append(date)   # list of all dates in the file
# newFile.close()