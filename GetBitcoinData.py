
import json
import pandas as pd

#Reads the file
with open("HistoricalDataBitcoin.json", "r") as f:
    data = json.load(f)

#Extract the data I need
ts = data["chart"]["result"][0]["timestamp"];
o = data["chart"]["result"][0]["indicators"]["quote"][0]["open"];
h = data["chart"]["result"][0]["indicators"]["quote"][0]["high"];
l = data["chart"]["result"][0]["indicators"]["quote"][0]["low"];
c = data["chart"]["result"][0]["indicators"]["quote"][0]["close"];

#Changes the Timestamps from Unix time to human time
dt = pd.to_datetime(ts, unit="s")

#Create Dataframe with extracted Data
df = pd.DataFrame({"Date": dt, "Open": o, "High": h, "Low": l, "Close": c})

#Deletes the 2 years as they are not fully completed
df = df[(df["Date"].dt.year != 2014) & (df["Date"].dt.year != 2025)] 
df["Date"] = df["Date"].dt.date

#Saves the clean data to a new csv file
df.to_csv("CleanHistoricalDataBitcoin.csv", index=False)

