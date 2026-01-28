# Quick Reference Card - Desktop Application

## 🚀 Quick Start

```bash
cd frontend-desktop
run.bat                    # Windows quick start
# OR
python main.py            # Manual start
```

## 📋 Prerequisites

- ✅ Python 3.8+
- ✅ Backend running at http://localhost:8000
- ✅ Dependencies: `pip install -r requirements.txt`

## 🎯 Key Features

| Feature | Location | Action |
|---------|----------|--------|
| **Upload CSV** | Right panel → "Choose CSV File" | Click to select file |
| **View History** | Right panel → History list | Click dataset to load |
| **Refresh History** | Right panel → "↻ Refresh" | Click to reload |
| **Sort Table** | Main area → Table headers | Click to sort |
| **View Charts** | Main area → Middle section | Auto-updates |

## 📊 UI Layout

```
┌────────────────────────────────────────────────────────┐
│  HEADER: Chemical Equipment Visualizer                │
├────────────────────────────────┬───────────────────────┤
│  MAIN CONTENT (70%)            │  SIDEBAR (30%)        │
│                                │                       │
│  [Card] [Card] [Card] [Card]   │  ┌─────────────────┐ │
│                                │  │ Upload CSV      │ │
│  ┌──────────┐  ┌──────────┐   │  │ [Choose File]   │ │
│  │ Bar Chart│  │ Pie Chart│   │  └─────────────────┘ │
│  └──────────┘  └──────────┘   │                       │
│                                │  ┌─────────────────┐ │
│  ┌──────────────────────────┐ │  │ History         │ │
│  │ Equipment Data Table     │ │  │ • Dataset 1     │ │
│  │ [Sortable columns]       │ │  │ • Dataset 2     │ │
│  └──────────────────────────┘ │  └─────────────────┘ │
└────────────────────────────────┴───────────────────────┘
```

## 🔌 API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/summary/<id>/` | Get dataset summary |
| GET | `/api/history/` | List recent datasets |

## 📁 CSV Format

**Required Columns:**
- Equipment Name
- Type
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump P-101,Pump,250.5,4.5,35.0
Heat Exchanger E-201,Heat Exchanger,180.0,3.2,85.5
```

## 🎨 Summary Cards

1. **Total Equipment** - Count of equipment units
2. **Avg Flowrate** - Average in m³/h
3. **Avg Pressure** - Average in bar
4. **Avg Temperature** - Average in °C

## 📈 Charts

1. **Bar Chart** - Parameter averages (Flowrate, Pressure, Temperature)
2. **Pie Chart** - Equipment type distribution

## 🗂️ Data Table

- **Columns:** Equipment Name, Type, Flowrate, Pressure, Temperature
- **Features:** Sortable, row count, formatted numbers
- **Sorting:** Click column header to sort

## ⚠️ Common Issues

### Backend Not Running
**Error:** "Cannot connect to backend server"  
**Solution:** Start backend with `python manage.py runserver`

### Upload Fails
**Error:** "Missing columns: ..."  
**Solution:** Ensure CSV has all required columns

### Charts Not Showing
**Error:** Blank chart area  
**Solution:** Ensure matplotlib is installed: `pip install matplotlib`

## 🔄 Workflow

1. **Start Backend**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start Desktop App**
   ```bash
   cd frontend-desktop
   python main.py
   ```

3. **Upload CSV**
   - Click "Choose CSV File"
   - Select your CSV
   - Wait for processing

4. **View Data**
   - Summary cards update
   - Charts display
   - Table shows all records

5. **Switch Datasets**
   - Click dataset in history
   - UI updates automatically

## 🧪 Testing

Run through **TESTING.md** for comprehensive test cases:
- 22 test cases
- Covers all features
- Includes edge cases

## 📚 Documentation

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `TESTING.md` | Test cases |
| `ARCHITECTURE.md` | System architecture |
| `PR4_COMPLETION_REPORT.md` | Completion report |
| `SUMMARY.md` | Executive summary |

## 🛠️ File Structure

```
frontend-desktop/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── run.bat             # Quick start
├── api/
│   └── client.py       # API integration
└── ui/
    ├── main_window.py  # Main window
    └── widgets/        # UI components
```

## 💡 Tips

- **Sorting:** Click table headers to sort data
- **History:** Auto-loads latest dataset on startup
- **Refresh:** Use refresh button to reload history
- **Errors:** Check backend logs for detailed errors
- **Performance:** App handles 100+ rows smoothly

## 🔑 Keyboard Shortcuts

- **Ctrl+Q** - Quit application (standard)
- **Alt+F4** - Close window (Windows)

## 📞 Support

For issues or questions:
1. Check **README.md** for detailed docs
2. Review **TESTING.md** for test cases
3. Check backend logs for API errors
4. Verify backend is running

## ✅ Quick Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Backend running on port 8000
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV file ready with required columns

## 🎯 Success Criteria

App is working correctly when:
- ✅ Window opens without errors
- ✅ History loads on startup
- ✅ CSV uploads successfully
- ✅ Summary cards show data
- ✅ Charts display correctly
- ✅ Table shows all records
- ✅ Dataset switching works

## 📊 Performance

- **Startup:** < 2 seconds
- **Upload:** Depends on file size
- **Dataset Switch:** < 1 second
- **Chart Render:** < 500ms

---

**Version:** 1.0  
**Last Updated:** 2026-01-27  
**PR:** #4 - PyQt5 Desktop Application
