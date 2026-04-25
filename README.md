# European Bathing Water Quality Dashboard

An interactive Streamlit dashboard analysing European bathing water quality 
from 1990 to 2024, built for the 5DATA004C Data Science Project Lifecycle 
Individual Coursework.

## Dataset
- **Source:** European Environment Agency (EEA)
- **Dataset:** Bathing Water Directive – Status of Bathing Water (1990–2024)
- **Link:** https://www.eea.europa.eu/en/datahub/datahubitem-view/c3858959-90da-4c1b-b9ca-492db0e514df

## Live Dashboard
[Click here to view the live app](https://malkiparis-bathing-water-dashboard-app-ghtxko.streamlit.app)

## Features
- Filter by country, year and water type
- KPI metrics: total sites, excellent count, poor count, % excellent
- Quality rating bar chart
- Coastal vs Inland vs Lake pie chart
- Quality trends over time (1990–2024)
- Country comparison bar chart
- Interactive map of all bathing sites
- Beach name search with full quality history

## Project Structure
- `app.py` — Main Streamlit dashboard application
- `bathing_water_clean.csv` — Cleaned dataset used by the app
- `data_cleaning.ipynb` — Data cleaning notebook (Google Colab)
- `requirements.txt` — Python dependencies

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- GitHub + Streamlit Community Cloud
