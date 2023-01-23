import pandas as pd
import csv
from datetime import datetime

inFile = open("sortedSleepDataFinal.csv", "r")
lineCounter = 0
headers = inFile.readline()
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)

with open('sortedSleepDataFinal.csv') as csvfile:
    readCSV = list(csv.reader(csvfile, delimiter=','))
dateList = []
counter = 0
for emptyLine in emptyLineList:
    if emptyLine == emptyLineList[0]:
        tempTuple = (readCSV[1][3], readCSV[emptyLine-2][3])
        dateList.append(tempTuple)
        counter += 1
    else:
        tempTuple = (readCSV[emptyLineList[counter-1]]
                     [3], readCSV[emptyLine-2][3])
        dateList.append(tempTuple)
        counter += 1
csvfile.close()

inFile2 = open("sortedSleepDataFinal.csv", "r")
allTimeList = [[]]
headers = inFile2.readline()
counter = 0

for line in inFile2:
    if line.split(",") != ["\n"]:
        allTimeList[counter].append(line.split(",")[3])
    else:
        allTimeList.append([])
        counter += 1
allTimeList.remove([])
# print(allTimeList)

timeDateDict = {}
for dateTimeSet in allTimeList:
    awakeTime = []
    timeDifferenceDay = 0
    for i in range(len(dateTimeSet)):
        if dateTimeSet[i] == dateTimeSet[0]:
            initialTime = datetime.strptime(
                dateTimeSet[i], "%Y-%m-%d %H:%M:%S.%f")
            finalTime = datetime.strptime(
                dateTimeSet[-1], "%Y-%m-%d %H:%M:%S.%f")
            timeDifferenceDay = finalTime - initialTime
            timeDateDict[dateTimeSet[0][:11].strip()] = {"Average sleep time": str(timeDifferenceDay),
                                                         "Number of times woken up during sleep": 0, "Sleep during day": "No", "Sleep during night": "No"}
        else:
            utcTime1 = datetime.strptime(
                dateTimeSet[i-1], "%Y-%m-%d %H:%M:%S.%f")
            utcTime2 = datetime.strptime(
                dateTimeSet[i], "%Y-%m-%d %H:%M:%S.%f")
            timeDifference = utcTime2-utcTime1
            if utcTime1.hour <= 10 or utcTime1.hour >= 17:
                timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Sleep during night"] = "Yes"
            else:
                timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Sleep during day"] = "Yes"
            # print(timeDifference)
            if timeDifference.total_seconds()/3600 > 1:
                timeDateDict[dateTimeSet[0][:11].strip(
                )]["Number of times woken up during sleep"] += 1
                awakeTime.append(timeDifference)
    totalTimeAwake = 0
    for awakeTimeItem in awakeTime:
        if awakeTimeItem == awakeTime[0]:
            totalTimeAwake = awakeTimeItem
        else:
            totalTimeAwake += awakeTimeItem
    if (type(totalTimeAwake) != int):
        if totalTimeAwake >= timeDifferenceDay:
            timeDateDict[dateTimeSet[0][:11].strip()]["Average sleep time"] = str(
                totalTimeAwake-timeDifferenceDay)
        else:
            timeDateDict[dateTimeSet[0][:11].strip()]["Average sleep time"] = str(
                timeDifferenceDay-totalTimeAwake)

outFile = open("Final_Processed_Data_Sleep.csv", "w")
headers = ["Date", "Average Sleep Time", "Number of times woken up during sleep",
           "Sleep during day", "Sleep during night"]
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")

for date, values in timeDateDict.items():
    outFile.write(date+" "+",")
    for title, value in values.items():
        if title == "Sleep during night":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
