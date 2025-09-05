# BlueDot — Flood Analysis

This repository is focused on flood analysis: collecting, cleaning, exploring, and visualizing river inflow and related data to understand historical and ongoing flood dynamics. A future portal/dashboard is planned and will integrate an AI assistant (agentic RAG-based) for interactive, question-driven exploration. For now, this repo is strictly for analysis workflows (scripts, notebooks, data assets).


## Scope (Current vs Future)

- Current
  - Jupyter notebooks and supporting data/files used for flood-related analysis
  - Reproducible, file-based workflows (no production web app)
- Future (planned)
  - A web portal/dashboard
  - Integrated agentic RAG assistant to answer questions, retrieve evidence, and generate charts/summaries


## Project Tree

An overview of the repository content. Items marked as legacy are not part of the active workflow.

```
bluedot/
├─ README.md
├─ main.ipynb
├─ easternSide.ipynb
├─ main.py                               # placeholder
├─ data/                                 # place input datasets here (currently empty)
├─ results/                              # place analysis outputs/exports here (currently empty)
├─ assets/
│  ├─ breaches.jpeg
│  └─ ndma-logo.png
├─ pm_dashboard_data.csv                 # auxiliary data (notebooks may reference)
├─ pong.csv                              # auxiliary data (notebooks may reference)
├─ historicalFlood.xlsx                  # example/reference workbook
├─ Breaching Section.xlsx                # example/reference workbook
├─ Marala, Qadirabad,Sulemanki,Balloki flows (2012 -2023).xlsx
├─ bulletin-26-06-2025-37.pdf            # reference document
├─ breaches.jpeg                         # media/figure
├─ breachingSection.png                  # media/figure
├─ easternSideOutFlows.png               # media/figure
├─ Flood_2014_peaks.png                  # media/figure
├─ Flood_2025_peaks.png                  # media/figure
├─ outFlowAnalysisOfGSWala.png           # media/figure
├─ outFlowAnalysisOfHarike.png           # media/figure
├─ frm.jpg                               # media/figure
├─ ndma-logo.png                         # media/figure
├─ Flood_Hist_Analysis (3).py            # legacy/experimental — not used; safe to ignore
└─ .qodo/                                # tooling metadata
```

Note: The legacy item above is retained in the tree for completeness but is not part of the current analysis workflow.


## Getting Started

### Environment

- Python 3.9+
- Recommended packages
  - jupyter, jupyterlab
  - pandas, numpy
  - openpyxl (Excel engine)
  - matplotlib, seaborn
  - plotly (optional, for interactive charts in notebooks)

Create and activate a virtual environment (Windows CMD/PowerShell):
```
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install jupyter jupyterlab pandas numpy openpyxl matplotlib seaborn plotly
```
macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install jupyter jupyterlab pandas numpy openpyxl matplotlib seaborn plotly
```

### Run Notebooks

1. Launch Jupyter Lab:
   ```
   jupyter lab
   ```
2. Open and execute:
   - main.ipynb
   - easternSide.ipynb
3. If needed, update file paths in the notebooks to point to your local datasets. Prefer keeping inputs in `data/` and writing outputs to `results/`.


## Data Expectations

Typical columns used in analyses (actual notebook code may adapt):
- date: parseable datetime
- inflow (cusecs): numeric
- structure/barrage: string identifier

You can place your Excel/CSV files in `data/` and update the notebook cells to load them. Example reference files are included at the repo root.


## Outputs

- Save derived tables, charts, and exports to `results/` to keep the root clean.
- Keep raw inputs in `data/` for a predictable structure.


## Roadmap (Portal + Agentic RAG Assistant)

Planned deliverable: a production-grade portal/dashboard with a conversational assistant capable of:
- Answering questions over flood data, bulletins, and historical archives
- Retrieving relevant evidence (timeseries slices, documents, figures)
- Generating on-demand charts and summaries

High-level plan:
- Data layer: schemas for timeseries (flows), geospatial layers, and documents (PDF/XLSX/CSV)
- Indexing & retrieval: vector search for documents, metadata filters, timeseries aggregation endpoints
- Agentic orchestration: tools for retrieval, analysis, and chart generation
- LLM framework: LangChain/LlamaIndex (or equivalent) with tool/function calling
- UI: modern web dashboard with chart components and a conversational pane

Milestones:
- Consolidate data-loading utilities (config-driven paths/column maps)
- Establish canonical datasets and validation checks
- Stand up a minimal RAG POC on local docs/derived summaries
- Define portal architecture and CI for reproducible analysis modules


## Housekeeping

- Legacy/experimental scripts are not part of current workflows and can be ignored
- Prefer relative paths to keep notebooks portable
- Large raw datasets should be kept out of version control when possible


## Disclaimer

This repository is currently an analysis workspace and not a production service. The portal and agentic RAG assistant are planned and will be built separately on top of the analysis outcomes documented here.
