"""
Comparison Logic for Datasets
"""

from .comparison_stats import calculate_comparison_stats

def compare_datasets(dataset_a, dataset_b):
    """
    Compare two datasets and return the structure with delta.
    Does NOT recalculate basics, just computes differences based on stored summary.
    """
    summary_a = dataset_a.summary
    summary_b = dataset_b.summary

    # Calculate Deltas (B - A)
    # 1. Total Equipment
    delta_total = summary_b.get('total_equipment', 0) - summary_a.get('total_equipment', 0)

    # 2. Averages
    avg_a = summary_a.get('averages', {})
    avg_b = summary_b.get('averages', {})

    delta_avgs = {
        'flowrate': round(avg_b.get('flowrate', 0) - avg_a.get('flowrate', 0), 2),
        'pressure': round(avg_b.get('pressure', 0) - avg_a.get('pressure', 0), 2),
        'temperature': round(avg_b.get('temperature', 0) - avg_a.get('temperature', 0), 2),
    }

    # 3. Advanced Stats
    stats = calculate_comparison_stats(dataset_a, dataset_b)

    result = {
        "dataset_a": {
            "id": dataset_a.id,
            "filename": dataset_a.original_filename,
            "summary": summary_a
        },
        "dataset_b": {
            "id": dataset_b.id,
            "filename": dataset_b.original_filename,
            "summary": summary_b
        },
        "delta": {
            "total_equipment": delta_total,
            "averages": delta_avgs
        },
        "comparison_stats": stats
    }
    
    return result
