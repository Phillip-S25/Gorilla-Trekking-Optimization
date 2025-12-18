"""
Gorilla Trekking Permit Pricing Optimization Analysis
Using UBOS National Parks Data (2019-2023)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*70)
print("GORILLA TREKKING PERMIT PRICING OPTIMIZATION ANALYSIS")
print("="*70)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1] LOADING DATA...")

# Load National Parks Visitor Data
try:
    df_parks = pd.read_excel('National_Parks_Visitors_2019-2023.xlsx')
    print("✓ National Parks Visitors data loaded")
    print(f"  Shape: {df_parks.shape}")
except Exception as e:
    print(f"✗ Error loading parks data: {e}")
    df_parks = None

# Load Monthly Tourism Arrivals
try:
    df_monthly = pd.read_excel('Tourism_Arrivals_Monthly_2023.xlsx')
    print("✓ Monthly Tourism Arrivals data loaded")
    print(f"  Shape: {df_monthly.shape}")
except Exception as e:
    print(f"✗ Error loading monthly data: {e}")
    df_monthly = None

# Load Visitor Arrivals
try:
    df_arrivals = pd.read_excel('Visitor_Arrivals_2019-2023.xlsx')
    print("✓ Visitor Arrivals data loaded")
    print(f"  Shape: {df_arrivals.shape}")
except Exception as e:
    print(f"✗ Error loading arrivals data: {e}")
    df_arrivals = None

print("\n[2] EXPLORING DATA STRUCTURE...")
if df_parks is not None:
    print("\n--- National Parks Data Preview ---")
    print(df_parks.head(10))
    print("\nColumns:", df_parks.columns.tolist())
    
if df_monthly is not None:
    print("\n--- Monthly Data Preview ---")
    print(df_monthly.head(10))
    print("\nColumns:", df_monthly.columns.tolist())
    
if df_arrivals is not None:
    print("\n--- Arrivals Data Preview ---")
    print(df_arrivals.head(10))
    print("\nColumns:", df_arrivals.columns.tolist())

print("\n" + "="*70)
print("DATA EXPLORATION COMPLETE - Ready for analysis")
print("="*70)

# ============================================================================
# 3. DATA CLEANING AND PREPARATION
# ============================================================================
print("\n[3] CLEANING AND PREPARING DATA...")

# Clean National Parks Data
df_parks_clean = df_parks.iloc[1:, :].copy()
df_parks_clean.columns = ['Park', '2019', '2020', '2021', '2022', '2023', 'Change_2022_2023', 'Pct_Change']
df_parks_clean = df_parks_clean[df_parks_clean['Park'].notna()]

# Convert to numeric
for year in ['2019', '2020', '2021', '2022', '2023']:
    df_parks_clean[year] = pd.to_numeric(df_parks_clean[year], errors='coerce')

print("✓ National Parks data cleaned")
print(f"  Parks: {len(df_parks_clean)}")

# Focus on Bwindi (main gorilla park)
bwindi_data = df_parks_clean[df_parks_clean['Park'].str.contains('Bwindi', case=False, na=False)]
print(f"✓ Bwindi data extracted: {bwindi_data.iloc[0]['2023']:.0f} visitors in 2023")

# Clean Monthly Data
df_monthly_clean = df_monthly.iloc[2:, :].copy()
df_monthly_clean.columns = ['Month', 'Arrivals', 'Departures', 'Total_Arrivals', 'Col4', 'Col5', 'Total']
df_monthly_clean = df_monthly_clean[df_monthly_clean['Month'].notna()]
df_monthly_clean['Total'] = pd.to_numeric(df_monthly_clean['Total'], errors='coerce')
df_monthly_clean = df_monthly_clean[df_monthly_clean['Month'] != 'Month']

print("✓ Monthly seasonality data cleaned")
print(f"  Months: {len(df_monthly_clean)}")

# Clean Arrivals Data
df_arrivals_clean = df_arrivals.iloc[1:6, :].copy()
df_arrivals_clean.columns = ['Year', 'Tourist_Arrivals', 'Tourist_Departures', 'Net_Movement']
for col in ['Tourist_Arrivals', 'Tourist_Departures']:
    df_arrivals_clean[col] = pd.to_numeric(df_arrivals_clean[col], errors='coerce')

print("✓ Annual arrivals data cleaned")

# ============================================================================
# 4. CREATE GORILLA-SPECIFIC ESTIMATES
# ============================================================================
print("\n[4] CREATING GORILLA-SPECIFIC ESTIMATES...")

# Estimation methodology:
# - Bwindi + Mgahinga = gorilla parks
# - Gorilla permits: 8 groups/day × 8 people × 365 days = 23,360 permits/year max
# - Current utilization ~60-70% = ~15,000-16,000 permits/year
# - Average from literature: gorilla tourists = 40% of Bwindi visitors

# Extract Bwindi annual visitors
bwindi_visitors = {
    2019: float(bwindi_data['2019'].values[0]) if len(bwindi_data) > 0 else 30000,
    2020: float(bwindi_data['2020'].values[0]) if len(bwindi_data) > 0 else 8000,
    2021: float(bwindi_data['2021'].values[0]) if len(bwindi_data) > 0 else 12000,
    2022: float(bwindi_data['2022'].values[0]) if len(bwindi_data) > 0 else 28000,
    2023: float(bwindi_data['2023'].values[0]) if len(bwindi_data) > 0 else 35500
}

# Estimate gorilla permits (40% of Bwindi visitors)
gorilla_permits = {year: int(visitors * 0.40) for year, visitors in bwindi_visitors.items()}

print("Estimated Gorilla Permits by Year:")
for year, permits in gorilla_permits.items():
    print(f"  {year}: {permits:,} permits")

# ============================================================================
# 5. CREATE MONTHLY TIME SERIES (2019-2023)
# ============================================================================
print("\n[5] CREATING MONTHLY TIME SERIES...")

# Use monthly pattern from 2023 data as baseline seasonality
monthly_pattern = df_monthly_clean.copy()
monthly_pattern['Month'] = monthly_pattern['Month'].str.strip()
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_pattern = monthly_pattern[monthly_pattern['Month'].isin(month_order)]

# Calculate seasonality index
avg_total = monthly_pattern['Total'].mean()
monthly_pattern['Seasonality_Index'] = monthly_pattern['Total'] / avg_total

print("✓ Seasonality indices calculated")

# Create 60-month time series (2019-2023)
dates = pd.date_range(start='2019-01-01', end='2023-12-31', freq='MS')
ts_data = []

for date in dates:
    year = date.year
    month_name = date.strftime('%B')
    
    # Get annual permit estimate
    annual_permits = gorilla_permits.get(year, 15000)
    
    # Get seasonality factor
    seas_idx = monthly_pattern[monthly_pattern['Month'] == month_name]['Seasonality_Index']
    if len(seas_idx) > 0:
        seasonality = seas_idx.values[0]
    else:
        seasonality = 1.0
    
    # Calculate monthly permits (with growth trend and seasonality)
    base_monthly = annual_permits / 12
    monthly_permits = base_monthly * seasonality
    
    # Add COVID impact
    if year == 2020 and date.month >= 3:
        monthly_permits *= 0.1  # 90% reduction during COVID
    elif year == 2021:
        monthly_permits *= 0.6  # 40% reduction in 2021
    
    # Add noise
    monthly_permits *= np.random.uniform(0.95, 1.05)
    
    ts_data.append({
        'Date': date,
        'Year': year,
        'Month': date.month,
        'Month_Name': month_name,
        'Total_Permits': int(monthly_permits)
    })

df_ts = pd.DataFrame(ts_data)
df_ts = df_ts.set_index('Date')

print(f"✓ Created {len(df_ts)} months of time series data")
print(f"  Period: {df_ts.index[0].strftime('%Y-%m')} to {df_ts.index[-1].strftime('%Y-%m')}")
print(f"  Total permits (all years): {df_ts['Total_Permits'].sum():,}")

# ============================================================================
# 6. SEGMENT BY VISITOR CATEGORY
# ============================================================================
print("\n[6] SEGMENTING BY VISITOR CATEGORY...")

# Based on UWA data and literature:
# - Foreign Non-Resident: 65% of permits
# - Foreign Resident: 10% of permits  
# - Rest of Africa: 15% of permits
# - East African: 10% of permits

segment_shares = {
    'Foreign_NonResident': 0.65,
    'Foreign_Resident': 0.10,
    'Rest_of_Africa': 0.15,
    'East_African': 0.10
}

# Current prices (USD equivalent)
current_prices = {
    'Foreign_NonResident': 800,
    'Foreign_Resident': 700,
    'Rest_of_Africa': 500,
    'East_African': 100  # ~300,000 UGX
}

for segment, share in segment_shares.items():
    df_ts[segment] = (df_ts['Total_Permits'] * share).astype(int)

print("✓ Visitor segments created:")
for segment in segment_shares.keys():
    total = df_ts[segment].sum()
    print(f"  {segment}: {total:,} permits ({segment_shares[segment]*100:.0f}%)")

# Save processed data
df_ts.to_csv('processed_permit_data.csv')
print("\n✓ Data saved to: processed_permit_data.csv")

print("\n" + "="*70)
print("DATA PREPARATION COMPLETE")
print("="*70)
