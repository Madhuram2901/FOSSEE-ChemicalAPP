# Desktop Application Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DESKTOP APPLICATION                         │
│                      (PyQt5 + Python)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API                                │
│                   (Django + DRF)                                │
│                                                                 │
│  POST /api/upload/          Upload CSV file                    │
│  GET  /api/summary/<id>/    Get dataset summary                │
│  GET  /api/history/         Get recent datasets                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE                                   │
│                      (SQLite)                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Desktop App Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                    (Entry Point)                                │
│                                                                 │
│  • Initialize QApplication                                      │
│  • Create MainWindow                                            │
│  • Start event loop                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ui/main_window.py                            │
│                   (Main Application Window)                     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      HEADER                                │ │
│  │  • Title: "Chemical Equipment Visualizer"                 │ │
│  │  • Subtitle: "Desktop Analytics Dashboard"                │ │
│  │  • Loading indicator                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────┬─────────────────────────────────┐ │
│  │   MAIN CONTENT (70%)    │   RIGHT SIDEBAR (30%)           │ │
│  │                         │                                 │ │
│  │  ┌──────────────────┐   │  ┌──────────────────────────┐  │ │
│  │  │  Summary Cards   │   │  │   Upload Panel           │  │ │
│  │  │  (4 cards)       │   │  │  • File picker           │  │ │
│  │  └──────────────────┘   │  │  • Requirements info     │  │ │
│  │                         │  └──────────────────────────┘  │ │
│  │  ┌──────────────────┐   │                                 │ │
│  │  │  Charts          │   │  ┌──────────────────────────┐  │ │
│  │  │  • Bar chart     │   │  │   History Panel          │  │ │
│  │  │  • Pie chart     │   │  │  • Recent datasets       │  │ │
│  │  └──────────────────┘   │  │  • Click to select       │  │ │
│  │                         │  │  • Refresh button        │  │ │
│  │  ┌──────────────────┐   │  └──────────────────────────┘  │ │
│  │  │  Data Table      │   │                                 │ │
│  │  │  • 5 columns     │   │                                 │ │
│  │  │  • Sortable      │   │                                 │ │
│  │  └──────────────────┘   │                                 │ │
│  └─────────────────────────┴─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ui/widgets/                                │
│                   (Reusable UI Components)                      │
│                                                                 │
│  • StatCard          - Summary statistic display               │
│  • UploadPanel       - CSV file upload interface               │
│  • HistoryPanel      - Dataset history list                    │
│  • ChartWidget       - Matplotlib chart container              │
│  • ChartsContainer   - Bar + Pie charts                        │
│  • DataTable         - Equipment data table                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Communicates via
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      api/client.py                              │
│                     (API Client Layer)                          │
│                                                                 │
│  • upload_csv(file_path)     → POST /api/upload/               │
│  • get_summary(dataset_id)   → GET /api/summary/<id>/          │
│  • get_history()             → GET /api/history/               │
│  • check_connection()        → GET /api/                       │
│                                                                 │
│  Uses: requests library for HTTP calls                         │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Upload Flow
```
User clicks "Choose CSV File"
         │
         ▼
UploadPanel.file_selected signal
         │
         ▼
MainWindow._handle_upload()
         │
         ▼
APIWorker (QThread)
         │
         ▼
APIClient.upload_csv()
         │
         ▼
POST /api/upload/ (Backend)
         │
         ▼
Backend processes CSV
         │
         ▼
Returns {dataset_id, message}
         │
         ▼
MainWindow._on_upload_success()
         │
         ▼
Reload history + Load new dataset
         │
         ▼
UI updates with new data
```

### Dataset Selection Flow
```
User clicks dataset in history
         │
         ▼
HistoryPanel.dataset_selected signal
         │
         ▼
MainWindow._handle_dataset_selected()
         │
         ▼
APIWorker (QThread)
         │
         ▼
APIClient.get_summary(dataset_id)
         │
         ▼
GET /api/summary/<id>/ (Backend)
         │
         ▼
Returns {total_equipment, averages, type_distribution, table}
         │
         ▼
MainWindow._on_summary_loaded()
         │
         ▼
Update stat cards, charts, and table
```

## Threading Model

```
┌─────────────────────────────────────────────────────────────────┐
│                      MAIN THREAD                                │
│                    (UI Event Loop)                              │
│                                                                 │
│  • Handle user interactions                                     │
│  • Update UI components                                         │
│  • Emit signals                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Spawns
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKER THREADS                               │
│                     (APIWorker)                                 │
│                                                                 │
│  • Execute API calls                                            │
│  • Prevent UI freezing                                          │
│  • Emit finished/error signals                                  │
│                                                                 │
│  Worker 1: Upload CSV                                           │
│  Worker 2: Fetch summary                                        │
│  Worker 3: Fetch history                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Signals back to
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MAIN THREAD                                │
│                   (Update UI with results)                      │
└─────────────────────────────────────────────────────────────────┘
```

## State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION STATES                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   STARTUP    │  • Check backend connection
│              │  • Load history
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    EMPTY     │  • No data loaded
│              │  • Show "No Data Yet" message
└──────┬───────┘  • Upload panel active
       │
       │ User uploads CSV
       ▼
┌──────────────┐
│   LOADING    │  • Show loading indicator
│              │  • Disable buttons
└──────┬───────┘  • "Uploading..." / "Loading..."
       │
       ├─── Success ───┐
       │               ▼
       │         ┌──────────────┐
       │         │     DATA     │  • Summary cards populated
       │         │              │  • Charts displayed
       │         └──────────────┘  • Table filled
       │
       └─── Error ────┐
                      ▼
                ┌──────────────┐
                │    ERROR     │  • Show error dialog
                │              │  • Offer retry option
                └──────────────┘  • Return to previous state
```

## Component Dependencies

```
main.py
  └── MainWindow
       ├── StatCard (x4)
       ├── ChartsContainer
       │    ├── ChartWidget (Bar)
       │    └── ChartWidget (Pie)
       ├── DataTable
       ├── UploadPanel
       ├── HistoryPanel
       └── APIClient
            └── requests
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      DEPENDENCIES                               │
└─────────────────────────────────────────────────────────────────┘

PyQt5 (>=5.15.0)
  • QMainWindow          - Main application window
  • QWidget              - Base widget class
  • QVBoxLayout          - Vertical layouts
  • QHBoxLayout          - Horizontal layouts
  • QGridLayout          - Grid layouts
  • QLabel               - Text labels
  • QPushButton          - Buttons
  • QTableWidget         - Data table
  • QListWidget          - History list
  • QFileDialog          - File picker
  • QMessageBox          - Dialogs
  • QThread              - Worker threads
  • pyqtSignal           - Signal/slot mechanism

requests (>=2.31.0)
  • HTTP client for API calls
  • Multipart file upload
  • Error handling

matplotlib (>=3.7.0)
  • Figure               - Chart container
  • FigureCanvas         - Qt integration
  • pyplot               - Chart creation
  • Bar charts
  • Pie charts
```

## Error Handling Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                      ERROR HANDLING                             │
└─────────────────────────────────────────────────────────────────┘

API Call
  │
  ├─── Network Error
  │     └─→ Show: "Failed to connect to backend"
  │
  ├─── Timeout
  │     └─→ Show: "Request timed out. Please try again."
  │
  ├─── 400 Bad Request
  │     └─→ Show backend error message (e.g., "Missing columns")
  │
  ├─── 404 Not Found
  │     └─→ Show: "Dataset not found"
  │
  ├─── 500 Server Error
  │     └─→ Show: "Server error. Please try again later."
  │
  └─── Success
        └─→ Update UI with data

All errors:
  • Display in QMessageBox
  • Log to console
  • Return to previous state
  • Offer retry option where applicable
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────────┐
│                      OPTIMIZATIONS                              │
└─────────────────────────────────────────────────────────────────┘

1. Threading
   • All API calls in separate threads
   • UI remains responsive during network operations

2. Lazy Loading
   • Charts rendered only when data available
   • Empty state shown when no data

3. Efficient Updates
   • Only update changed components
   • Clear and rebuild instead of incremental updates

4. Memory Management
   • Worker threads cleaned up after completion
   • Old datasets managed by backend (last 5 only)

5. UI Responsiveness
   • Minimum window size: 1200x800
   • Scroll areas for overflow content
   • Proper layout constraints
```

---

**End of Architecture Documentation**
