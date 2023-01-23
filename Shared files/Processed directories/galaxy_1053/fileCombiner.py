import os
import pathlib
import glob
import pandas as pd
import csv
from heartRate import *
from csv import writer

dir_path = pathlib.Path().resolve()
extension = 'csv'
os.chdir(dir_path)
result = glob.glob('*.{}'.format(extension))
# print(result)
filesToProcess = ['Final_Processed_Data_Sleep.csv', 'Final_Processed_Data_Steps.csv',
                  'Final_Processed_Data_SleepFactor.csv', 'Final_Processed_Data_HeartRate.csv']
filesToBeRemoved=[]

for file in result:
    if file not in filesToProcess:
        try:
            result.remove(file)
        except:
            print("Could not remove file!")

l3 = [x for x in result if x not in filesToProcess]
for item in l3:
    try:
        result.remove(item)
    except:
        print("Could not remove "+item)
newResult=sorted(result)
print(newResult)

outputFile = pd.read_csv(newResult[0])

for i in range(len(newResult[1:])):
    inputFile = pd.read_csv(newResult[i+1])

    # using merge function by setting how='outer'
    output4 = pd.merge(inputFile, outputFile, on='Date', how='outer')

    # displaying result
    output4.to_csv("combinedFiles.csv")
    outputFile = pd.read_csv("combinedFiles.csv")

file = open("combinedFiles.csv")
filesToBeRemoved.append("combinedFiles.csv")
headers = file.readline().split(",")
# print(headers)

newHeaders = []
columnsToRemove = []
for header in headers:
    tempHeader = header.strip().split("_")[0]
    if header.strip().split(":")[0] == "Unnamed":
        columnsToRemove.append(header)
    newHeaders.append(tempHeader)
columnsToRemove.append('')

df = pd.read_csv("combinedFiles.csv")
df = df.sort_values(by="Date")

df = df.set_axis(newHeaders, axis=1, inplace=False)
for obsoleteHeader in columnsToRemove:
    df=df.drop(obsoleteHeader,1)
df.to_csv("galaxy_1053_CombinedFiles.csv")

with open('galaxy_1053_CombinedFiles.csv', 'a', newline='') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow([" "]+uniqueIDdata.split())
    f_object.close()

import os
for file in filesToBeRemoved:
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist "+file)