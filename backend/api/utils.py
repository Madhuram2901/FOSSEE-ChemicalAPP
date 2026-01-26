"""
Analytics utilities for CSV processing
"""
import pandas as pd

REQUIRED_COLUMNS = {"Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"}


def analyze_csv(file_path):
    """
    Analyze a CSV file and return summary statistics
    """
    df = pd.read_csv(file_path)

    if not REQUIRED_COLUMNS.issubset(set(df.columns)):
        missing = REQUIRED_COLUMNS - set(df.columns)
        raise ValueError(f"Missing columns: {missing}")

    summary = {
        "total_equipment": len(df),
        "averages": {
            "flowrate": round(df["Flowrate"].mean(), 2),
            "pressure": round(df["Pressure"].mean(), 2),
            "temperature": round(df["Temperature"].mean(), 2),
        },
        "type_distribution": df["Type"].value_counts().to_dict(),
        "table": df.to_dict(orient="records"),
    }

    return summary
