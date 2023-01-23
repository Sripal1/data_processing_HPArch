from audioop import avg
import pandas as pd
import csv
from datetime import datetime

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
                (float(data[-3].strip()))
        except:
            avgMentalRecovery += 0.0
        try:
            avgSleepEfficiency += (float(data[4].strip())) * \
                (float(data[-3].strip()))
        except:
            avgSleepEfficiency += 0.0
        try:
            avgSleepScore += (float(data[5].strip()))*(float(data[-3].strip()))
        except:
            avgSleepScore += 0.0
        try:
            totalSleepDuration += float(data[-3].strip())
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

    dictToPrint[data[-2]] = {"Avg. mental recovery": round(avgMentalRecovery, 2), "Avg. sleep efficiency": round(avgSleepEfficiency, 2), "Avg. sleep score": round(avgSleepScore, 2)}
# print(dictToPrint)


headers = ["Date"]
for key, value in dictToPrint.items():
    for header, data in value.items():
        if header not in headers:
            headers.append(header)
# print(headers)

outFile = open("Final_Processed_Data_SleepFactor_2.csv", "w")
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
