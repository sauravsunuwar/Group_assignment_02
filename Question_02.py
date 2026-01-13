import os
import pandas as pd

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

MONTH_TO_NUM = {m: i + 1 for i, m in enumerate(MONTHS)}
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

INPUT_FOLDER = "temperatures"
AVG_TEMP_FILE = "average_temp.txt"
TEMP_RANGE_FILE = "largest_temp_range_station.txt"
STABILITY_FILE = "temperature_stability_stations.txt"

def season_from_month(month_num):
    # Season rules are kept in one function so they stay clear and easy to adjust.
    if month_num in (12, 1, 2):
        return "Summer"
    if month_num in (3, 4, 5):
        return "Autumn"
    if month_num in (6, 7, 8):
        return "Winter"
    return "Spring"

def read_all_temperature_files(folder):
    rows = []

    # Reading all CSV files allows the program to scale when new years are added.
    for filename in sorted(os.listdir(folder)):
        if not filename.lower().endswith(".csv"):
            continue

        df = pd.read_csv(os.path.join(folder, filename))

        # Different datasets use different station labels, so this avoids hard failures.
        station_col = "STATION_NAME" if "STATION_NAME" in df.columns else "STN_ID"

        # Converting months into rows creates one consistent structure for analysis.
        available_months = [m for m in MONTHS if m in df.columns]
        if not available_months:
            continue

        long_df = df.melt(
            id_vars=[station_col],
            value_vars=available_months,
            var_name="MonthName",
            value_name="MeanTemp"
        ).rename(columns={station_col: "Station"})

        # Converting early prevents hidden errors caused by text or symbols.
        long_df["MeanTemp"] = pd.to_numeric(long_df["MeanTemp"], errors="coerce")

        # Missing values are removed so they do not distort any calculations.
        long_df = long_df.dropna(subset=["MeanTemp", "Station"])

        long_df["MonthNum"] = long_df["MonthName"].map(MONTH_TO_NUM)
        long_df["Season"] = long_df["MonthNum"].apply(season_from_month)

        rows.append(long_df[["Station", "Season", "MeanTemp"]])

    # Joining once keeps the process clean and avoids slow repeated merging.
    if rows:
        return pd.concat(rows, ignore_index=True)
    return pd.DataFrame(columns=["Station", "Season", "MeanTemp"])

def write_seasonal_averages(data, out_file):
    # Mean is used because the task asks for overall seasonal averages, not extremes.
    seasonal = data.groupby("Season")["MeanTemp"].mean()

    with open(out_file, "w") as f:
        for s in SEASON_ORDER:
            if s in seasonal.index:
                f.write(f"{s}: {seasonal[s]:.1f}°C\n")
            else:
                f.write(f"{s}: No data\n")

def write_largest_range_station(data, out_file):
    # Range directly measures the biggest temperature difference at a station.
    g = data.groupby("Station")["MeanTemp"]
    station_max = g.max()
    station_min = g.min()
    station_range = station_max - station_min

    with open(out_file, "w") as f:
        if station_range.empty:
            f.write("No data\n")
            return

        best = station_range.max()

        # Ties are included because multiple stations can share the same range.
        winners = station_range[station_range == best].index.tolist()

        for st in winners:
            f.write(
                f"Station {st}: Range {best:.1f}°C "
                f"(Max: {station_max[st]:.1f}°C, Min: {station_min[st]:.1f}°C)\n"
            )

def write_stability(data, out_file):
    # Standard deviation is used because it shows how consistent temperatures are.
    stds = data.groupby("Station")["MeanTemp"].std()

    with open(out_file, "w") as f:
        if stds.empty:
            f.write("No data\n")
            return

        min_std = stds.min()
        max_std = stds.max()

        # Supporting ties keeps the results fair and complete.
        most_stable = stds[stds == min_std].index.tolist()
        most_variable = stds[stds == max_std].index.tolist()

        f.write("Most Stable:\n")
        for st in most_stable:
            f.write(f"Station {st}: StdDev {min_std:.1f}°C\n")

        f.write("\nMost Variable:\n")
        for st in most_variable:
            f.write(f"Station {st}: StdDev {max_std:.1f}°C\n")

def main():
    data = read_all_temperature_files(INPUT_FOLDER)

    # Separate output files keep results organised and easy to verify.
    write_seasonal_averages(data, AVG_TEMP_FILE)
    write_largest_range_station(data, TEMP_RANGE_FILE)
    write_stability(data, STABILITY_FILE)

    print("Finished! Output files created:")
    print("-", AVG_TEMP_FILE)
    print("-", TEMP_RANGE_FILE)
    print("-", STABILITY_FILE)

if __name__ == "__main__":
    main()
