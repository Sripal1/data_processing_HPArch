import os
import csv
import operator
import json
from types import new_class
import pandas as pd
import numpy as np
from audioop import avg
from datetime import datetime


# Enter your file name(include ".csv" at the end)
fileToRead = "com.samsung.shealth.sleep.202111281446.csv"
# do not leave spaces inbetween the words (recommend camel casing)
dataType = "sleepFactors"
outFileName = "sorted"+dataType+"Data.csv"
filesToBeRemoved = []


def sortData():
    file = open(fileToRead)
    firstLine = file.readline()  # Line with wrong headers
    headers = file.readline().split(",")  # Line with correct headers

    csv_reader = csv.reader(file, delimiter=",")
    # List of all data from and including row of index 3
    csv_list = list(csv_reader)
    file.close()
    outFile = open("sorted"+dataType+"Data.csv", "w")
    filesToBeRemoved.append("sorted"+dataType+"Data.csv")

    for i in headers:
        if i == headers[25]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    csv_list.sort(key=lambda l: l[25], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        # iterates through rows except last cell which is empty
        for j in range(len(i[:-1])):
            if counter == 25:
                tempList.append(i[j][:11])  # date
                tempList.append(i[j][11:])  # time
            else:
                tempList.append(i[j])
            counter += 1
        newList.append(tempList)

    for i in newList:  # list of all rows
        for j in range(len(i)):  # values in each row
            if j == len(i)-1:
                outFile.write(i[j])
            else:
                outFile.write(i[j]+",")
        outFile.write("\n")
    outFile.close()


sortData()

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

toBeRemoved = ["factor_01", "factor_02", "factor_03", "factor_04", "factor_05", "factor_06",
               "factor_07", "factor_08", "factor_09", "factor_10","has_sleep_data","data_version", "extra_data", "com.samsung.health.sleep.update_time", "com.samsung.health.sleep.create_time", "com.samsung.health.sleep.end_time", "com.samsung.health.sleep.datauuid"]
for item in toBeRemoved:
    try:
        usefulColumns.remove(item)
        obsoleteColumns.append(item)
    except:
        print("Couldn't remove column from file "+item)

# removing obsolete columns and writing to a new csv file
newFile2 = open("finalDeletedColumns.csv", "w")
filesToBeRemoved.append("finalDeletedColumns.csv")
for obsoleteHeader in obsoleteColumns:
    df2 = df2.drop(obsoleteHeader, 1)
df2.to_csv(newFile2)
newFile2.close()

with open("finalDeletedColumns.csv", "r") as file:
    headers = file.readline()

df = pd.read_csv("finalDeletedColumns.csv")
newFile = open("sorted"+dataType+"DataFinal.csv", "w")
filesToBeRemoved.append("sorted"+dataType+"DataFinal.csv")
# df = df.drop_duplicates(
#     subset="com.samsung.shealth.calories_burned.active_time", keep="first")
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

# Creating a list of all empty line numbers
inFile = open("sortedSleepFactorsDataFinal.csv", "r")
lineCounter = 0
headers = inFile.readline()
headers = headers.split(",")[1:]
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)
# print(emptyLineList)

with open('sortedSleepFactorsDataFinal.csv') as csvfile:
    readCSV = list(csv.reader(csvfile, delimiter=','))
counter = 1
dateGroupedList = []
for emptyLine in emptyLineList:
    tempList = []
    for i in range(counter, emptyLine-1):
        tempList.append(readCSV[i][1:])
    dateGroupedList.append(tempList)
    counter = emptyLine
# print(dateGroupedList)

dictToPrint = {}
for item in dateGroupedList:
    avgMentalRecovery = 0
    # avgPhysicalRecovery = 0
    # avgMovementAwakening = 0
    # totalSleepCycles = 0
    avgSleepEfficiency = 0
    avgSleepScore = 0
    totalSleepDuration = 0
    for data in item:
        try:
            avgMentalRecovery += (float(data[0].strip())) * \
                (float(data[-4].strip()))
        except:
            avgMentalRecovery += 0.0
        try:
            avgSleepEfficiency += (float(data[5].strip())) * \
                (float(data[-4].strip()))
        except:
            avgSleepEfficiency += 0.0
        try:
            avgSleepScore += (float(data[6].strip()))*(float(data[-4].strip()))
        except:
            avgSleepScore += 0.0
        try:
            totalSleepDuration += float(data[-4].strip())
        except:
            break
    totalSleepDurationHours = int(totalSleepDuration//60)
    totalSleepDurationMin = int(totalSleepDuration % 60)
    try:
        avgMentalRecovery = avgMentalRecovery/totalSleepDuration
        # avgPhysicalRecovery = avgPhysicalRecovery/totalSleepDuration
        # avgMovementAwakening = avgMovementAwakening/totalSleepDuration
        avgSleepEfficiency = avgSleepEfficiency/totalSleepDuration
        avgSleepScore = avgSleepScore/totalSleepDuration
    except:
        continue

    dictToPrint[data[-3]] = {"Avg. mental recovery": round(avgMentalRecovery, 2), "Avg. sleep efficiency": round(
        avgSleepEfficiency, 2), "Avg. sleep score": round(avgSleepScore, 2)}
# print(dictToPrint)


headers = ["Date"]
for key, value in dictToPrint.items():
    for header, data in value.items():
        if header not in headers:
            headers.append(header)
# print(headers)

outFile = open("Final_Processed_Data_SleepFactor.csv", "w")
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "Avg. sleep score":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()

for file in filesToBeRemoved:
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist "+file)