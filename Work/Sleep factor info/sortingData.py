import csv
import operator
import json

# Reads data from input file and writes it to a new csv file with correct headers

# Enter your file name(include ".csv" at the end)
fileToRead = "com.samsung.shealth.sleep.202111291535 - şığçşğ - şığçşğ.csv"
# do not leave spaces inbetween the words (recommend camel casing)
dataType = "sleepFactors"
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
        if i == headers[25]:
            outFile.write("start_date"+",")
            outFile.write("start_time"+",")
        elif i == headers[-1]:
            outFile.write(i)
        else:
            outFile.write(i+",")

    # Sorts data in ascending order based on dates
    csv_list.sort(key=lambda l: l[25], reverse=False)
    newList = []
    for i in csv_list:
        tempList = []
        counter = 0
        for j in range(len(i[:-1])):  # iterates through rows except last cell which is empty
            if counter == 25:
                tempList.append(i[j][:11])  # date
                tempList.append(i[j][11:])  # time
            else:
                tempList.append(i[j])
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
