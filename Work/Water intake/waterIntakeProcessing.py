from audioop import avg
import pandas as pd
import csv
from datetime import datetime

# Creating a list of all empty line numbers
inFile = open("sortedWaterIntakeDataFinal.csv", "r")
lineCounter = 0
headers = inFile.readline()
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)
# print(emptyLineList)

with open('sortedWaterIntakeDataFinal.csv') as csvfile:
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

# nonDuplicateList = []

# for item in dateGroupedList:
#     tempList = []
#     for i in range(len(item)):
#         if len(item) >= 2:
#             if i != 0:
#                 utcTime1 = datetime.strptime(item[i-1][2], "%H:%M:%S.%f")
#                 utcTime2 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
#                 timeDifference = utcTime2-utcTime1
#                 if timeDifference.total_seconds() < 960:
#                     if int(item[i][4]) > int(item[i-1][4]):
#                         tempList.append(item[i])
#                     else:
#                         tempList.append(item[i-1])
#                 else:
#                     tempList.append(item[i])
#             elif i == 0:
#                 utcTime1 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
#                 utcTime2 = datetime.strptime(item[i+1][2], "%H:%M:%S.%f")
#                 timeDifference = utcTime2-utcTime1
#                 if timeDifference.total_seconds() < 960:
#                     if int(item[i][4]) > int(item[i+1][4]):
#                         tempList.append(item[i])
#                     else:
#                         tempList.append(item[i+1])
#                 else:
#                     tempList.append(item[i])
#         else:
#             tempList.append(item[i])
#     nonDuplicateList.append(tempList)

# newList = []
# for item in nonDuplicateList:
#     tempList = []
#     for data in item:
#         if data not in tempList:
#             tempList.append(data)
#     newList.append(tempList)

# finalList = []

# for item in newList:
#     tempList = []
#     for i in range(len(item)):
#         if len(item) >= 2:
#             if i != 0:
#                 utcTime1 = datetime.strptime(item[i-1][2], "%H:%M:%S.%f")
#                 utcTime2 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
#                 timeDifference = utcTime2-utcTime1
#                 if timeDifference.total_seconds() < 960:
#                     if int(item[i][4]) > int(item[i-1][4]):
#                         tempList.append(item[i])
#                     else:
#                         tempList.append(item[i-1])
#                 else:
#                     tempList.append(item[i])
#             elif i == 0:
#                 utcTime1 = datetime.strptime(item[i][2], "%H:%M:%S.%f")
#                 utcTime2 = datetime.strptime(item[i+1][2], "%H:%M:%S.%f")
#                 timeDifference = utcTime2-utcTime1
#                 if timeDifference.total_seconds() < 960:
#                     if int(item[i][4]) > int(item[i+1][4]):
#                         tempList.append(item[i])
#                     else:
#                         tempList.append(item[i+1])
#                 else:
#                     tempList.append(item[i])
#         else:
#             tempList.append(item[i])
#     finalList.append(tempList)

# newList = []
# for item in finalList:
#     tempList = []
#     for data in item:
#         if data not in tempList:
#             tempList.append(data)
#     newList.append(tempList)
# finalList = newList
# # print(finalList)

dictToPrint = {}
for item in dateGroupedList:
    totalWaterIntake = 0
    waterQuantityPerIntake = {}
    frequency = 0
    for data in item:
        totalWaterIntake += float(data[2].strip())
        if (float(data[2].strip())) in waterQuantityPerIntake:
            waterQuantityPerIntake[float(data[2].strip())] += 1
        else:
            waterQuantityPerIntake[float(data[2].strip())] = 1
        frequency += 1
    waterQuantityPerIntake = totalWaterIntake/frequency
    dictToPrint[data[0]] = {"Total Water Intake (ml)": totalWaterIntake, "Average water Quantity per Intake (ml)": waterQuantityPerIntake,
                            "Frequency of water intake": frequency}
# print(dictToPrint)

outFile = open("Final_Processed_Data_WaterIntake.csv", "w")
headers = [
    "Date", "Total Water Intake (ml)", "Average water Quantity per Intake (ml)", "Frequency of water intake"]

for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "Frequency of water intake":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()
