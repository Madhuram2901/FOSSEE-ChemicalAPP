"""
Main Window - Primary application window
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QMessageBox, QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from .widgets import StatCard, UploadPanel, HistoryPanel, ChartsContainer, DataTable
from api import APIClient


class APIWorker(QThread):
    """Worker thread for API calls to prevent UI freezing"""
    
    # Signals
    finished = pyqtSignal(object)  # Success signal with result
    error = pyqtSignal(str)  # Error signal with message
    
    def __init__(self, func, *args, **kwargs):
        """
        Initialize worker
        
        Args:
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Execute the function"""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        self.api_client = APIClient()
        self.current_summary = None
        self.current_dataset_id = None
        self.active_workers = []  # Track active worker threads
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Window settings
        self.setWindowTitle("Chemical Equipment Visualizer - Desktop")
        self.setMinimumSize(1400, 900)
        self.resize(1400, 900)  # Set default size
        
        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #CDB885;")
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content area WITH scroll (restored for responsive table)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: #EFE1B5; border: none; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #EFE1B5;")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(12)
        
        # Left content (main area)
        left_content = self._create_left_content()
        
        # Right sidebar
        right_sidebar = self._create_right_sidebar()
        
        content_layout.addWidget(left_content, stretch=7)
        content_layout.addWidget(right_sidebar, stretch=3)
        
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        
        # Status message labels
        self.status_label = None
    
    def _create_header(self):
        """Create header section"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 1px solid #e5e7eb;
            }
        """)
        header.setFixedHeight(60)  # Reduced from 80
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)  # Reduced padding
        
        # Left side - Title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)  # Reduced spacing
        
        title = QLabel("Chemical Equipment Visualizer")
        title_font = QFont()
        title_font.setPointSize(14)  # Reduced from 18
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        
        title_layout.addWidget(title)
                
        # Right side - Loading indicator
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("""
            color: #3b82f6;
            font-size: 11px;
            font-weight: 600;
        """)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(self.loading_label)
        
        header.setLayout(layout)
        return header
    
    def _create_left_content(self):
        """Create left content area"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(1)  # Reduced from 10 to minimize gaps
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)  # Reduced from 16
        
        self.stat_total = StatCard("Total Equipment")
        self.stat_flowrate = StatCard("Avg Flowrate")
        self.stat_pressure = StatCard("Avg Pressure")
        self.stat_temperature = StatCard("Avg Temperature")
        
        stats_layout.addWidget(self.stat_total, 0, 0)
        stats_layout.addWidget(self.stat_flowrate, 0, 1)
        stats_layout.addWidget(self.stat_pressure, 0, 2)
        stats_layout.addWidget(self.stat_temperature, 0, 3)
        
        # Charts
        self.charts_container = ChartsContainer()
        
        # Data table
        self.data_table = DataTable()
        
        # Empty state
        self.empty_state = self._create_empty_state()
        
        layout.addLayout(stats_layout)
        layout.addWidget(self.charts_container)
        layout.addWidget(self.data_table)
        layout.addWidget(self.empty_state)
        
        # ADDED: Push everything to the top to remove gaps
        layout.addStretch()
        
        # Initially hide charts and table
        self.charts_container.hide()
        self.data_table.hide()
        
        container.setLayout(layout)
        return container
    
    def _create_right_sidebar(self):
        """Create right sidebar"""
        container = QWidget()
        container.setMaximumWidth(350)  # Reduced from 400
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Reduced from 20
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Upload panel
        self.upload_panel = UploadPanel()
        self.upload_panel.file_selected.connect(self._handle_upload)
        
        # History panel
        self.history_panel = HistoryPanel()
        self.history_panel.dataset_selected.connect(self._handle_dataset_selected)
        self.history_panel.refresh_requested.connect(self._load_history)
        
        layout.addWidget(self.upload_panel)
        layout.addWidget(self.history_panel, stretch=1)  # Allow history to expand
        
        container.setLayout(layout)
        return container
    
    def _create_empty_state(self):
        """Create empty state widget"""
        empty = QFrame()
        empty.setFrameShape(QFrame.StyledPanel)
        empty.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        empty.setMinimumHeight(200)  # Reduced from 300
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("📊")
        icon.setStyleSheet("font-size: 48px;")  # Reduced from 64px
        icon.setAlignment(Qt.AlignCenter)
        
        title = QLabel("No Data Yet")
        title_font = QFont()
        title_font.setPointSize(14)  # Reduced from 16
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        title.setAlignment(Qt.AlignCenter)
        
        description = QLabel(
            "Upload a CSV file containing equipment data to see analytics,\n"
            "charts, and detailed breakdowns."
        )
        description.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
        """)
        description.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(description)
        
        empty.setLayout(layout)
        return empty
    
    def _set_loading(self, loading: bool, message: str = ""):
        """Set loading state"""
        if loading:
            self.loading_label.setText(f"⟳ {message}")
        else:
            self.loading_label.setText("")
        
        self.upload_panel.set_loading(loading)
        self.history_panel.set_loading(loading)
    
    def _show_message(self, message: str, is_error: bool = False):
        """Show status message"""
        if is_error:
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Success", message)
    
    def _load_initial_data(self):
        """Load initial data on startup"""
        # Check backend connection
        if not self.api_client.check_connection():
            QMessageBox.warning(
                self,
                "Backend Not Available",
                "Cannot connect to backend server at http://localhost:8000\n\n"
                "Please ensure the Django backend is running:\n"
                "1. Navigate to the backend directory\n"
                "2. Run: python manage.py runserver\n\n"
                "You can still use the app once the backend is started."
            )
            return
        
        # Load history
        self._load_history()
    
    def _load_history(self):
        """Load dataset history"""
        self._set_loading(True, "Loading history...")
        
        worker = APIWorker(self.api_client.get_history)
        worker.finished.connect(self._on_history_loaded)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        worker.error.connect(self._on_history_error)
        worker.error.connect(lambda: self._cleanup_worker(worker))
        worker.start()
        
        # Track active worker
        self.active_workers.append(worker)
    
    def _on_history_loaded(self, history):
        """Handle history loaded"""
        self._set_loading(False)
        self.history_panel.set_history(history)
        
        # Auto-load latest dataset if available and no current data
        if history and not self.current_summary:
            latest_id = history[0]['id']
            self._handle_dataset_selected(latest_id)
    
    def _on_history_error(self, error):
        """Handle history error"""
        self._set_loading(False)
        self._show_message(f"Failed to load history: {error}", is_error=True)
    
    def _handle_upload(self, file_path: str):
        """Handle file upload"""
        self._set_loading(True, "Uploading file...")
        
        worker = APIWorker(self.api_client.upload_csv, file_path)
        worker.finished.connect(self._on_upload_success)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        worker.error.connect(self._on_upload_error)
        worker.error.connect(lambda: self._cleanup_worker(worker))
        worker.start()
        
        # Track active worker
        self.active_workers.append(worker)
    
    def _on_upload_success(self, result):
        """Handle upload success"""
        self._set_loading(False)
        self._show_message("File uploaded and processed successfully!")
        
        # Reload history and select new dataset
        dataset_id = result['dataset_id']
        self._load_history()
        self._handle_dataset_selected(dataset_id)
    
    def _on_upload_error(self, error):
        """Handle upload error"""
        self._set_loading(False)
        self._show_message(f"Upload failed: {error}", is_error=True)
    
    def _handle_dataset_selected(self, dataset_id: int):
        """Handle dataset selection"""
        self.current_dataset_id = dataset_id
        self._set_loading(True, "Loading dataset...")
        
        worker = APIWorker(self.api_client.get_summary, dataset_id)
        worker.finished.connect(self._on_summary_loaded)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        worker.error.connect(self._on_summary_error)
        worker.error.connect(lambda: self._cleanup_worker(worker))
        worker.start()
        
        # Track active worker
        self.active_workers.append(worker)
    
    def _on_summary_loaded(self, summary):
        """Handle summary loaded"""
        self._set_loading(False)
        self.current_summary = summary
        self._update_ui_with_data(summary)
        
        # Select in history
        if self.current_dataset_id:
            self.history_panel.select_dataset(self.current_dataset_id)
    
    def _on_summary_error(self, error):
        """Handle summary error"""
        self._set_loading(False)
        self._show_message(f"Failed to load dataset: {error}", is_error=True)
    
    def _update_ui_with_data(self, data: dict):
        """Update UI with summary data"""
        # Hide empty state, show data widgets
        self.empty_state.hide()
        self.charts_container.show()
        self.data_table.show()
        
        # Update stat cards
        self.stat_total.set_value(f"{data['total_equipment']} units")
        self.stat_flowrate.set_value(f"{data['averages']['flowrate']:.2f} m³/h")
        self.stat_pressure.set_value(f"{data['averages']['pressure']:.2f} bar")
        self.stat_temperature.set_value(f"{data['averages']['temperature']:.2f} °C")
        
        # Update charts
        self.charts_container.update_charts(data)
        
        # Update table
        self.data_table.set_data(data['table'])
    
    def _cleanup_worker(self, worker):
        """Remove finished worker from active workers list"""
        if worker in self.active_workers:
            self.active_workers.remove(worker)
    
    def closeEvent(self, event):
        """Handle window close event - cleanup worker threads"""
        # Wait for all active workers to finish
        for worker in self.active_workers:
            if worker.isRunning():
                worker.quit()  # Ask thread to quit
                worker.wait(1000)  # Wait up to 1 second
        
        # Clear the list
        self.active_workers.clear()
        
        # Accept the close event
        event.accept()
