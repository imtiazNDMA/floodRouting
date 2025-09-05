## Historical Flood Flow Analysis

Interactive analytics and visualization for river inflows at key barrages, with a focus on comparative flood-period analysis. This repository contains a Dash (Plotly) web app, supporting notebooks, and data/assets to explore historical flow patterns and flood timelines.


## Highlights

- Interactive dashboard built with Dash/Plotly
  - Select one or more barrages (multi-select)
  - Filter by year or show all years
  - Hover tooltips, unified crosshair, and flood-period highlighting
- Sensible fallback: if input data is unavailable, the app generates sample data so you can explore UI/UX immediately
- Extensible: easy to add barrages, tune flood periods, or point to different Excel sheets
- Notebooks included for exploratory and ad‑hoc analyses


## Repository Structure

- Flood_Hist_Analysis (3).py — Main Dash app (entry point)
- main.py — Placeholder (empty)
- main.ipynb — Notebook (exploratory)
- easternSide.ipynb — Notebook (exploratory)
- data/ — Data folder (currently empty; you can place custom inputs here)
- results/ — Output folder (currently empty)
- assets/, *.png, *.jpeg, *.jpg — Images and logos used in documents/dashboards

Note: Some media files (e.g., ndma-logo.png) are provided for presentation and branding.

## Requirements

- Python 3.9+ (tested on Windows)
- Recommended packages:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - cartopy

Install via pip:

```
pip install pandas numpy matplotlib seaborn cartopy
```

Optionally, use a virtual environment:

- Windows (CMD/PowerShell):
  ```
  python -m venv .venv
  .venv\Scripts\activate
  pip install -U pip
  pip install dash plotly pandas numpy openpyxl
  ```
- macOS/Linux:
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -U pip
  pip install dash plotly pandas numpy openpyxl
  ```

## Dashboard Features

- Barrage selector (multi-select): choose specific structures or All
- Year selector: focus on a particular year or All Years
- Main flow chart: lines of inflow vs. date with distinct color per barrage
- Flood-period highlights: shaded regions for flood windows in 2014, 2022, 2023
- Responsive layout and readable legends

Note: Additional charts (flood comparison, yearly peaks, monthly patterns) are scaffolded and can be re-enabled by uncommenting the corresponding sections and callbacks in the script.


## Customization

- Add or edit barrages: update `dropdown_options` in `Flood_Hist_Analysis (3).py`
- Flood periods: adjust the `flood_periods` dictionary to set start/end dates per year
- Colors: tweak `all_colors` in `update_main_chart`
- Data cleaning/mapping: extend logic in `load_barrage_data` to accommodate new column names
- Default sample data: modify `create_sample_data` to include other structures/years


## Notebooks

- `main.ipynb`, `easternSide.ipynb` contain exploratory or ad‑hoc analysis. Open in Jupyter Lab/Notebook to review and run. These are not required to run the Dash app.

Launch Jupyter (optional):
```
jupyter lab
```


## Troubleshooting

- App loads but shows generic patterns: likely running on generated sample data. Update the file path to your Excel dataset.
- Excel read errors: ensure the file exists, sheet name is correct, and `openpyxl` is installed.
- Port already in use: change the `port` in `app.run(debug=True, port=8050)`.
- Blank/empty charts: confirm your data contains expected columns and that dates parse correctly.


## Roadmap Ideas

- Re-enable and refine the comparison/summary charts
- Export charts or computed statistics to `results/`
- Add CLI or config file for data path/sheet name
- Add tests and CI for data parsing and chart generation
- Provide a requirements.txt and pinned versions


## License

No license file is present. By default, all rights are reserved. If you intend to open-source this project, add a LICENSE file (e.g., MIT, Apache 2.0) and update this section accordingly.


## Acknowledgments

- Plotly/Dash for interactive visualization
- Pandas and NumPy for data processing
- Sample and historical datasets courtesy of the project stakeholders
