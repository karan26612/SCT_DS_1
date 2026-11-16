# Population Comparison Chart

A Python script that creates a horizontal bar chart comparing the population of selected countries. It uses the latest year available in the included World Development Indicators CSV, preferring 2025 when present.

## Requirements

- Python 3
- pandas
- matplotlib

Install the required packages:

```bash
python -m pip install pandas matplotlib
```

## Files

Keep these files together in the same folder:

- `population_chart.py`
- `API_SP.POP.TOTL_DS2_en_csv_v2_58181.csv`

## Run the script

```bash
python population_chart.py
```

The chart is saved beside the script as `population_selected_countries_<year>.png` and is also displayed on screen.

## Data

The CSV contains total population by country and year. The chart compares selected countries and displays values in millions. It does **not** contain age or gender breakdowns, so this script does not show age or gender distributions.

Data source: [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators), World Bank.

## Customization

Edit the `countries` list in `population_chart.py` to change which countries appear in the chart.