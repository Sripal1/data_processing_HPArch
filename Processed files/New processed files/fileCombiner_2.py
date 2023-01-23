import os
import pathlib
import glob
import pandas as pd
import csv
dir_path = pathlib.Path().resolve()
extension = 'csv'
os.chdir(dir_path)
result = glob.glob('*.{}'.format(extension))

specialFiles = ['combinedFiles.csv', 'finalCombinedFiles_2.csv',"finalCombinedFiles.csv"]
for item in specialFiles:
    try:
        result.remove(item)
    except:
        print("Could not remove file!")
        continue
# print(result)
newResult=sorted(result)
print(newResult)

outputFile = pd.read_csv(newResult[0])

for i in range(len(newResult[1:])):
    inputFile = pd.read_csv(newResult[i])

    # using merge function by setting how='outer'
    output4 = pd.merge(inputFile, outputFile, on='Date', how='outer')

    # displaying result
    output4.to_csv("combinedFiles.csv")
    outputFile = pd.read_csv("combinedFiles.csv")

file = open("combinedFiles.csv")
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
df.to_csv("finalCombinedFiles_2.csv")