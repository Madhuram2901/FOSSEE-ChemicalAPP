import pandas as pd
from django.core.exceptions import ValidationError

REQUIRED_COLUMNS = {"Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"}
MAX_FILE_SIZE_MB = 10
MAX_ROWS = 20000

def validate_csv_file(file):
    """
    Validates the CSV file for:
    - Size
    - Extension
    - Required Columns
    - Data Types
    """
    # 1. File size validation
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File too large. Max size is {MAX_FILE_SIZE_MB}MB.")

    # 2. Extension validation
    if not file.name.endswith('.csv'):
        raise ValidationError("Invalid file format. Only CSV allowed.")

    # 3. Content Validation
    try:
        # We read the file into pandas to check structure
        # Note: chunks could be used for large files to avoid memory issues,
        # but for validation we need to check columns.
        df = pd.read_csv(file)
        
        if df.empty:
            raise ValidationError("CSV file is empty.")

        # Check row count
        if len(df) > MAX_ROWS:
             raise ValidationError(f"File contains {len(df)} rows. Maximum allowed is {MAX_ROWS}.")

        # Check columns
        if not REQUIRED_COLUMNS.issubset(set(df.columns)):
            missing = REQUIRED_COLUMNS - set(df.columns)
            raise ValidationError(f"Missing required columns: {', '.join(missing)}")

        # Check numeric types
        numeric_cols = ["Flowrate", "Pressure", "Temperature"]
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                # Attempt to convert to see if it's coercion-safe
                try:
                    pd.to_numeric(df[col])
                except Exception:
                    raise ValidationError(f"Column '{col}' must contain numeric data.")

    except pd.errors.EmptyDataError:
        raise ValidationError("CSV file is empty or invalid.")
    except pd.errors.ParserError:
        raise ValidationError("Failed to parse CSV file.")
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        raise ValidationError(f"Invalid CSV content: {str(e)}")
    finally:
        # IMPORTANT: Reset file pointer so it can be read again later
        file.seek(0)
