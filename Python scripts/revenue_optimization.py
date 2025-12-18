"""
PART 3: Revenue Optimization and Scenario Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("PART 3: REVENUE OPTIMIZATION & SCENARIO ANALYSIS")
print("="*70)

# Load data
df = pd.read_csv('processed_permit_data.csv', index_col=0, parse_dates=True)

# Current prices (USD)
current_prices = {
    'Foreign_NonResident': 800,
    'Foreign_Resident': 700,
    'Rest_of_Africa': 500,
    'East_African': 100
}

# Segment elasticities
elasticities = {
    'Foreign_NonResident': -0.3,
    'Foreign_Resident': -0.6,
    'Rest_of_Africa': -1.2,
    'East_African': -1.8
}

segments = list(current_prices.keys())

# ============================================================================
# 3.1 BASELINE REVENUE CALCULATION
# ============================================================================
print("\n[3.1] BASELINE REVENUE (Current Pricing)...")

# Calculate current revenue
for segment in segments:
    df[f'{segment}_Revenue'] = df[segment] * current_prices[segment]

df['Total_Revenue'] = sum(df[f'{segment}_Revenue'] for segment in segments)

baseline_revenue_monthly = df['Total_Revenue'].mean()
baseline_revenue_annual = df['Total_Revenue'].sum() / 5  # Average per year

print(f"✓ Current Average Monthly Revenue: ${baseline_revenue_monthly:,.0f}")
print(f"✓ Current Average Annual Revenue: ${baseline_revenue_annual:,.0f}")

# ============================================================================
# 3.2 OPTIMIZED PRICING SCENARIOS
# ============================================================================
print("\n[3.2] DEVELOPING OPTIMIZED PRICING SCENARIOS...")

# Define peak and off-peak months
peak_months = [6, 7, 8, 9, 12, 1, 2]
df['Season_Type'] = df['Month'].apply(lambda x: 'Peak' if x in peak_months else 'Off-Peak')

# SCENARIO 1: Current Pricing (Baseline)
scenario1 = {
    'name': 'Current Pricing',
    'peak_multiplier': {seg: 1.0 for seg in segments},
    'offpeak_multiplier': {seg: 1.0 for seg in segments}
}

# SCENARIO 2: Moderate Dynamic Pricing
scenario2 = {
    'name': 'Moderate Dynamic Pricing',
    'peak_multiplier': {
        'Foreign_NonResident': 1.30,  # +30% in peak
        'Foreign_Resident': 1.20,      # +20%
        'Rest_of_Africa': 1.10,        # +10%
        'East_African': 1.0            # No change (equity)
    },
    'offpeak_multiplier': {
        'Foreign_NonResident': 0.85,   # -15% discount
        'Foreign_Resident': 0.80,      # -20%
        'Rest_of_Africa': 0.75,        # -25%
        'East_African': 0.70           # -30% (stimulate demand)
    }
}

# SCENARIO 3: Aggressive Revenue Maximization
scenario3 = {
    'name': 'Aggressive Pricing',
    'peak_multiplier': {
        'Foreign_NonResident': 1.50,   # Rwanda-level pricing
        'Foreign_Resident': 1.35,
        'Rest_of_Africa': 1.20,
        'East_African': 1.0
    },
    'offpeak_multiplier': {
        'Foreign_NonResident': 0.90,
        'Foreign_Resident': 0.85,
        'Rest_of_Africa': 0.70,
        'East_African': 0.60
    }
}

scenarios = [scenario1, scenario2, scenario3]

# ============================================================================
# 3.3 CALCULATE REVENUE FOR EACH SCENARIO
# ============================================================================
print("\n[3.3] SIMULATING SCENARIOS...")

results = []

for scenario in scenarios:
    print(f"\n  Processing: {scenario['name']}")
    
    # Create new dataframe for this scenario
    df_scenario = df.copy()
    
    total_revenue = 0
    
    for segment in segments:
        # Calculate new prices
        df_scenario[f'{segment}_Price'] = df_scenario.apply(
            lambda row: current_prices[segment] * (
                scenario['peak_multiplier'][segment] if row['Season_Type'] == 'Peak' 
                else scenario['offpeak_multiplier'][segment]
            ), axis=1
        )
        
        # Calculate demand change based on elasticity
        price_change_pct = (df_scenario[f'{segment}_Price'] / current_prices[segment]) - 1
        demand_change_pct = price_change_pct * elasticities[segment]
        
        # New demand
        df_scenario[f'{segment}_New'] = df_scenario[segment] * (1 + demand_change_pct)
        df_scenario[f'{segment}_New'] = df_scenario[f'{segment}_New'].clip(lower=0)  # No negative demand
        
        # Revenue
        df_scenario[f'{segment}_Rev'] = df_scenario[f'{segment}_New'] * df_scenario[f'{segment}_Price']
        total_revenue += df_scenario[f'{segment}_Rev'].sum()
    
    df_scenario['Total_Revenue_New'] = sum(df_scenario[f'{segment}_Rev'] for segment in segments)
    
    # Calculate metrics
    annual_revenue = df_scenario['Total_Revenue_New'].sum() / 5
    monthly_revenue = df_scenario['Total_Revenue_New'].mean()
    total_permits = sum(df_scenario[f'{segment}_New'].sum() for segment in segments)
    
    results.append({
        'Scenario': scenario['name'],
        'Annual_Revenue': annual_revenue,
        'Monthly_Revenue': monthly_revenue,
        'Total_Permits_5yr': total_permits,
        'Revenue_vs_Baseline': ((annual_revenue / baseline_revenue_annual) - 1) * 100,
        'DataFrame': df_scenario
    })

# Create comparison DataFrame
comparison = pd.DataFrame(results)[['Scenario', 'Annual_Revenue', 'Monthly_Revenue', 'Total_Permits_5yr', 'Revenue_vs_Baseline']]
print("\n" + "="*70)
print("SCENARIO COMPARISON RESULTS")
print("="*70)
print(comparison.to_string(index=False))

# ============================================================================
# 3.4 VISUALIZE RESULTS
# ============================================================================
print("\n[3.4] CREATING VISUALIZATIONS...")

# Revenue comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Annual revenue comparison
axes[0,0].bar(comparison['Scenario'], comparison['Annual_Revenue']/1000000, 
             color=['#2E86AB', '#F18F01', '#E63946'], alpha=0.8, edgecolor='black', linewidth=2)
axes[0,0].set_title('Annual Revenue by Scenario', fontsize=13, fontweight='bold')
axes[0,0].set_ylabel('Revenue (Million USD)')
axes[0,0].set_xlabel('Scenario')
axes[0,0].grid(True, alpha=0.3, axis='y')
for i, row in comparison.iterrows():
    axes[0,0].text(i, row['Annual_Revenue']/1000000 + 0.3, 
                  f"${row['Annual_Revenue']/1000000:.2f}M", 
                  ha='center', fontsize=11, fontweight='bold')

# Revenue increase %
axes[0,1].bar(comparison['Scenario'], comparison['Revenue_vs_Baseline'], 
             color=['#2E86AB', '#F18F01', '#E63946'], alpha=0.8, edgecolor='black', linewidth=2)
axes[0,1].axhline(0, color='black', linestyle='-', linewidth=1)
axes[0,1].set_title('Revenue Increase vs. Baseline', fontsize=13, fontweight='bold')
axes[0,1].set_ylabel('% Increase')
axes[0,1].set_xlabel('Scenario')
axes[0,1].grid(True, alpha=0.3, axis='y')
for i, row in comparison.iterrows():
    axes[0,1].text(i, row['Revenue_vs_Baseline'] + 2, 
                  f"+{row['Revenue_vs_Baseline']:.1f}%", 
                  ha='center', fontsize=11, fontweight='bold')

# Monthly revenue trend (Scenario 2)
df_scenario2 = results[1]['DataFrame']
axes[1,0].plot(df_scenario2.index, df_scenario2['Total_Revenue_New']/1000, 
              linewidth=2, color='#F18F01', label='Optimized')
axes[1,0].plot(df.index, df['Total_Revenue']/1000, 
              linewidth=2, color='#2E86AB', alpha=0.6, label='Current')
axes[1,0].set_title('Monthly Revenue: Current vs. Optimized', fontsize=13, fontweight='bold')
axes[1,0].set_ylabel('Revenue (Thousand USD)')
axes[1,0].set_xlabel('Date')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Peak vs Off-Peak pricing (Scenario 2)
peak_prices = [current_prices[seg] * scenario2['peak_multiplier'][seg] for seg in segments]
offpeak_prices = [current_prices[seg] * scenario2['offpeak_multiplier'][seg] for seg in segments]
x = np.arange(len(segments))
width = 0.35

bars1 = axes[1,1].bar(x - width/2, [current_prices[seg] for seg in segments], width, 
                     label='Current', color='#2E86AB', alpha=0.8, edgecolor='black')
bars2 = axes[1,1].bar(x + width/2, peak_prices, width, 
                     label='Peak (Optimized)', color='#E63946', alpha=0.8, edgecolor='black')

axes[1,1].set_title('Optimized Peak Season Pricing', fontsize=13, fontweight='bold')
axes[1,1].set_ylabel('Price (USD)')
axes[1,1].set_xlabel('Visitor Segment')
axes[1,1].set_xticks(x)
axes[1,1].set_xticklabels([s.replace('_', '\n') for s in segments], fontsize=9)
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('08_revenue_optimization.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 08_revenue_optimization.png")
plt.close()

# ============================================================================
# 3.5 DETAILED PRICING RECOMMENDATIONS
# ============================================================================
print("\n[3.5] GENERATING PRICING RECOMMENDATIONS...")

recommendations = []
for segment in segments:
    rec = {
        'Segment': segment.replace('_', ' '),
        'Current_Price': current_prices[segment],
        'Peak_Price': current_prices[segment] * scenario2['peak_multiplier'][segment],
        'OffPeak_Price': current_prices[segment] * scenario2['offpeak_multiplier'][segment],
        'Peak_Change': (scenario2['peak_multiplier'][segment] - 1) * 100,
        'OffPeak_Change': (scenario2['offpeak_multiplier'][segment] - 1) * 100
    }
    recommendations.append(rec)

recommendations_df = pd.DataFrame(recommendations)
print("\nRECOMMENDED PRICING STRUCTURE:")
print(recommendations_df.to_string(index=False))

# Save results
recommendations_df.to_csv('pricing_recommendations.csv', index=False)
comparison.to_csv('scenario_comparison.csv', index=False)

# ============================================================================
# 3.6 WRITE COMPREHENSIVE SUMMARY
# ============================================================================
with open('optimization_results.txt', 'w') as f:
    f.write("="*70 + "\n")
    f.write("REVENUE OPTIMIZATION RESULTS\n")
    f.write("="*70 + "\n\n")
    
    f.write("BASELINE (CURRENT PRICING)\n")
    f.write("-"*70 + "\n")
    f.write(f"Average Annual Revenue:  ${baseline_revenue_annual:,.0f}\n")
    f.write(f"Average Monthly Revenue: ${baseline_revenue_monthly:,.0f}\n\n")
    
    f.write("SCENARIO COMPARISON\n")
    f.write("-"*70 + "\n")
    f.write(comparison.to_string(index=False))
    f.write("\n\n")
    
    f.write("RECOMMENDED PRICING STRATEGY (Moderate Dynamic Pricing)\n")
    f.write("-"*70 + "\n")
    f.write(recommendations_df.to_string(index=False))
    f.write("\n\n")
    
    f.write("KEY BENEFITS\n")
    f.write("-"*70 + "\n")
    revenue_increase = results[1]['Annual_Revenue'] - baseline_revenue_annual
    f.write(f"• Additional Annual Revenue: ${revenue_increase:,.0f} (+{comparison.iloc[1]['Revenue_vs_Baseline']:.1f}%)\n")
    f.write(f"• Conservation funding increase: ${revenue_increase * 0.7:,.0f} (assuming 70% allocation)\n")
    f.write("• Smoothed seasonal demand distribution\n")
    f.write("• Maintained affordability for East African citizens\n")
    f.write("• Capitalized on inelastic foreign demand during peak seasons\n")
    f.write("• Stimulated off-peak tourism through strategic discounts\n")

print("✓ Saved: optimization_results.txt")
print("✓ Saved: pricing_recommendations.csv")
print("✓ Saved: scenario_comparison.csv")

print("\n" + "="*70)
print("OPTIMIZATION ANALYSIS COMPLETE")
print("="*70)
print(f"\nRECOMMENDED STRATEGY: Moderate Dynamic Pricing")
print(f"Projected Revenue Increase: +{comparison.iloc[1]['Revenue_vs_Baseline']:.1f}%")
print(f"Additional Annual Funding: ${results[1]['Annual_Revenue'] - baseline_revenue_annual:,.0f}")
