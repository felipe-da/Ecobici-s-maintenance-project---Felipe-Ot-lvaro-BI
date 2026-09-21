"""
analyze_ecobici_data.py

Ecobici Bike Usage Analysis - Box Plots & Top Bikes
-----------------------------------------------------
Author: Felipe Otalvaro
LinkedIn: https://www.linkedin.com/in/felipe-ot%C3%A1lvaro-agudelo/

This script reads the cleaned dataset produced by clean_ecobici_data.py
and generates:

1. A box plot of daily bike usage: for every bike, on every day it was
   used, the total number of minutes it was ridden. This shows how
   usage (and therefore mechanical stress) is distributed across the
   fleet on a day-to-day basis.

2. A box plot of monthly bike usage: the same idea, but aggregated per
   bike, per month.

3. A comparison of the 5 most-used bikes in July 2026 (by total minutes
   ridden) against the average bike's usage that same month, to see how
   much more stress the busiest bikes are under relative to the fleet.

Output:
Two PNG files (daily_usage_boxplot.png, monthly_usage_boxplot.png) saved
to a "plots" subfolder, plus printed summary stats in the terminal.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG - adjust this path if your files live somewhere else
# ---------------------------------------------------------------------------
DATA_FOLDER = Path(r"C:\Users\felip\Downloads\ecobici")
CLEAN_FILE = DATA_FOLDER / "ecobici_clean.csv"
OUTPUT_FOLDER = DATA_FOLDER / "plots"
OUTPUT_FOLDER.mkdir(exist_ok=True)


def load_clean_data() -> pd.DataFrame:
    """Load the cleaned dataset and add a few helper columns used across all analyses."""
    df = pd.read_csv(CLEAN_FILE, parse_dates=["Retiro_Datetime", "Arribo_Datetime"])

    df["Duration_Minutes"] = df["Duration_Seconds"] / 60
    df["Ride_Date"] = df["Retiro_Datetime"].dt.date
    df["Ride_Month"] = df["Retiro_Datetime"].dt.to_period("M")

    return df


def plot_daily_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Box plot showing, for each bike/day combination, the total number of
    minutes that bike was in use. Outlier points are hidden (showfliers=False)
    since with thousands of bike-days there will always be some extreme
    values that would otherwise flatten the rest of the plot visually.
    """
    daily_usage = (
        df.groupby(["Bici", "Ride_Date"])["Duration_Minutes"]
        .sum()
        .reset_index(name="Total_Minutes")
    )

    plt.figure(figsize=(6, 6))
    plt.boxplot(daily_usage["Total_Minutes"], vert=True, showfliers=False)
    plt.title("Daily Bike Usage\n(minutes ridden per bike, per day)")
    plt.ylabel("Minutes ridden")
    plt.tight_layout()
    plt.savefig(OUTPUT_FOLDER / "daily_usage_boxplot.png", dpi=150)
    plt.close()

    print("\n--- Daily usage summary (minutes per bike per day) ---")
    print(daily_usage["Total_Minutes"].describe())

    return daily_usage


def plot_monthly_usage(df: pd.DataFrame) -> pd.DataFrame:
    """Same idea as the daily plot, but aggregated per bike, per month."""
    monthly_usage = (
        df.groupby(["Bici", "Ride_Month"])["Duration_Minutes"]
        .sum()
        .reset_index(name="Total_Minutes")
    )

    plt.figure(figsize=(6, 6))
    plt.boxplot(monthly_usage["Total_Minutes"], vert=True, showfliers=False)
    plt.title("Monthly Bike Usage\n(minutes ridden per bike, per month)")
    plt.ylabel("Minutes ridden")
    plt.tight_layout()
    plt.savefig(OUTPUT_FOLDER / "monthly_usage_boxplot.png", dpi=150)
    plt.close()

    print("\n--- Monthly usage summary (minutes per bike per month) ---")
    print(monthly_usage["Total_Minutes"].describe())

    return monthly_usage


def top_bikes_july(monthly_usage: pd.DataFrame):
    """
    Identifies the 5 most-used bikes in July 2026 (by total minutes ridden)
    and compares their usage to the average bike's usage that same month.
    """
    july_period = pd.Period("2026-07", freq="M")
    july = monthly_usage[monthly_usage["Ride_Month"] == july_period]

    if july.empty:
        print("\nNo July 2026 data found - check that a '2026-07.csv' file was included.")
        return

    average_minutes = july["Total_Minutes"].mean()
    top5 = july.sort_values("Total_Minutes", ascending=False).head(5)

    print("\n--- Top 5 most-used bikes in July 2026 ---")
    for _, row in top5.iterrows():
        multiple = row["Total_Minutes"] / average_minutes
        print(
            f"Bike {int(row['Bici'])}: {row['Total_Minutes']:.0f} minutes "
            f"({multiple:.1f}x the average bike)"
        )

    print(f"\nAverage bike usage in July 2026: {average_minutes:.0f} minutes")


def main():
    df = load_clean_data()

    plot_daily_usage(df)
    monthly_usage = plot_monthly_usage(df)
    top_bikes_july(monthly_usage)

    print(f"\nPlots saved to: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
