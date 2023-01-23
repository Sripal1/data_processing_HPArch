import csv
import operator
from types import new_class
import pandas as pd
import csv
import numpy as np
from datetime import datetime


# Enter your file name(include ".csv" at the end)
fileToRead = "com.samsung.health.sleep_stage.202112121421.csv"
dataType = "Sleep"
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
        if i == headers[0]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    csv_list.sort(key=lambda l: l[0], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        for j in i[:-1]:  # iterates through rows except last cell which is empty
            if counter == 0:
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

for header in usefulColumns:
    # checking if all cells in a column are longer than 25 characters
    if len(str(df2[header][0])) > 25:
        obsoleteColumns.append(header.strip())
        usefulColumns.remove(header.strip())

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

inFile = open("sortedSleepDataFinal.csv", "r")
filesToBeRemoved.append("sortedSleepDataFinal.csv")
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
    nightSleep = {}
    timeDifferenceDay = 0
    totalNightSleep = None
    totalDaySleep = None
    for i in range(len(dateTimeSet)-1):
        if dateTimeSet[i] == dateTimeSet[0]:
            initialTime = datetime.strptime(
                dateTimeSet[i], "%Y-%m-%d %H:%M:%S.%f")
            finalTime = datetime.strptime(
                dateTimeSet[i+1], "%Y-%m-%d %H:%M:%S.%f")
            if (initialTime.hour >= 9 and initialTime.hour < 21) and (finalTime.hour >= 9 and finalTime.hour < 21):
                timeDifferenceDay = finalTime - initialTime
                nightSleep[dateTimeSet[0][:11].strip()]=[]
                totalDaySleep = timeDifferenceDay
                timeDateDict[dateTimeSet[0][:11].strip()] = {"Total sleep time": str(timeDifferenceDay), "Nap duration": totalDaySleep,"Starting sleep time(night)":None, "Ending sleep time(night)":None,
                                                             "Number of times woken up during sleep": 0, "Sleep during night": "No", "Total night sleep": totalNightSleep}
            else:
                timeDifferenceNight = finalTime - initialTime
                nightSleep[dateTimeSet[0][:11].strip()] = [(dateTimeSet[i],dateTimeSet[i+1])]
                totalNightSleep = timeDifferenceNight
                timeDateDict[dateTimeSet[0][:11].strip()] = {"Total sleep time": str(timeDifferenceNight), "Nap duration": 0,"Starting sleep time(night)":None, "Ending sleep time(night)":None,
                                                             "Number of times woken up during sleep": 0, "Sleep during night": "Yes", "Total night sleep": totalNightSleep}
        else:
            initialTime = datetime.strptime(
                dateTimeSet[i], "%Y-%m-%d %H:%M:%S.%f")
            finalTime = datetime.strptime(
                dateTimeSet[i+1], "%Y-%m-%d %H:%M:%S.%f")

            if (initialTime.hour >= 9 and initialTime.hour < 21) and (finalTime.hour >= 9 and finalTime.hour < 21):
                timeDifferenceDay = finalTime - initialTime
                if timeDifferenceDay.total_seconds()/60 > 10:
                    timeDateDict[dateTimeSet[0][:11].strip(
                    )]["Number of times woken up during sleep"] += 1
                if timeDifferenceDay.total_seconds()/60 > 30:
                    pass
                else:
                    try:
                        totalDaySleep+=timeDifferenceDay
                    except:
                        totalDaySleep=timeDifferenceDay
                
            else:
                timeDifferenceNight = finalTime - initialTime
                nightSleep[dateTimeSet[0][:11].strip()].append((dateTimeSet[i],dateTimeSet[i+1]))
                if timeDifferenceNight.total_seconds()/60>10:
                    timeDateDict[dateTimeSet[0][:11].strip(
                        )]["Number of times woken up during sleep"] += 1
                if timeDifferenceNight.total_seconds()/60 > 30:
                    pass
                else:
                    timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Sleep during night"] = "Yes"
                    try:
                        totalNightSleep+=timeDifferenceNight
                    except:
                        totalNightSleep=timeDifferenceNight
        try:
            nightSleepHrs=int(totalNightSleep.total_seconds()//3600)
            nightSleepMin=int((totalNightSleep.total_seconds()%3600)//60)
        except:
            nightSleepHrs=0
            nightSleepMin=0
        
        try:
            daySleepHrs=int(totalDaySleep.total_seconds()//3600)
            daySleepMin=int((totalDaySleep.total_seconds()%3600)//60)
        except:
            daySleepHrs=0
            daySleepMin=0
        
        timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Total night sleep"]=str(nightSleepHrs)+" hours "+ str(nightSleepMin)+" min"
        timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Nap duration"]=str(daySleepHrs)+" hours "+ str(daySleepMin)+" min"

        if totalDaySleep==None:
            totalSleepTime=totalNightSleep
        elif totalNightSleep==None:
            totalSleepTime=totalDaySleep
        else:
            totalSleepTime=totalNightSleep+totalDaySleep
        
        try:
            totalSleepHrs=int(totalSleepTime.total_seconds()//3600)
            totalSleepMin=int((totalSleepTime.total_seconds()%3600)//60)
        except:
            totalSleepHrs=0
            totalSleepMin=0
        timeDateDict[dateTimeSet[0]
                             [:11].strip()]["Total sleep time"]=str(totalSleepHrs)+" hours "+ str(totalSleepMin)+" min"
    for value in nightSleep.values():
        initialList=[]
        finalList=[]
        for initialTime,finalTime in value:
            initialList.append(initialTime)
            finalList.append(finalTime)
        try:
            initialTime = datetime.strptime(initialList[0], "%Y-%m-%d %H:%M:%S.%f")
            finalTime = datetime.strptime(finalList[-1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            initialTimeToPrint=("No time")
            finalTimeToPrint=("No time")
            continue
        if initialTime.hour<9 or initialTime.hour>=21:
            try:
                initialTimeToPrint=(initialList[0])
            except:
                initialTimeToPrint=("No time")
        else:
            try:
                initialTimeToPrint=(initialList[1])
            except:
                initialTimeToPrint=(initialList[0])
        
        if finalTime.hour<9 or finalTime.hour>=21:
            try:
                finalTimeToPrint=(finalList[-1])
            except:
                finalTimeToPrint=("No time")
        else:
            try:
                finalTimeToPrint=(initialList[-2])
            except:
                finalTimeToPrint=(initialList[-1])

    timeDateDict[dateTimeSet[0][:11].strip()]["Starting sleep time(night)"]=initialTimeToPrint[11:-4]
    timeDateDict[dateTimeSet[0][:11].strip()]["Ending sleep time(night)"]=finalTimeToPrint[11:-4]

# print(timeDateDict)


outFile = open("Final_Processed_Data_Sleep.csv", "w")
headers = ["Date","Total sleep time", "Nap duration", "Starting sleep time(night)", "Ending sleep time(night)","Number of times woken up during sleep","Sleep during night","Total night sleep"]
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")

for date, values in timeDateDict.items():
    outFile.write(date+" "+",")
    for title, value in values.items():
        if title == "Total night sleep":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")

import os
for file in filesToBeRemoved:
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist "+file)