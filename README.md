# DSA 210 Project — Demand Analysis for Plastic Buckets in the Dairy Industry

**Author:** Omer Dogru  
**Course:** DSA 210 — Introduction to Data Science (Spring 2026)  
**Institution:** Sabancı University

## Project Overview

This project analyzes the factors that affect weekly demand for plastic buckets used in the dairy industry. The sales data comes from my family's plastic injection factory in Osmaniye, which supplies buckets primarily to yogurt producers across Turkey. The goal is to systematically test whether observed patterns (such as higher sales in warmer periods) hold up to statistical scrutiny, and ultimately to predict bucket demand using machine learning.

## Research Questions

1. Do summer sales differ significantly from winter sales?
2. Is there a positive association between temperature and bucket demand?
3. Do all four seasons have different sales distributions?
4. Does Brent crude oil price (a proxy for plastic raw material cost) correlate with sales?
5. Does the USD/TRY exchange rate genuinely affect demand, or is the apparent correlation spurious?

## Data Sources 
| Dataset | Source | Frequency | Period |
| Plastic bucket sales (tons) | Family factory records | Weekly | 2023–2025 |
| Temperature & precipitation (10 cities) | [Open-Meteo Historical API](https://open-meteo.com/) | Daily → aggregated to weekly | 2023–2025 |
| Brent crude oil price | Yahoo Finance (`BZ=F`) | Daily → weekly | 2023–2025 |
| USD/TRY exchange rate | Yahoo Finance (`TRY=X`) | Daily → weekly | 2023–2025 |

The Turkey-wide temperature is computed as a population-weighted average across nine major cities (Istanbul, Ankara, Izmir, Bursa, Antalya, Konya, Adana, Gaziantep, Kayseri). Osmaniye (factory location) is kept as a separate signal.

## Repository Structure

```
dsa210/
├── README.md
├── AI_USAGE.md
├── requirements.txt
├── collect_data.py              # Fetches & merges all external datasets
├── 01_eda.ipynb                 # Exploratory Data Analysis
├── 02_hypothesis_tests.ipynb    # Statistical hypothesis tests
└── data/
    ├── raw/
    │   ├── haftalik_satis_2023_2025.xlsx
    │   ├── weather_daily.csv
    │   ├── brent_daily.csv
    │   └── usdtry_daily.csv
    └── processed/
        └── merged_weekly.csv
```

## How to Reproduce

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place the sales file at `data/raw/haftalik_satis_2023_2025.xlsx`.
3. Run the data collection script (this fetches weather and financial data from public APIs):
   ```bash
   python collect_data.py
   ```
4. Open the notebooks in Jupyter and run all cells:
   ```bash
   jupyter notebook 01_eda.ipynb
   jupyter notebook 02_hypothesis_tests.ipynb
   ```

## Progress

- [x] **17 March:** GitHub repo created
- [x] **31 March:** Project proposal submitted
- [x] **14 April:** Data collection, EDA, and hypothesis tests
- [ ] **5 May:** Machine learning models
- [ ] **18 May:** Final report and code submission

## Key Findings So Far

1. **Strong upward trend** in sales across 2023–2025, independent of seasonality.
2. **Clear seasonality** — summer sales are significantly higher than winter sales (Mann-Whitney U, p < 0.001).
3. **Temperature is a strong predictor** of weekly demand (Spearman ρ ≈ 0.6–0.7, p < 0.001).
4. **Brent oil shows weak association** with sales volume (oil affects cost, not demand directly).
5. **USD/TRY raw correlation is spurious** — both series trend upward; after first-differencing, the relationship is much weaker.

## Next Steps

- Feature engineering: lagged temperature variables, rolling averages, season indicators, time-trend index.
- Apply multiple ML models (Linear Regression, Ridge, Random Forest, XGBoost) with time-series cross-validation.
- Compare performance and interpret feature importance.

## AI Tool Disclosure

See [AI_USAGE.md](AI_USAGE.md) for detailed disclosure of how AI tools were used in this project, in accordance with course policy.
