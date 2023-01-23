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

print(timeDateDict)


outFile = open("Final_Processed_Data_Sleep_2.csv", "w")
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
