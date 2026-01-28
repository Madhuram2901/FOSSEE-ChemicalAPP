# Desktop Application Testing Guide

## Pre-Testing Setup

### 1. Start the Backend Server

```bash
cd backend
python manage.py runserver
```

Verify backend is running by visiting: http://localhost:8000/api/

### 2. Install Desktop App Dependencies

```bash
cd frontend-desktop
pip install -r requirements.txt
```

## Test Cases

### Test 1: Application Startup

**Steps:**
1. Run `python main.py`
2. Observe the main window opens

**Expected Results:**
- ✅ Window opens with title "Chemical Equipment Visualizer - Desktop"
- ✅ Header shows "Chemical Equipment Visualizer" and "Desktop Analytics Dashboard"
- ✅ Empty state is visible with "No Data Yet" message
- ✅ Upload panel is visible on the right
- ✅ History panel is visible below upload panel
- ✅ If backend is running, history loads automatically

**Pass/Fail:** _______

---

### Test 2: Backend Connection Check

**Steps:**
1. Stop the backend server
2. Start the desktop app
3. Observe the warning dialog

**Expected Results:**
- ✅ Warning dialog appears: "Backend Not Available"
- ✅ Dialog explains how to start the backend
- ✅ App still opens after dismissing dialog

**Pass/Fail:** _______

---

### Test 3: CSV Upload - Success

**Steps:**
1. Ensure backend is running
2. Click "Choose CSV File"
3. Select `data1.csv` from the root directory
4. Wait for upload to complete

**Expected Results:**
- ✅ File dialog opens
- ✅ After selection, "Selected: data1.csv" appears
- ✅ Loading indicator shows "⟳ Uploading file..."
- ✅ Success message appears: "File uploaded and processed successfully!"
- ✅ Empty state disappears
- ✅ Summary cards populate with data
- ✅ Charts appear (bar chart and pie chart)
- ✅ Data table shows equipment records
- ✅ History panel updates with new entry

**Pass/Fail:** _______

---

### Test 4: CSV Upload - Invalid File

**Steps:**
1. Click "Choose CSV File"
2. Select a non-CSV file (e.g., .txt or .jpg)

**Expected Results:**
- ✅ Warning dialog: "Invalid File - Please select a CSV file"
- ✅ No upload occurs
- ✅ UI remains in previous state

**Pass/Fail:** _______

---

### Test 5: CSV Upload - Missing Columns

**Steps:**
1. Create a CSV file with missing required columns
2. Upload the file

**Expected Results:**
- ✅ Error dialog appears with message about missing columns
- ✅ No data is displayed
- ✅ UI returns to previous state

**Pass/Fail:** _______

---

### Test 6: Dataset History Loading

**Steps:**
1. Upload 3 different CSV files (data1.csv, data2.csv, data3.csv)
2. Observe the history panel

**Expected Results:**
- ✅ History panel shows all 3 datasets
- ✅ Each entry shows filename and timestamp
- ✅ Most recent upload is at the top
- ✅ Entries are clickable

**Pass/Fail:** _______

---

### Test 7: Dataset Selection from History

**Steps:**
1. Upload multiple datasets
2. Click on a dataset in the history panel
3. Observe the UI updates

**Expected Results:**
- ✅ Loading indicator appears
- ✅ Summary cards update with selected dataset's data
- ✅ Charts refresh with new data
- ✅ Table updates with new equipment records
- ✅ Selected dataset is highlighted in history

**Pass/Fail:** _______

---

### Test 8: History Refresh

**Steps:**
1. Click the "↻ Refresh" button in history panel
2. Observe the behavior

**Expected Results:**
- ✅ Button shows "Loading..."
- ✅ History list refreshes
- ✅ Button returns to "↻ Refresh"

**Pass/Fail:** _______

---

### Test 9: Summary Cards Display

**Steps:**
1. Upload data1.csv
2. Verify the summary cards

**Expected Results:**
- ✅ Total Equipment shows "8 units"
- ✅ Avg Flowrate shows "285.06 m³/h"
- ✅ Avg Pressure shows "4.44 bar"
- ✅ Avg Temperature shows "121.94 °C"
- ✅ All values are properly formatted

**Pass/Fail:** _______

---

### Test 10: Bar Chart Display

**Steps:**
1. Upload a dataset
2. Examine the bar chart

**Expected Results:**
- ✅ Chart title: "Parameter Averages"
- ✅ Three bars: Flowrate, Pressure, Temperature
- ✅ Different colors for each bar
- ✅ Value labels on top of bars
- ✅ Y-axis labeled "Value"
- ✅ Grid lines visible

**Pass/Fail:** _______

---

### Test 11: Pie Chart Display

**Steps:**
1. Upload a dataset
2. Examine the pie chart

**Expected Results:**
- ✅ Chart title: "Equipment Type Distribution"
- ✅ Slices for each equipment type
- ✅ Percentages shown on slices
- ✅ Labels for each type
- ✅ Different colors for each slice

**Pass/Fail:** _______

---

### Test 12: Data Table Display

**Steps:**
1. Upload data1.csv
2. Examine the data table

**Expected Results:**
- ✅ Table title: "Equipment Data"
- ✅ Row count shows "8 rows"
- ✅ 5 columns: Equipment Name, Type, Flowrate, Pressure, Temperature
- ✅ All 8 equipment records visible
- ✅ Numeric values right-aligned
- ✅ Values formatted to 1 decimal place

**Pass/Fail:** _______

---

### Test 13: Table Sorting

**Steps:**
1. Upload a dataset
2. Click on "Flowrate (m³/h)" column header
3. Click again

**Expected Results:**
- ✅ First click: Table sorts by flowrate ascending
- ✅ Second click: Table sorts by flowrate descending
- ✅ Sorting works for all columns

**Pass/Fail:** _______

---

### Test 14: Multiple Dataset Switching

**Steps:**
1. Upload data1.csv
2. Note the total equipment count
3. Upload data2.csv
4. Click on data1.csv in history
5. Click on data2.csv in history

**Expected Results:**
- ✅ UI updates correctly for each dataset
- ✅ Summary cards change
- ✅ Charts update
- ✅ Table shows correct data
- ✅ No errors or lag

**Pass/Fail:** _______

---

### Test 15: Application Restart with History

**Steps:**
1. Upload 2-3 datasets
2. Close the application
3. Restart the application

**Expected Results:**
- ✅ History panel loads previous datasets
- ✅ Most recent dataset is auto-loaded
- ✅ Summary cards, charts, and table show latest data

**Pass/Fail:** _______

---

### Test 16: Window Resizing

**Steps:**
1. Load a dataset
2. Resize the window to minimum size
3. Maximize the window
4. Resize to various sizes

**Expected Results:**
- ✅ Minimum size is 1200x800
- ✅ Layout remains functional at all sizes
- ✅ Scroll bars appear when needed
- ✅ No UI elements overlap or disappear

**Pass/Fail:** _______

---

### Test 17: Loading States

**Steps:**
1. Upload a large CSV file
2. Observe loading indicators

**Expected Results:**
- ✅ Loading message appears in header
- ✅ Upload button shows "Uploading..."
- ✅ Upload button is disabled during upload
- ✅ Refresh button disabled during history load

**Pass/Fail:** _______

---

### Test 18: Error Recovery

**Steps:**
1. Stop the backend
2. Try to upload a file
3. Observe error message
4. Start the backend
5. Click refresh in history panel

**Expected Results:**
- ✅ Error dialog shows connection error
- ✅ After backend restart, refresh works
- ✅ App recovers without restart

**Pass/Fail:** _______

---

### Test 19: Empty History State

**Steps:**
1. Clear all datasets from backend (delete db.sqlite3 and recreate)
2. Start desktop app

**Expected Results:**
- ✅ History panel shows "No datasets yet. Upload a CSV to get started."
- ✅ Empty state visible in main area
- ✅ Upload panel is functional

**Pass/Fail:** _______

---

### Test 20: Concurrent Operations Prevention

**Steps:**
1. Click upload
2. Immediately click refresh
3. Observe behavior

**Expected Results:**
- ✅ Only one operation executes at a time
- ✅ Buttons are disabled during operations
- ✅ No crashes or errors

**Pass/Fail:** _______

---

## Performance Tests

### Test 21: Large Dataset

**Steps:**
1. Create a CSV with 100+ rows
2. Upload and observe

**Expected Results:**
- ✅ Upload completes successfully
- ✅ Table displays all rows
- ✅ Charts render correctly
- ✅ No significant lag

**Pass/Fail:** _______

---

### Test 22: Rapid Dataset Switching

**Steps:**
1. Upload 5 datasets
2. Rapidly click between them in history

**Expected Results:**
- ✅ UI updates smoothly
- ✅ No crashes
- ✅ Correct data shown for each

**Pass/Fail:** _______

---

## Summary

**Total Tests:** 22  
**Passed:** _______  
**Failed:** _______  
**Pass Rate:** _______%

## Notes

_Add any observations, bugs, or issues here:_

---

## Sign-off

**Tester Name:** _______________________  
**Date:** _______________________  
**Signature:** _______________________
