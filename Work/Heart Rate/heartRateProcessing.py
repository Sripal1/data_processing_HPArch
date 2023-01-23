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

dictToPrint = {}
for item in dateGroupedList:
    avgMinHR = 0
    avgMaxHR = 0
    avgHR = 0
    counter=0
    for data in item:
        avgMinHR += float(data[3].strip())
        avgMaxHR += (float(data[2].strip()))
        avgHR += float(data[-1].strip())
        counter+=1
    avgHR=avgHR/counter
    avgMaxHR=avgMaxHR/counter
    avgMinHR=avgMinHR/counter
    dictToPrint[data[0]] = {"avg. min HR": round(avgMinHR,2), "avg. max HR": round(avgMaxHR, 2),
                            "avg. HR": round(avgHR, 4)}
print(dictToPrint)

outFile = open("Final_Processed_Data_HeartRate.csv", "w")
headers = ["Date","Avg. min Heart Rate (bpm)", "Avg. max Heart Rate (bpm)", "Avg. Heart Rate (bpm)"]

print(headers)
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "avg. HR":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()
