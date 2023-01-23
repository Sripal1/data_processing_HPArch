import pandas as pd

df = pd.read_csv("pokemon_data.csv")

pd.set_option('display.max_rows', 9999)
pd.set_option('display.max_columns', 9999)
pd.set_option('display.width', 1000)

# print(df)
print(df.head(3))  # prints first 3 lines
# print(df.tail(3))  # prints last 3 lines

# .txt files have \t as the delimeter
# df=pd.read_csv("pokemon.txt", delimiter= "\t")

# reading headers/titles
# print(df.columns)

# reading each column
# print(df["Name"][0:5])

# read mulitple columns not necessarily in order
# print(df[["Name","Type 1", "HP"]])

# read each row
