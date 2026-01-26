# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop + Backend application for visualizing chemical equipment parameters. This application allows users to analyze, visualize, and manage data related to various chemical process equipment.

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.x, Django REST Framework |
| **Web Frontend** | React 18+, Vite |
| **Desktop Frontend** | Python, PyQt5, Matplotlib |
| **Database** | SQLite (Development) |
| **Data Processing** | Pandas |

## Repository Structure

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
│   ├── app.py                  # Main desktop application
│   └── requirements.txt
│
├── sample_equipment_data.csv   # Sample equipment data
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
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

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

### Web Frontend Setup

1. Navigate to the frontend-web directory:
   ```bash
   cd frontend-web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The web application will be available at `http://localhost:5173/`

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
   python app.py
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check - returns initialization status |

## License

This project is developed for educational and demonstration purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
