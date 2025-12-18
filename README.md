# Gorilla Trekking Permit Pricing Optimization

**A Data-Driven Approach to Enhance Conservation Funding in Uganda**

## Project Overview

This project develops an optimized pricing strategy for Uganda's gorilla-trekking permits using time-series forecasting, econometric analysis, and revenue optimization techniques. The analysis demonstrates that moderate dynamic pricing can increase annual conservation revenue by $325,225 (+5.0%) while maintaining social equity and smoothing seasonal demand.

## Key Findings

- **Revenue Increase:** +$325,225 annually (+5.0%) with moderate dynamic pricing
- **Conservation Funding:** +$227,658 additional funding (70% revenue allocation)
- **Demand Smoothing:** Peak utilization reduced 73%→71%, off-peak increased 64%→68%
- **Equity Preserved:** East African pricing protected, off-peak discounts enhanced
- **Statistical Confidence:** 95% bootstrap CI [$298K, $351K], 99.7% probability of positive impact

## Methodology

### 1. Data Collection
- **Source:** Uganda Bureau of Statistics (UBOS) National Parks data 2019-2023
- **Coverage:** 60 months, 48,611 estimated gorilla permits
- **Validation:** Cross-referenced with UWA capacity constraints and revenue benchmarks

### 2. Analytical Approach
- **SARIMA Forecasting:** ARIMA(1,1,1)×(1,1,1)₁₂ model for 12-month demand projection (MAPE: 11.3%)
- **Price Elasticity:** Log-linear regression on cross-country data, segment-specific estimation
- **Revenue Optimization:** Constrained optimization across 4 visitor segments and 2 seasons

### 3. Market Segmentation
- Foreign Non-Resident: 65% (elasticity: -0.30)
- Foreign Resident: 10% (elasticity: -0.60)
- Rest of Africa: 15% (elasticity: -1.20)
- East African Citizens: 10% (elasticity: -1.80)

## Repository Structure

```
├── gorilla_pricing_analysis.py       # Data preprocessing and segmentation
├── eda_and_modeling.py                # Exploratory analysis and visualizations
├── forecasting_elasticity.py          # SARIMA forecasting and elasticity estimation
├── revenue_optimization.py            # Pricing scenario optimization
├── run_complete_analysis.py           # Master execution script
├── convert_reports_to_word.py         # Report generation utility
└── README.md                          # This file
```

## Requirements

### Python Version
- Python 3.10 or higher

### Dependencies
```bash
pip install pandas numpy matplotlib seaborn statsmodels scikit-learn python-docx openpyxl
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## How to Reproduce Results

### 1. Data Preparation
Place the following UBOS data files in `Research data/` folder:
- `National_Parks_Visitors_2019-2023.xlsx`
- `Monthly_Tourism_Arrivals_2023.xlsx`
- `Visitor_Arrivals_2019-2023.xlsx`
- `UWA_Tariff_2024-2026.pdf`

### 2. Run Complete Analysis
```bash
python run_complete_analysis.py
```

This will execute all analysis steps:
1. Data preprocessing and permit estimation
2. Exploratory data analysis with 5 visualizations
3. SARIMA forecasting and elasticity estimation
4. Revenue optimization across 3 scenarios
5. Generate all reports and outputs

### 3. Outputs Generated

**Data Files** (saved to `Data files/`):
- `processed_permit_data.csv` - 60-month time series with market segments
- `demand_forecast_2024.csv` - 12-month SARIMA projections
- `pricing_recommendations.csv` - Recommended pricing structure
- `scenario_comparison.csv` - Revenue comparison across scenarios

**Visualizations** (saved to `Data visualization/`):
- `01_time_series_analysis.png` - Overall trend with COVID impact
- `02_seasonal_decomposition.png` - Trend/seasonal/residual components
- `03_correlation_matrix.png` - Segment correlation heatmap
- `04_distribution_analysis.png` - Distribution by segment
- `05_peak_offpeak_comparison.png` - Seasonal demand comparison
- `06_sarima_forecast.png` - 12-month projection with confidence bands
- `07_price_elasticity.png` - Cross-country and segment elasticities
- `08_revenue_optimization.png` - Scenario comparison charts

**Reports** (saved to `Reports/`):
- `eda_summary.txt` - Statistical summaries and key findings
- `elasticity_results.txt` - Elasticity estimates and interpretations
- `optimization_results.txt` - Scenario comparisons and recommendations
- `EXECUTIVE_SUMMARY.txt` - Stakeholder-focused overview

## Individual Script Usage

### Data Preprocessing
```bash
python gorilla_pricing_analysis.py
```
Outputs: `processed_permit_data.csv`

### Exploratory Data Analysis
```bash
python eda_and_modeling.py
```
Outputs: 5 visualizations + `eda_summary.txt`

### Forecasting & Elasticity
```bash
python forecasting_elasticity.py
```
Outputs: 2 visualizations + `elasticity_results.txt` + `demand_forecast_2024.csv`

### Revenue Optimization
```bash
python revenue_optimization.py
```
Outputs: 1 visualization + `optimization_results.txt` + pricing CSVs

## Key Results

### Recommended Pricing Strategy

| Segment | Current | Peak (Recommended) | Off-Peak (Recommended) |
|---------|---------|-------------------|----------------------|
| Foreign Non-Resident | $800 | $1,040 (+30%) | $680 (-15%) |
| Foreign Resident | $700 | $840 (+20%) | $560 (-20%) |
| Rest of Africa | $500 | $550 (+10%) | $375 (-25%) |
| East African | $100 | $100 (0%) | $70 (-30%) |

### Scenario Comparison

| Scenario | Annual Revenue | Change | Conservation Funding |
|----------|---------------|---------|---------------------|
| Current Baseline | $6,550,780 | - | $4,585,546 |
| Moderate Dynamic | $6,876,005 | +$325,225 (+5.0%) | $4,813,204 |
| Aggressive Dynamic | $7,215,754 | +$664,974 (+10.2%) | $5,051,028 |

**Recommendation:** Moderate Dynamic Pricing balances revenue optimization with demand stability and equity considerations.

## Data Sources

### Primary Data
- **Uganda Bureau of Statistics (UBOS):** [www.ubos.org](https://www.ubos.org)
  - National Parks Visitors Statistics 2019-2023
  - Monthly Tourism Arrivals 2023
  - Visitor Arrivals and Departures 2019-2023

- **Uganda Wildlife Authority (UWA):** [ugandawildlife.org](https://www.ugandawildlife.org)
  - Conservation Tariff 2024-2026

### Regional Comparative Data
- Rwanda Development Board: Gorilla permit pricing ($1,500)
- Democratic Republic of Congo: Virunga National Park pricing ($400)

## Methodology References

- **Time Series:** Box, G.E.P. and Jenkins, G.M. (1976) *Time Series Analysis: Forecasting and Control*
- **Revenue Management:** Talluri, K.T. and van Ryzin, G.J. (2004) *The Theory and Practice of Revenue Management*
- **Conservation Economics:** Moyini, Y. and Uwimbabazi, B. (2003) *Analysis of the Economic Significance of Gorilla Tourism in Uganda*

## Project Context

This analysis was conducted as part of the MSc in IT for Business Data Analytics programme. The project demonstrates:
- Advanced data preprocessing and validation techniques
- Time-series forecasting with SARIMA models
- Econometric analysis for price elasticity estimation
- Constrained optimization for multi-segment revenue maximization
- Business insights aligned with conservation and equity objectives

## Limitations and Future Work

### Current Limitations
1. Estimation-based approach (no direct UWA permit sales data)
2. Cross-country elasticity extrapolation
3. Assumes constant elasticity within analysis period
4. No booking lead time data

### Future Research Recommendations
1. Validate with actual UWA permit booking data
2. Conduct willingness-to-pay surveys for segment-specific elasticities
3. Implement pilot A/B testing for selected visitor segments
4. Develop dynamic booking platform with real-time demand signals
5. Expand to multi-year capacity planning (gorilla habituation cycles)
6. Integrate environmental impact metrics (carbon footprint, habituation stress)

## Contact & Citation

**Author:** Business Data Analytics MSc Student  
**Institution:** International Business School  
**Date:** December 2025

For questions or collaboration opportunities regarding this analysis, please contact through appropriate academic channels.

## License

This project is submitted as academic work for the MSc in IT for Business Data Analytics programme. Data sources are publicly available from UBOS and UWA. Code is provided for reproducibility and educational purposes.

---

**Note:** This analysis uses real UBOS aggregate data combined with literature-based estimation for gorilla-specific patterns. Results should be validated with UWA's internal permit sales data before full implementation.
