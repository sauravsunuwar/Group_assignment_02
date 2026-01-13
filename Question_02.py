import os
import pandas as pd

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"

all_data = []

folder = "temperatures"
files = os.listdir(folder)

for file in files:
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        df = pd.read_csv(path)

        if "STATION_NAME" in df.columns:
            station_col = "STATION_NAME"
        else:
            station_col = "STN_ID"

        for month in MONTHS:
            if month in df.columns:
                temp_data = df[[station_col, month]]
                temp_data = temp_data.rename(columns={station_col: "Station", month: "MeanTemp"})
                temp_data["Month"] = month
                all_data.append(temp_data)

data = pd.concat(all_data, ignore_index=True)

month_numbers = {
    "January":1, "February":2, "March":3, "April":4, "May":5, "June":6,
    "July":7, "August":8, "September":9, "October":10, "November":11, "December":12
}

data["MonthNum"] = data["Month"].map(month_numbers)
data["Season"] = data["MonthNum"].apply(get_season)
data["MeanTemp"] = pd.to_numeric(data["MeanTemp"], errors="coerce")
data = data.dropna()

season_avg = data.groupby("Season")["MeanTemp"].mean()

f = open("average_temp.txt", "w")
for s in ["Summer", "Autumn", "Winter", "Spring"]:
    if s in season_avg:
        f.write(s + ": " + str(round(season_avg[s], 1)) + "°C\n")
f.close()

max_temps = data.groupby("Station")["MeanTemp"].max()
min_temps = data.groupby("Station")["MeanTemp"].min()
ranges = max_temps - min_temps

largest_range = ranges.max()
stations = ranges[ranges == largest_range].index

f = open("largest_temp_range_station.txt", "w")
for st in stations:
    f.write("Station " + str(st) + ": Range " + str(round(largest_range,1)) +
            "°C (Max: " + str(round(max_temps[st],1)) +
            "°C, Min: " + str(round(min_temps[st],1)) + "°C)\n")
f.close()

std_dev = data.groupby("Station")["MeanTemp"].std()

min_std = std_dev.min()
max_std = std_dev.max()

stable = std_dev[std_dev == min_std].index
variable = std_dev[std_dev == max_std].index

f = open("temperature_stability_stations.txt", "w")

f.write("Most Stable:\n")
for st in stable:
    f.write(str(st) + ": StdDev " + str(round(min_std,1)) + "°C\n")

f.write("\nMost Variable:\n")
for st in variable:
    f.write(str(st) + ": StdDev " + str(round(max_std,1)) + "°C\n")

f.close()

print("Finished! All answer files created.")
