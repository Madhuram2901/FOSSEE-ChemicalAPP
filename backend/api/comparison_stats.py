"""
Statistical Comparison Logic for Datasets
"""
import pandas as pd
import numpy as np

def calculate_comparison_stats(dataset_a, dataset_b):
    """
    Calculate statistical comparison metrics between two datasets.
    """
    try:
        df_a = pd.read_csv(dataset_a.file.path)
        df_b = pd.read_csv(dataset_b.file.path)
    except Exception as e:
        # Fallback if files missing (though unlikely in prod)
        return {}

    metrics = ['Flowrate', 'Pressure', 'Temperature']
    stats = {}

    for metric in metrics:
        key = metric.lower()
        
        # Extract series
        series_a = df_a[metric].dropna()
        series_b = df_b[metric].dropna()
        
        # 1. Basic stats
        mean_a = series_a.mean()
        mean_b = series_b.mean()
        std_a = series_a.std()
        std_b = series_b.std()
        
        # 2. Percentage Change
        percent_change = ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0
        
        # 3. Stability (Variability)
        # Using 20% increase in std dev as threshold for instability
        stability = "stable" if std_b <= (std_a * 1.2) else "unstable"
        
        # 4. Effect Size (Cohen's d)
        pooled_std = np.sqrt((std_a**2 + std_b**2) / 2)
        if pooled_std == 0:
            effect_size_val = 0
        else:
            effect_size_val = (mean_b - mean_a) / pooled_std
            
        abs_d = abs(effect_size_val)
        if abs_d < 0.2:
            effect_label = "trivial"
        elif abs_d < 0.5:
            effect_label = "small"
        elif abs_d < 0.8:
            effect_label = "medium"
        else:
            effect_label = "large"
            
        # 5. Risk Indicators
        risk_level = "normal"
        # Flowrate: Warning > 20%, Critical > 40% change
        if key == 'flowrate':
            abs_change = abs(percent_change)
            if abs_change > 40:
                risk_level = "critical"
            elif abs_change > 20:
                risk_level = "warning"
                
        # Pressure: Critical > 50, Warning > 40 (Absolute Value Check)
        elif key == 'pressure':
            if mean_b > 50:
                risk_level = "critical"
            elif mean_b > 40:
                risk_level = "warning"
                
        # Temperature: Critical > 600, Warning > 500 (Absolute Value Check)
        elif key == 'temperature':
            if mean_b > 600:
                risk_level = "critical"
            elif mean_b > 500:
                risk_level = "warning"

        stats[key] = {
            "percent_change": round(percent_change, 2),
            "std_dev_a": round(std_a, 2),
            "std_dev_b": round(std_b, 2),
            "stability": stability,
            "effect_size": effect_label,
            "risk_level": risk_level
        }
        
    return stats
