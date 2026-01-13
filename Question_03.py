import pandas as pd
import glob
import os
import math

files = glob.glob("temperatures/*.csv")

all_data = []
for f in files:
    all_data.append(pd.read_csv(f))

data = pd.concat(all_data, ignore_index=True)

months = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

season_of = {
    "December":"Summer","January":"Summer","February":"Summer",
    "March":"Autumn","April":"Autumn","May":"Autumn",
    "June":"Winter","July":"Winter","August":"Winter",
    "September":"Spring","October":"Spring","November":"Spring"
}

season_values = {"Summer": [], "Autumn": [], "Winter": [], "Spring": []}
station_values = {}

for i in range(len(data)):
    sid = data.loc[i, "STN_ID"]
    name = data.loc[i, "STATION_NAME"]
    key = (sid, name)
    if key not in station_values:
        station_values[key] = []
    for m in months:
        if m in data.columns:
            v = data.loc[i, m]
            if pd.notna(v):
                v = float(v)
                station_values[key].append(v)
                season_values[season_of[m]].append(v)

with open("average_temp.txt", "w", encoding="utf-8") as f:
    for s in ["Summer","Autumn","Winter","Spring"]:
        if len(season_values[s]) > 0:
            avg = sum(season_values[s]) / len(season_values[s])
            f.write(f"{s}: {avg:.1f}°C\n")
        else:
            f.write(f"{s}: No data\n")

ranges = {}
for k in station_values:
    vals = station_values[k]
    if len(vals) > 0:
        ranges[k] = max(vals) - min(vals)

max_range = max(ranges.values())

with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
    for k in ranges:
        if abs(ranges[k] - max_range) < 0.00001:
            f.write(f"{k[1]}: {ranges[k]:.1f}°C\n")

stds = {}
for k in station_values:
    vals = station_values[k]
    if len(vals) > 0:
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        stds[k] = math.sqrt(var)

min_std = min(stds.values())
max_std = max(stds.values())

with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
    for k in stds:
        if abs(stds[k] - min_std) < 0.00001:
            f.write(f"Most Stable: {k[1]} ({min_std:.1f}°C)\n")
    for k in stds:
        if abs(stds[k] - max_std) < 0.00001:
            f.write(f"Most Variable: {k[1]} ({max_std:.1f}°C)\n")
