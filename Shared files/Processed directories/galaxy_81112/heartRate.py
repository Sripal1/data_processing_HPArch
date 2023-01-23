import csv
import operator
import json
from types import new_class
import pandas as pd
import numpy as np
from itertools import count
from datetime import datetime

# Reads data from input file and writes it to a new csv file with correct headers

# Enter your file name(include ".csv" at the end)
fileToRead = "com.samsung.shealth.tracker.heart_rate.202112181112.csv"
dataType = "HeartRate"
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
        if i == headers[3]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    csv_list.sort(key=lambda l: l[3], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        for j in i[:-1]:  # iterates through rows except last cell which is empty
            if counter == 3:
                tempList.append(j[:11])  # date
                tempList.append(j[11:])  # time
            else:
                tempList.append(j)
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

file=open(fileToRead)
uniqueIDdata=file.readline()

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
    toBeRemovedHeartRate = ['tag_id', 'com.samsung.health.heart_rate.binning_data', 'com.samsung.health.heart_rate.update_time','com.samsung.health.heart_rate.create_time']
    # checking if all cells in a column are longer than 25 characters
    if len(str(df2[header][0])) > 25:
        obsoleteColumns.append(header.strip())
        usefulColumns.remove(header.strip())
    for item in toBeRemovedHeartRate:
        if header.strip() == item:
            obsoleteColumns.append(header.strip())
            usefulColumns.remove(header.strip())
# obsoleteColumns.append("com.samsung.health.heart_rate.update_time")
# usefulColumns.remove("com.samsung.health.heart_rate.update_time")

# removing obsolete columns and writing to a new csv file
newFile2 = open("finalDeletedColumns.csv", "w")
filesToBeRemoved.append("finalDeletedColumns.csv")
for obsoleteHeader in obsoleteColumns:
    df2 = df2.drop(obsoleteHeader, 1)
df2.to_csv(newFile2)


with open("finalDeletedColumns.csv", "r") as file:
    headers = file.readline()

df = pd.read_csv("finalDeletedColumns.csv")
newFile = open("sorted"+dataType+"DataFinal.csv", "w")
# df=df.drop_duplicates(subset="speed",keep="last")
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
inFile = open("sortedHeartRateDataFinal.csv", "r")
filesToBeRemoved.append("sortedHeartRateDataFinal.csv")
lineCounter = 0
headers = inFile.readline()
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)
# print(emptyLineList)

with open('sortedHeartRateDataFinal.csv') as csvfile:
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


dayList = []
nightList = []
for item in dateGroupedList:
    tempDayList = []
    tempNightList = []
    for data in item:
        startTime = datetime.strptime(data[1], "%H:%M:%S.%f")
        dayBeginning = datetime.strptime("09:00", "%H:%M")
        dayEnding = datetime.strptime("21:00", "%H:%M")
        if startTime > dayBeginning and startTime < dayEnding:
            tempDayList.append(data)
        else:
            tempNightList.append(data)
    dayList.append(tempDayList)
    nightList.append(tempNightList)
while [] in dayList:dayList.remove([])
while [] in nightList:nightList.remove([])
# print(dayList)
# print(nightList)

dayDict = {}
for item in dayList:
    minDayHR = None
    maxDayHR = None
    totalDayHR = 0.0
    counter = 0
    for dateData in item:
        # print(dateData)
        if minDayHR == None:
            minDayHR = float(dateData[4].strip())
        elif float(dateData[4].strip()) < minDayHR:
            minDayHR = float(dateData[4].strip())

        if maxDayHR == None:
            maxDayHR = float(dateData[3].strip())
        elif float(dateData[3].strip()) > maxDayHR:
            maxDayHR = float(dateData[3].strip())

        totalDayHR += float(dateData[-1].strip())
        counter += 1
    # print(str(totalDayHR)+"/"+str(counter))
    avgDayHR=totalDayHR/counter
    dayDict[dateData[0].strip()]={"Avg. day HR":round(avgDayHR,2),"Max. HR (day)": maxDayHR,"Min. HR (day)":minDayHR,"Number of samples (day)":counter}
# print(dayDict)

nightDict={}
for item in nightList:
    minNightHR = None
    maxNightHR = None
    totalNightHR = 0.0
    counter = 0
    for dateData in item:
        # print(dateData)
        if minNightHR == None:
            minNightHR = float(dateData[4].strip())
        elif float(dateData[4].strip()) < minNightHR:
            minNightHR = float(dateData[4].strip())

        if maxNightHR == None:
            maxNightHR = float(dateData[3].strip())
        elif float(dateData[3].strip()) > maxNightHR:
            maxNightHR = float(dateData[3].strip())

        totalNightHR += float(dateData[-1].strip())
        counter += 1
    avgNightHR=totalNightHR/counter
    nightDict[dateData[0].strip()]={"Avg. night HR":round(avgNightHR,2),"Max. HR (night)": maxNightHR,"Min. HR (night)":minNightHR,"Number of samples (night)":counter}
# print(nightDict)

dailyDict = {}
for item in dateGroupedList:
    dailyMinHR = None
    dailyMaxHR = None
    avgHR = 0
    counter=0
    for data in item:
        if dailyMinHR == None:
            dailyMinHR = float(data[4].strip())
        elif float(data[4].strip()) < dailyMinHR:
            dailyMinHR = float(data[4].strip())

        if dailyMaxHR == None:
            dailyMaxHR = float(data[3].strip())
        elif float(data[3].strip()) > dailyMaxHR :
            dailyMaxHR  = float(data[3].strip())
        avgHR += float(data[-1].strip())
        counter+=1
    avgHR=avgHR/counter
    dailyDict[data[0]] = {"Min. HR (daily)": round(dailyMinHR,2), "Max. HR (daily)": round(dailyMaxHR, 2),
                            "Avg. HR (daily)": round(avgHR, 2),"Number of samples (daily)":counter}
# print(dailyDict)

outFile = open("Final_Processed_Data_HeartRate.csv", "w")
headers = ["Date"]

def writeHeaders(dictName):
    for item in dictName.values():
        for header in item.keys():
            if header not in headers:
                headers.append(header)
writeHeaders(dailyDict)
writeHeaders(dayDict)
writeHeaders(nightDict)
# print(headers)
# print(dailyDict)
# print(dayDict)
# print(nightDict)

for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dailyDict.items():
    outFile.write(date+",")
    for title, value in values.items():
        outFile.write(str(value)+",")

    if date.strip() in dayDict.keys():
        tempValue=dayDict[date.strip()]
        for title,value in tempValue.items():
            outFile.write(str(value)+",")
    else:
        for i in range(4):
            outFile.write(" "+",")

    if date.strip() in nightDict.keys():
        for title,value in nightDict[date.strip()].items():
            if title == "Number of samples (night)":
                outFile.write(str(value)+"\n")
            else:
                outFile.write(str(value)+",")
    else:
        for i in range(3):
            outFile.write(" "+",")
        outFile.write(" "+"\n")
outFile.close()

import os
for file in filesToBeRemoved:
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist "+file)