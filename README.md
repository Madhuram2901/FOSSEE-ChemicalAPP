# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop + Backend application for visualizing chemical equipment parameters. This application allows users to analyze, visualize, and manage data related to various chemical process equipment.

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.x, Django REST Framework |
| **Web Frontend** | React 18+, Vite, Tailwindcss |
| **Desktop Frontend** | Python, PyQt5, Matplotlib |
| **Database** | SQLite (Development) |
| **Data Processing** | Pandas |
| **Styling** | Vanilla CSS (Web), PyQt5 Stylesheets (Desktop) |

## Features

- **Multi-Platform**: Identical functionality across Web and Desktop interfaces.
- **CSV Data Ingestion**: Robust upload and processing of equipment parameters.
- **Dynamic Visualizations**: Real-time charts for data distributions and metrics.
- **History Management**: Track and revisit previously uploaded datasets.
- **Searchable Inventory**: Instant filtering of equipment lists.
- **Trends Analysis**
- **AI Insights**

```
chemical-equipment-visualizer/
│
├── backend/                    # Django REST API
│   ├── equipment_visualizer/   # Django project settings
│   ├── api/                    # API application
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/               # React web application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components
│   │   └── App.jsx             # Main application entry
│   └── package.json
│
├── frontend-desktop/           # PyQt5 desktop application
│   ├── main.py                 # Main desktop application
│   └── requirements.txt
│
├── sample_equipment_data.csv   # Sample equipment data
├── .gitignore
└── README.md
```

## Setup Instructions

For production deployment details, please see the [Deployment Guide](DEPLOYMENT.md).

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

Backend is hosted completely on **Railway**.

### Web Frontend Setup

Frontend-web is hosted completely on **Vercel**.

### Desktop Application Setup

1. Navigate to the frontend-desktop directory:
   ```bash
   cd frontend-desktop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the desktop application:
   ```bash
   python main.py
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check - returns initialization status |
| POST | `/api/upload/` | Upload CSV for processing |
| GET | `/api/history/` | List most recent 5 datasets |
| GET | `/api/summary/<id>/` | Get detailed summary and data table |

## License

This project is developed for screening task round of FOSSEE.
