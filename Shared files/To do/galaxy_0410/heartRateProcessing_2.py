from itertools import count
import pandas as pd
import csv
from datetime import datetime

# Creating a list of all empty line numbers
inFile = open("sortedHeartRateDataFinal.csv", "r")
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
            minDayHR = float(dateData[3].strip())
        elif float(dateData[3].strip()) < minDayHR:
            minDayHR = float(dateData[3].strip())

        if maxDayHR == None:
            maxDayHR = float(dateData[2].strip())
        elif float(dateData[2].strip()) > maxDayHR:
            maxDayHR = float(dateData[2].strip())

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
            minNightHR = float(dateData[3].strip())
        elif float(dateData[3].strip()) < minNightHR:
            minNightHR = float(dateData[3].strip())

        if maxNightHR == None:
            maxNightHR = float(dateData[2].strip())
        elif float(dateData[2].strip()) > maxNightHR:
            maxNightHR = float(dateData[2].strip())

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
            dailyMinHR = float(data[3].strip())
        elif float(data[3].strip()) < dailyMinHR:
            dailyMinHR = float(data[3].strip())

        if dailyMaxHR == None:
            dailyMaxHR = float(data[2].strip())
        elif float(data[2].strip()) > dailyMaxHR :
            dailyMaxHR  = float(data[2].strip())
        avgHR += float(data[-1].strip())
        counter+=1
    avgHR=avgHR/counter
    dailyDict[data[0]] = {"Min. HR (daily)": round(dailyMinHR,2), "Max. HR (daily)": round(dailyMaxHR, 2),
                            "Avg. HR (daily)": round(avgHR, 2),"Number of samples (daily)":counter}
# print(dailyDict)

outFile = open("Final_Processed_Data_HeartRate_2.csv", "w")
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