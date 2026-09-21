# Ecobici Bike Usage Analysis

Data analysis project exploring how Ecobici (Mexico City's bike-share system) could shift from purely reactive maintenance to a data-driven preventive model. This project cleans and analyzes ride data to identify usage patterns and flag the bikes under the most mechanical stress before they fail.

## Why this project

Ecobici currently sends bikes for maintenance on a fixed 60-day schedule, plus reactive fixes whenever a user reports an issue. This works, but it's not preventive — a heavily used bike and a lightly used bike get treated the same way between checkups. This project uses Ecobici's open ride data to see whether usage intensity (measured through ride duration, since distance isn't available in the dataset) can help predict which bikes are most at risk and should be prioritized for preventive maintenance.

## Data

Source: [Ecobici Open Data](https://ecobici.cdmx.gob.mx/en/open-data), monthly ride files for January–August 2026.

Each raw file contains one row per ride, with the rider's gender and age, the bike ID, and the departure/arrival station, date, and time.

## Project structure

```
ecobici-analysis/
├── clean_ecobici_data.py       # Combines and cleans the 8 monthly CSVs
├── analyze_ecobici_data.py     # Generates box plots and the top-5 bikes analysis
├── plots/
│   ├── daily_usage_boxplot.png
│   └── monthly_usage_boxplot.png
└── README.md
```

## Data cleaning

`clean_ecobici_data.py` combines all monthly files into a single dataset and applies the following rules:

- **Drops rows with no bike ID** — a ride can't be attributed to a specific bike without one.
- **Calculates ride duration in seconds** from the departure and arrival date/time columns.
- **Removes rides shorter than 2 minutes** — these likely reflect a user picking up a bike, immediately noticing something was wrong with it, and returning it right away, rather than genuine use.
- **Removes rides longer than 2 hours** — Ecobici's standard membership only covers 45 minutes of continuous use per ride (90 on weekends) before extra charges apply, so legitimate rides rarely run this long. A ride this length more likely reflects a system/logging error than actual continuous riding.

## Setup

**1. Clone the repository**
```
git clone https://github.com/<your-username>/ecobici-analysis.git
cd ecobici-analysis
```

**2. Download the data**
Download the monthly CSV files from [Ecobici's open data portal](https://ecobici.cdmx.gob.mx/en/open-data) and place them in the project folder, named `2026-01.csv` through `2026-08.csv`.

**3. Create and activate a virtual environment**
```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

**4. Install dependencies**
```
pip install pandas matplotlib
```

## How to run

Run the cleaning script first — the analysis script depends on the clean CSV it produces:

```
python clean_ecobici_data.py
python analyze_ecobici_data.py
```

`clean_ecobici_data.py` will print how many rows were removed at each cleaning step and save `ecobici_clean.csv`.

`analyze_ecobici_data.py` will print summary statistics and the top 5 most-used bikes in July 2026, and save two box plot images to a `plots/` folder:

- `daily_usage_boxplot.png` — minutes ridden per bike, per day
- `monthly_usage_boxplot.png` — minutes ridden per bike, per month

## Results

*(Add your key findings here once you have the numbers — e.g. average daily/monthly usage, how much busier the top quartile of bikes is, and how the 5 busiest bikes in July compared to the fleet average.)*

## Next steps

- Extend the analysis to stations (busiest stations, coverage gaps).
- Incorporate external factors (weather, elevation, road conditions) if that data becomes available.
- Explore potential system expansion using station usage and geographic context.

## Author

**Felipe Otálvaro**
[LinkedIn](https://www.linkedin.com/in/felipe-ot%C3%A1lvaro-agudelo/)
