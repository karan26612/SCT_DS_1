from pathlib import Path
import csv

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# Keep the CSV file in the same folder as this script.
csv_path = Path(__file__).with_name(
    "API_SP.POP.TOTL_DS2_en_csv_v2_58181.csv"
)

if not csv_path.exists():
    raise FileNotFoundError(
        f"CSV file not found:\n{csv_path}\n"
        "Keep the CSV file and this Python script in the same folder."
    )

# Find the row containing the actual column headers.
with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
    rows = csv.reader(file)
    header_row = next(
        (
            index
            for index, row in enumerate(rows)
            if row and row[0].strip().strip('"') == "Country Name"
        ),
        None,
    )

if header_row is None:
    raise ValueError(
        "Could not find the 'Country Name' header. "
        "Check that this is a World Development Indicators CSV."
    )

# Read the data, skipping the metadata above the header.
df = pd.read_csv(
    csv_path,
    skiprows=header_row,
    encoding="utf-8-sig",
    skipinitialspace=True,
)

# Clean column names and remove any empty trailing columns.
df.columns = [str(column).strip().strip('"') for column in df.columns]
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

# Identify available year columns.
year_columns = [
    column for column in df.columns
    if str(column).strip().isdigit()
]

if not year_columns:
    raise ValueError("No year columns were found in the CSV.")

# Use 2025 if available; otherwise, use the latest year in the file.
year = "2025" if "2025" in year_columns else max(year_columns, key=int)

# Convert the selected year's population values to numbers.
df[year] = pd.to_numeric(df[year], errors="coerce")
df["Country Name"] = df["Country Name"].astype(str).str.strip()

# Select countries for a readable comparison.
countries = [
    "India",
    "China",
    "United States",
    "Indonesia",
    "Pakistan",
    "Nigeria",
    "Brazil",
    "Bangladesh",
    "Russian Federation",
    "Ethiopia",
]

chart_data = (
    df[df["Country Name"].isin(countries)]
    .dropna(subset=[year])
    .copy()
)

if chart_data.empty:
    raise ValueError(
        f"No population data found for the selected countries in {year}. "
        "Check the country names and year in the CSV."
    )

# Convert population totals to millions and sort for display.
chart_data["Population (millions)"] = chart_data[year] / 1_000_000
chart_data = chart_data.sort_values("Population (millions)", ascending=True)

# Highlight India and use a contrasting color for the other countries.
colors = [
    "#E07A3F" if country == "India" else "#3977A8"
    for country in chart_data["Country Name"]
]

# Create the chart.
fig, ax = plt.subplots(figsize=(11, 7), facecolor="#F7F8FA")
ax.set_facecolor("#F7F8FA")

bars = ax.barh(
    chart_data["Country Name"],
    chart_data["Population (millions)"],
    color=colors,
    height=0.68,
    zorder=3,
)

# Add population labels at the end of each bar.
max_population = chart_data["Population (millions)"].max()
label_offset = max_population * 0.015

for bar, value in zip(bars, chart_data["Population (millions)"]):
    ax.text(
        value + label_offset,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,.1f}",
        va="center",
        ha="left",
        fontsize=9,
        color="#263238",
    )

# Titles and axis labels.
ax.set_title(
    f"Population of Selected Countries, {year}",
    loc="left",
    fontsize=18,
    fontweight="bold",
    color="#1F2933",
    pad=16,
)
ax.set_xlabel("Population (millions)", fontsize=11, labelpad=10)
ax.set_ylabel("")

# Style the axis and grid.
ax.set_xlim(0, max_population * 1.15)
ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.set_axisbelow(True)
ax.grid(axis="x", color="#D9DEE5", linewidth=0.8, zorder=0)
ax.tick_params(axis="both", labelsize=10, length=0, colors="#38434D")

for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)

ax.spines["bottom"].set_color("#B8C0C8")

# Add a source note.
fig.text(
    0.125,
    0.025,
    "Source: World Development Indicators (World Bank). "
    "Population values are shown in millions.",
    fontsize=8,
    color="#66727D",
)

fig.tight_layout(rect=(0, 0.06, 1, 1))

# Save the chart beside this script.
output_path = Path(__file__).with_name(
    f"population_selected_countries_{year}.png"
)
fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor(),
)

print(f"Chart saved to: {output_path}")
plt.show()