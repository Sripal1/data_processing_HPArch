import csv
import operator
import json
import pandas as pd
import googletrans
from googletrans import *
from datetime import datetime

translator=googletrans.Translator()

# Reads data from input file and writes it to a new csv file with correct headers

# Enter your file name(include ".csv" at the end)

fileToRead = "com.samsung.health.heart_rate.2021120410 copy.csv"
dataType = "HeartRate"
outFileName = "sorted"+dataType+"Data.csv"


def sortData():
    file = open(fileToRead)
    firstLine = file.readline()  # Line with wrong headers
    headers = file.readline().split(",")  # Line with correct headers

    csv_reader = csv.reader(file, delimiter=",")
    # List of all data from and including row of index 3
    csv_list = list(csv_reader)
    file.close()
    outFile = open("sorted"+dataType+"Data.csv", "w")

    for i in headers:
        if i == headers[7]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    # csv_list.sort(key=lambda l: l[7], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        for j in i[:-1]:  # iterates through rows except last cell which is empty
            if counter == 7:
                translatedText=translator.translate(j,dest="en")
                # print(translatedText.text)
                tempList.append(translatedText.text[:4]+"-"+translatedText.text[6:8]+"-"+translatedText.text[10:12])  # date
                if "PM" in translatedText.text:
                    timeSplit=j[17:].split(":")
                    if timeSplit[0]!="12":
                        hourTime=int(timeSplit[0])+12
                    else:
                        hourTime=int(timeSplit[0])
                    tempList.append(str(hourTime)+":"+str(timeSplit[1]+":"+str(timeSplit[2])))  # time
                else:
                    tempList.append(j[17:])  # time
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
