import csv
import operator
import json
from types import new_class
import pandas as pd
import numpy as np
from datetime import datetime

# Enter your file name(include ".csv" at the end)
fileToRead = "com.samsung.shealth.step_daily_trend.202112121456.csv"
dataType = "Steps"  #do not leave spaces inbetween the words (recommend camel casing)
outFileName = "sorted"+dataType+"Data.csv"
filesToBeRemoved=[]

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
        if i == headers[2]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    csv_list.sort(key=lambda l: l[2], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        for j in i[:-1]:  # iterates through rows except last cell which is empty
            if counter == 2:
                tempList.append(j[:11])  # date
                tempList.append(j[11:])  # time
            else:
                tempList.append(j)
            counter += 1
        newList.append(tempList)

    for i in newList:  # list of all rows
        for j in i:  # values in each row
            if j == i[-1]:
                outFile.write(j)
            else:
                outFile.write(j+",")
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

for item in ["deviceuuid","datauuid","day_time","binning_data"]:
    try:
        obsoleteColumns.append(item)
        usefulColumns.remove(item)
    except:
        print("Coudn't remove "+item)

# removing obsolete columns and writing to a new csv file
newFile2 = open("finalDeletedColumns.csv", "w")
for obsoleteHeader in obsoleteColumns:
    df2 = df2.drop(obsoleteHeader, 1)
df2.to_csv(newFile2)
newFile2.close()

with open("finalDeletedColumns.csv", "r") as file:
    headers = file.readline()
filesToBeRemoved.append("finalDeletedColumns.csv")

df = pd.read_csv("finalDeletedColumns.csv")
newFile = open("sorted"+dataType+"DataFinal.csv", "w")
df=df.drop_duplicates(subset="count",keep="last")
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
inFile = open("sortedStepsDataFinal.csv", "r")
filesToBeRemoved.append("sortedStepsDataFinal.csv")
lineCounter = 0
headers = inFile.readline()
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)
# print(emptyLineList)

with open('sortedStepsDataFinal.csv') as csvfile:
    readCSV = list(csv.reader(csvfile, delimiter=','))
counter = 1
dateGroupedList = []
for emptyLine in emptyLineList:
    if emptyLine == emptyLineList[-1] or emptyLine == emptyLineList[0]:
        tempList = []
        for i in range(counter, emptyLine-1):
            tempList.append(readCSV[i][1:])
        counter = emptyLine
    else:
        tempList = []
        for i in range(counter, emptyLine-1):
            tempList.append(readCSV[i][1:])
    dateGroupedList.append(tempList)
    counter = emptyLine
# print(dateGroupedList)

nonDuplicateList = []

for item in dateGroupedList:
    tempList = []
    for i in range(len(item)):
        if len(item) >= 2:
            if i != 0:
                utcTime1 = datetime.strptime(item[i-1][2], "%H:%M:%S.%f")
                utcTime2 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
                timeDifference = utcTime2-utcTime1
                if timeDifference.total_seconds() < 960:
                    if int(item[i][4]) > int(item[i-1][4]):
                        tempList.append(item[i])
                    else:
                        tempList.append(item[i-1])
                else:
                    tempList.append(item[i])
            elif i == 0:
                utcTime1 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
                utcTime2 = datetime.strptime(item[i+1][2], "%H:%M:%S.%f")
                timeDifference = utcTime2-utcTime1
                if timeDifference.total_seconds() < 960:
                    if int(item[i][4]) > int(item[i+1][4]):
                        tempList.append(item[i])
                    else:
                        tempList.append(item[i+1])
                else:
                    tempList.append(item[i])
        else:
            tempList.append(item[i])
    nonDuplicateList.append(tempList)

newList = []
for item in nonDuplicateList:
    tempList = []
    for data in item:
        if data not in tempList:
            tempList.append(data)
    newList.append(tempList)
finalList = []

for item in newList:
    tempList = []
    for i in range(len(item)):
        if len(item) >= 2:
            if i != 0:
                utcTime1 = datetime.strptime(item[i-1][2], "%H:%M:%S.%f")
                utcTime2 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
                timeDifference = utcTime2-utcTime1
                if timeDifference.total_seconds() < 960:
                    if int(item[i][4]) > int(item[i-1][4]):
                        tempList.append(item[i])
                    else:
                        tempList.append(item[i-1])
                else:
                    tempList.append(item[i])
            elif i == 0:
                utcTime1 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
                utcTime2 = datetime.strptime(item[i+1][2], "%H:%M:%S.%f")
                timeDifference = utcTime2-utcTime1
                if timeDifference.total_seconds() < 960:
                    if int(item[i][4]) > int(item[i+1][4]):
                        tempList.append(item[i])
                    else:
                        tempList.append(item[i+1])
                else:
                    tempList.append(item[i])
        else:
            tempList.append(item[i])
    finalList.append(tempList)

newList = []
for item in finalList:
    tempList = []
    for data in item:
        if data not in tempList:
            tempList.append(data)
    newList.append(tempList)
finalList = newList[:]
# print(finalList)

dictToPrint = {}
for item in finalList:
    totalSteps = 0
    avgSpeed = 0
    totalDistance = 0
    totalCalories = 0
    frequency = 0
    for data in item:
        totalSteps += int(data[4].strip())
        # totalCalories += float(data[-1].strip())
        totalDistance += float(data[-2].strip())
        avgSpeed += float(data[5].strip())*float(data[-2].strip())
        frequency += 1
    avgSpeed = avgSpeed/totalDistance
    if totalSteps>=10000:
        greaterThan10K="Yes"
    else:
        greaterThan10K="No"
    dictToPrint[data[1]] = {"Step Count": totalSteps,
                            "Speed (m/s)": round(avgSpeed,2), "Distance": round(totalDistance,2), "Greater than 10K steps": greaterThan10K}
# print(dictToPrint)

outFile = open("Final_Processed_Data_Steps.csv", "w")
headers = ["Date", "Step Count", "Speed (m/s)", "Distance", "Greater than 10K steps"]

for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "Greater than 10K steps":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()

import os
for file in filesToBeRemoved:
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist "+file)
