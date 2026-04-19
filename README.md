# Indian Aviation Load Factor Analysis

## Project Overview

This project analyzes how efficiently Indian airlines fill their aircraft—both in terms of passengers and total payload—across different months and over multiple years.

Using official monthly traffic statistics from the Directorate General of Civil Aviation (DGCA), this analysis tracks two core metrics:

- **Passenger Load Factor (PLF)**: The percentage of available seats actually occupied.
- **Weight Load Factor (WLF)**: The percentage of the aircraft's total weight capacity utilized across passengers, freight, and mail.

By tracking these metrics from 2018 to 2025, the project uncovers seasonal demand patterns, cargo dependencies, and the dramatic COVID-19 collapse and recovery arc of the Indian aviation market.

## Key Findings & Visualizations

The analysis is broken down into three main data stories:

1. **Seasonal Demand Patterns (Heatmap)**
   - Analyzed 3 years of domestic data (2022-2025) across 8 airlines.
   - Identified consistent peak travel windows in February and December, and monsoon troughs around July-September.

2. **7-Year Recovery Arc (Line Chart)**
   - Tracked domestic PLF for 5 core carriers (Air India, Air India Express, Alliance Air, Blue Dart, IndiGo) from 2018-2025.
   - Mapped the dramatic PLF collapse during the 2020-21 COVID-19 period and evaluated the speed and stability of the post-pandemic recovery against an 80% industry benchmark.

3. **Cargo Dependency & The "Preighter" Pivot (Scatter Plot)**
   - Engineered a new metric: `PLF_vs_WLF_Gap` (WLF - PLF) to quantify cargo reliance.
   - Compared the pre-COVID (2018-19) baseline to the mid-COVID (2020-21) crisis, revealing how commercial airlines successfully pivoted to cargo-heavy operations to offset passenger losses.

## Tech Stack

- **Environment & Dependency Management**: uv
- **Data Processing**: pandas, numpy, openpyxl
- **Visualizations**: plotly (interactive), seaborn, matplotlib
- **Environment**: Jupyter Notebook

## Data Architecture

The data pipeline handles messy DGCA Excel templates, mapping inconsistent columns and missing dates into standardized formats:

- `data/raw/`: Original Excel files directly from DGCA.
- `data/processed/`: Standardized CSVs containing 12 months of clean data per session.
- `data/filtered/`: Master datasets explicitly sliced for the 3-Year Market View, 7-Year Recovery Trend, and the Mid-COVID Cargo Transition.

## Getting Started (Local Setup)

This project uses the uv package manager to guarantee 100% environment reproducibility.

1. **Install uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   (Windows users: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`)

2. **Clone the repository**
   ```bash
   git clone https://github.com/ARYAN-04/aviation-load-factor-analysis.git
   cd aviation-load-factor-analysis
   ```

3. **Sync the environment**
   This will read the uv.lock file and perfectly recreate the exact versions of all dependencies used in this project.
   ```bash
   uv sync
   ```

4. **Launch the analysis**
   ```bash
   uv run jupyter lab
   ```

## License

MIT License - See LICENSE file for details