import csv
import operator
import json
import time

heartRateFile = "sortedHeartRateData.csv"
finalFile = "1003_C011_processed.csv"

file1 = open(heartRateFile)
headers1 = file1.readline().split()
csv_reader_1 = csv.reader(file1, delimiter=",")
csv_list_1 = list(csv_reader_1)

file2 = open(finalFile)
headers2 = file2.readline().split()
csv_reader_2 = csv.reader(file2, delimiter=",")
csv_list_2 = list(csv_reader_2)

print(csv_list_2)
