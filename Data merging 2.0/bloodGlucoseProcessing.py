from audioop import avg
import pandas as pd
import csv
from datetime import datetime

# Creating a list of all empty line numbers
inFile = open("sortedBloodGlucoseDataFinal.csv", "r")
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

with open('sortedBloodGlucoseDataFinal.csv') as csvfile:
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

# newList=[]
# for j in dateGroupedList:
#     for item in j:
#         tempList=[]
#         for i in range(len(item)):
#             if i==16:
#                 translatedText=translator.translate(item[i],dest="en")
#                 # print(translatedText.text.split("+"))
#                 tempTranslatedWords=""
#                 for char in translatedText.text.split("+"):
#                     if char=="":
#                         continue
#                     elif char==translatedText.text.split("+")[-2]:
#                         tempTranslatedWords+=char
#                     else:
#                         tempTranslatedWords+=char+"+"
#                 tempList.insert(0,tempTranslatedWords)
#             elif i==21:
#                 translatedText=translator.translate(item[i],dest="en")
#                 tempList.insert(1,str(translatedText.text))
#             elif i==11:
#                 continue
#             elif i==10:
#                 tempList.insert(0,item[i])
#             else:
#                 tempList.append(item[i].strip())
#         newList.append(tempList)
# # print(newList)

# headersToPrint=headers[:]
# for item in ['start_time']:
#     headersToPrint.remove(item)
# for item in ['name','serving_description','start_date'][::-1]:
#     headersToPrint.remove(item)
#     headersToPrint.insert(0,item)
# for header in headersToPrint:
#     if header == headers[-1]:
#         outFile.write(header+"\n")
#     else:
#         outFile.write(header+",")
# for item in newList:
#     for i in range(len(item)):
#         if i==len(item)-1:
#             outFile.write(item[i].strip()+"\n")
#         else:
#             outFile.write(item[i]+",")
# print(newList)

mealTypePlan = {80001: "Fasting", 80002: "After meal", 80003: "Before breakfast", 80004: "After breakfast", 80005: "Before lunch", 80006: "After lunch",
                80007: "Before dinner", 80008: "After dinner", 80009: "After bedtime", 80010: "After snack", 80011: "Before meal", 80012: "General measurement", 80013:"Before sleep"}
bloodType={90001:"Whole blood",90002:"Plasma",90003:"Serum",-1:"Unknown blood sample"}
dictToPrint = {}
for item in dateGroupedList:
    totalInjectedInsulin = 0
    totalMedicationConsumed = 0
    totalGlucoseValue=0
    timeOfMeasurement={}
    typeOfMeasurement={}
    frequency=0
    for data in item:
        try:
            totalInjectedInsulin += float(data[0].strip())
            totalMedicationConsumed+=float(data[1].strip())
        except:
            totalInjectedInsulin += 0.0
            totalMedicationConsumed+= 0.0
        timeOfMeasurement[int(data[4].strip())] = mealTypePlan[int(data[4].strip())]
        typeOfMeasurement[int(data[-1].strip())] = bloodType[int(data[-1].strip())]
        totalGlucoseValue+=float(data[5].strip())
        frequency+=1
    avgGlucoseValue=totalGlucoseValue/frequency
    timeOfMeasurementStr=""
    typeOfMeasurementStr=""
    for value in timeOfMeasurement.values():
        timeOfMeasurementStr+=value+"+"
    for value in typeOfMeasurement.values():
        typeOfMeasurementStr+=value+"+"
    timeOfMeasurementStr=timeOfMeasurementStr[:-1]
    typeOfMeasurementStr=typeOfMeasurementStr[:-1]

    dictToPrint[data[2]] = {"Total Injected Insulin": totalInjectedInsulin, "Total Medication Consumed": totalMedicationConsumed,"Average blood sugar level": round(avgGlucoseValue,3),
                            "Time of measurements": timeOfMeasurementStr, "Type of blood used for measurement": typeOfMeasurementStr}
# print(dictToPrint)


headers = ["Date"]
for key,value in dictToPrint.items():
    for header,data in value.items():
        if header not in headers:
            headers.append(header)

outFile = open("Final_Processed_Data_BloodGlucose.csv", "w")
for header in headers:
    if header == headers[-1]:
        outFile.write(header+"\n")
    else:
        outFile.write(header+",")
for date, values in dictToPrint.items():
    outFile.write(date+",")
    for title, value in values.items():
        if title == "Type of blood used for measurement":
            outFile.write(str(value)+"\n")
        else:
            outFile.write(str(value)+",")
outFile.close()
