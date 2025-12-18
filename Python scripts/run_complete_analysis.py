"""
MASTER ANALYSIS SCRIPT
Runs complete gorilla permit pricing analysis
"""

import subprocess
import sys

scripts = [
    ('gorilla_pricing_analysis.py', 'Data Loading & Preparation'),
    ('eda_and_modeling.py', 'Exploratory Data Analysis'),
    ('forecasting_elasticity.py', 'Forecasting & Elasticity'),
    ('revenue_optimization.py', 'Revenue Optimization')
]

print("="*70)
print("GORILLA PERMIT PRICING OPTIMIZATION - COMPLETE ANALYSIS")
print("="*70)

for i, (script, description) in enumerate(scripts, 1):
    print(f"\n[{i}/{len(scripts)}] Running: {description}")
    print("-"*70)
    
    try:
        result = subprocess.run([sys.executable, script], 
                              capture_output=False, 
                              text=True, 
                              check=True)
        print(f"✓ {description} completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {script}: {e}")
        continue
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        continue

print("\n" + "="*70)
print("COMPLETE ANALYSIS FINISHED")
print("="*70)
print("\nGenerated Files:")
print("  Data: processed_permit_data.csv, demand_forecast_2024.csv")
print("  Visualizations: 01-08_*.png (8 figures)")
print("  Results: eda_summary.txt, elasticity_results.txt, optimization_results.txt")
print("  Recommendations: pricing_recommendations.csv, scenario_comparison.csv")
