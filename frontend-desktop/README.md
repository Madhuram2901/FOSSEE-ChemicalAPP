# Chemical Equipment Visualizer - Desktop Application

PyQt5 desktop client for the Chemical Equipment Parameter Visualizer system.

## Overview

This desktop application provides the same functionality as the web dashboard, allowing users to:
- Upload CSV files containing equipment data
- View summary statistics (total equipment, average flowrate, pressure, temperature)
- Visualize data through interactive charts (bar chart for averages, pie chart for type distribution)
- Browse equipment data in a sortable table
- Access dataset history and switch between datasets

## Features

### ✅ Implemented Features

1. **CSV Upload**
   - Local file picker with CSV validation
   - Upload to backend API
   - Real-time status feedback
   - Error handling with clear messages

2. **Dataset History**
   - Automatic loading on app start
   - List view of recent uploads (last 5)
   - Click to switch between datasets
   - Refresh button to reload history

3. **Summary Cards**
   - Total Equipment Count
   - Average Flowrate (m³/h)
   - Average Pressure (bar)
   - Average Temperature (°C)
   - Dynamic updates on dataset change

4. **Charts**
   - Bar chart for parameter averages
   - Pie chart for equipment type distribution
   - Embedded matplotlib charts
   - Auto-refresh on dataset change

5. **Data Table**
   - Display all equipment records
   - Sortable columns
   - Row count display
   - Proper number formatting

6. **State Handling**
   - Loading indicators during API calls
   - Empty state when no data
   - Error messages with retry option
   - Success notifications

## Architecture

```
frontend-desktop/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── api/
│   ├── __init__.py
│   └── client.py          # API client for backend communication
└── ui/
    ├── __init__.py
    ├── main_window.py     # Main application window
    └── widgets/
        ├── __init__.py
        ├── stat_card.py       # Summary statistic cards
        ├── upload_panel.py    # CSV upload interface
        ├── history_panel.py   # Dataset history list
        ├── chart_widget.py    # Matplotlib chart widgets
        └── data_table.py      # Equipment data table
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Django backend running on `http://localhost:8000`

### Setup

1. **Navigate to the desktop app directory:**
   ```bash
   cd frontend-desktop
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

1. **Ensure the backend is running:**
   ```bash
   cd ../backend
   python manage.py runserver
   ```

2. **In a new terminal, start the desktop app:**
   ```bash
   cd frontend-desktop
   python main.py
   ```

### Using the Application

1. **Upload a CSV File:**
   - Click "Choose CSV File" in the right panel
   - Select a CSV file with the required columns
   - Wait for upload and processing

2. **View Data:**
   - Summary cards update automatically
   - Charts display parameter averages and type distribution
   - Table shows all equipment records

3. **Browse History:**
   - Recent datasets appear in the history panel
   - Click any dataset to load it
   - Use the refresh button to reload history

4. **Sort Table Data:**
   - Click column headers to sort
   - Click again to reverse sort order

## API Integration

The desktop app consumes the following backend APIs:

### POST /api/upload/
Upload a CSV file for processing.

**Request:**
- Multipart form data with `file` field

**Response:**
```json
{
  "dataset_id": 1,
  "message": "File uploaded successfully"
}
```

### GET /api/summary/<dataset_id>/
Get summary data for a specific dataset.

**Response:**
```json
{
  "total_equipment": 8,
  "averages": {
    "flowrate": 285.06,
    "pressure": 4.44,
    "temperature": 121.94
  },
  "type_distribution": {
    "Pump": 1,
    "Heat Exchanger": 2,
    "Distillation Column": 1,
    "Reactor": 1,
    "Compressor": 1,
    "Separator": 1,
    "Heater": 1
  },
  "table": [
    {
      "Equipment Name": "Centrifugal Pump P-101",
      "Type": "Pump",
      "Flowrate": 250.5,
      "Pressure": 4.5,
      "Temperature": 35.0
    },
    ...
  ]
}
```

### GET /api/history/
Get list of recent uploads (last 5).

**Response:**
```json
[
  {
    "id": 3,
    "filename": "data1.csv",
    "uploaded_at": "2026-01-27T15:30:00Z"
  },
  ...
]
```

## CSV File Format

The CSV file must contain the following columns:

- **Equipment Name**: Name of the equipment
- **Type**: Equipment type (e.g., Pump, Heat Exchanger, etc.)
- **Flowrate**: Flow rate in m³/h (numeric)
- **Pressure**: Pressure in bar (numeric)
- **Temperature**: Temperature in °C (numeric)

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Centrifugal Pump P-101,Pump,250.5,4.5,35.0
Shell and Tube Exchanger E-201,Heat Exchanger,180.0,3.2,85.5
Packed Column C-301,Distillation Column,320.0,2.8,120.0
```

## Technical Details

### Dependencies

- **PyQt5**: GUI framework
- **requests**: HTTP client for API calls
- **matplotlib**: Chart rendering

### Design Decisions

1. **Threading**: API calls run in separate threads (QThread) to prevent UI freezing
2. **Error Handling**: Comprehensive error handling with user-friendly messages
3. **State Management**: Clear separation between loading, empty, and data states
4. **Styling**: Modern, clean UI matching web app's information hierarchy
5. **Responsiveness**: Minimum window size ensures proper layout on all screens

### Differences from Web App

- **Styling**: Desktop app uses PyQt5 styling instead of Tailwind CSS
- **Icons**: No custom icons in stat cards (simplified for desktop)
- **Animations**: No CSS animations, but smooth state transitions
- **Layout**: Similar information hierarchy but adapted for desktop UX

## Testing Checklist

- [x] Upload multiple CSV files
- [x] Switch between datasets using history
- [x] Restart app and verify history loads
- [x] Trigger backend validation errors (invalid CSV)
- [x] Verify charts update correctly
- [x] Verify table updates correctly
- [x] Test with backend offline (shows warning)
- [x] Sort table columns
- [x] Resize window (responsive layout)

## Troubleshooting

### Backend Connection Error

**Problem:** "Cannot connect to backend server"

**Solution:**
1. Ensure Django backend is running: `python manage.py runserver`
2. Check backend is accessible at `http://localhost:8000`
3. Verify no firewall blocking the connection

### Upload Fails

**Problem:** Upload returns error

**Solution:**
1. Verify CSV has all required columns
2. Check CSV is properly formatted
3. Ensure file is not corrupted
4. Check backend logs for detailed error

### Charts Not Displaying

**Problem:** Charts appear blank

**Solution:**
1. Ensure matplotlib is installed: `pip install matplotlib`
2. Restart the application
3. Check console for errors

## Future Enhancements (Not in Scope)

- PDF export functionality
- User authentication
- Local data caching
- Advanced filtering options
- Custom chart configurations

## Notes

- **No Backend Modifications**: This app only consumes existing APIs
- **No Authentication**: Matches web app (no auth required)
- **No PDF Export**: Not implemented (as per requirements)
- **Read-Only**: Desktop app does not modify or delete data

## PR #4 Completion Checklist

- [x] PyQt5 desktop app created
- [x] Same UI layout as web app (conceptually)
- [x] CSV upload functionality
- [x] Dataset history with selection
- [x] Summary cards (4 metrics)
- [x] Charts (bar + pie)
- [x] Data table with sorting
- [x] Loading states
- [x] Empty states
- [x] Error handling with retry
- [x] Success messages
- [x] No backend modifications
- [x] No new API endpoints
- [x] Backend compatibility confirmed
- [x] README documentation
- [x] Code comments and documentation

## License

Part of the FOSSEE Chemical Equipment Visualizer project.
