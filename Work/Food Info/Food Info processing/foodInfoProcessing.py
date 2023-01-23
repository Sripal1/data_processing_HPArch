from audioop import avg
import pandas as pd
import csv
from datetime import datetime
import googletrans
from googletrans import *

translator=googletrans.Translator()

# Creating a list of all empty line numbers
inFile = open("sortedFoodInfoDataFinal.csv", "r")
lineCounter = 0
headers = inFile.readline()
headers=headers.split(",")[1:]
lineCounter += 1
emptyLineList = []
for line in inFile:
    lineCounter += 1
    if line.split() == []:
        emptyLineList.append(lineCounter)
# print(emptyLineList)

with open('sortedFoodInfoDataFinal.csv') as csvfile:
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

newList=[]
for j in dateGroupedList:
    for item in j:
        tempList=[]
        for i in range(len(item)):
            if i==16:
                translatedText=translator.translate(item[i],dest="en")
                # print(translatedText.text.split("+"))
                tempTranslatedWords=""
                for char in translatedText.text.split("+"):
                    if char=="":
                        continue
                    elif char==translatedText.text.split("+")[-2]:
                        tempTranslatedWords+=char
                    else:
                        tempTranslatedWords+=char+"+"
                tempList.insert(0,tempTranslatedWords)
            elif i==21:
                translatedText=translator.translate(item[i],dest="en")
                tempList.insert(1,str(translatedText.text))
            elif i==11:
                continue
            elif i==10:
                tempList.insert(0,item[i])
            else:
                tempList.append(item[i].strip())
        newList.append(tempList)
# print(newList)

outFile = open("Final_Processed_Data_FoodInfo.csv", "w")
headersToPrint=headers[:]
for item in ['start_time']:
    headersToPrint.remove(item)
for item in ['name','serving_description','start_date'][::-1]:
    headersToPrint.remove(item)
    headersToPrint.insert(0,item)
for header in headersToPrint:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for item in newList:
    for i in range(len(item)):
        if i==len(item)-1:
            outFile.write(item[i].strip()+"\n")
        else:
            outFile.write(item[i]+",")
# print(newList)

# dictToPrint = {}
# for item in newList:
#     totalWaterIntake = 0
#     waterQuantityPerIntake = {}
#     frequency = 0
#     for data in item:
#         totalWaterIntake += float(data[2].strip())
#         if (float(data[2].strip())) in waterQuantityPerIntake:
#             waterQuantityPerIntake[float(data[2].strip())] += 1
#         else:
#             waterQuantityPerIntake[float(data[2].strip())] = 1
#         frequency += 1
#     waterQuantityPerIntake = totalWaterIntake/frequency
#     dictToPrint[data[0]] = {"Total Water Intake (ml)": totalWaterIntake, "Average water Quantity per Intake (ml)": waterQuantityPerIntake,
#                             "Frequency of water intake": frequency}
# print(dictToPrint)


# headers = [
#     "Date", "Total Water Intake (ml)", "Average water Quantity per Intake (ml)", "Frequency of water intake"]

# for header in headers:
#     if header == headers[-1]:
#         outFile.write(header+"\n")
#     else:
#         outFile.write(header+",")
# for date, values in dictToPrint.items():
#     outFile.write(date+",")
#     for title, value in values.items():
#         if title == "Frequency of water intake":
#             outFile.write(str(value)+"\n")
#         else:
#             outFile.write(str(value)+",")
# outFile.close()
