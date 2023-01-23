from audioop import avg
import pandas as pd
import csv
from datetime import datetime

# Creating a list of all empty line numbers
inFile = open("sortedStepCountDataFinal.csv", "r")
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

with open('sortedStepCountDataFinal.csv') as csvfile:
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
    totalWalkTime = 0
    totalSteps = 0
    avgSpeed = 0
    totalCaloriesBurned = 0
    totalDistanceCovered = 0
    for data in item:
        try:
            totalWalkTime += (float(data[0].strip()))
        except:
            totalWalkTime += (float(data[4].strip()))*(float(data[5].strip())*1000)
        try:
            avgSpeed += round(float(data[4].strip())*float(data[1].strip()), 2)
        except:
            avgSpeed += 0
        try:
            totalSteps += int(data[1].strip())
        except:
            totalSteps += 0
        try:
            totalDistanceCovered += round(float(data[-3].strip()),2)
        except:
            totalDistanceCovered += 0.0      
        try:
            totalCaloriesBurned += round(float(data[-2].strip()), 2)
        except:
            totalCaloriesBurned += 0.0
    totalWalkTime=int(totalWalkTime/60000)
    avgSpeed = avgSpeed/totalSteps

    dictToPrint[data[2]] = {"Duration of walking": str(totalWalkTime)+" minutes",  "Total steps": totalSteps, "Total calories burned": round(totalCaloriesBurned, 2),
                            "Average speed (m/s)": round(avgSpeed, 4), "Total Distance (m)": round(totalDistanceCovered,4)}
# print(dictToPrint)


headers = ["Date"]
for key, value in dictToPrint.items():
    for header, data in value.items():
        if header not in headers:
            headers.append(header)
# print(headers)

outFile = open("Final_Processed_Data_StepCount.csv", "w")
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "Total Distance (m)":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()
