"""
Data Table Widget - Displays equipment data in a table
"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DataTable(QFrame):
    """Widget for displaying equipment data in a table"""
    
    def __init__(self, parent=None):
        """
        Initialize data table
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Panel styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            DataTable {
                background-color: #CDB885;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
        """)
        # Removed setMaximumHeight to allow expansion
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 20, 12, 10)  # Added 20px top padding
        layout.setSpacing(6)  # Reduced spacing from 8 to 6
        
        # Title
        title = QLabel("Equipment Data")
        title_font = QFont()
        title_font.setPointSize(18)  # Reduced from 13
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        
        # Row count label
        self.row_count_label = QLabel("0 rows")
        self.row_count_label.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
            font-weight: bold;
        """)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Equipment Name',
            'Type',
            'Flowrate (m³/h)',
            'Pressure (bar)',
            'Temperature (°C)'
        ])
        
        # Table styling
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: #ffffff;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f3f4f6;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                color: #374151;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                font-size: 18px;
            }
        """)
        
        # Table settings
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Disable scrollbars - make table strictly non-scrollable
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Resize columns to content
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Equipment Name stretches
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        layout.addWidget(title)
        layout.addWidget(self.row_count_label)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def set_data(self, data: list):
        """
        Set table data
        
        Args:
            data: List of dictionaries with equipment data
        """
        self.table.setRowCount(0)  # Clear existing rows
        
        if not data:
            self.row_count_label.setText("0 rows")
            self.table.setFixedHeight(100)  # Minimum height for empty state
            return
        
        self.table.setRowCount(len(data))
        self.row_count_label.setText(f"{len(data)} row{'s' if len(data) != 1 else ''}")
        
        for row_idx, row_data in enumerate(data):
            # Equipment Name
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get('Equipment Name', ''))))
            
            # Type
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get('Type', ''))))
            
            # Flowrate
            flowrate = row_data.get('Flowrate', 0)
            flowrate_item = QTableWidgetItem(f"{flowrate:.1f}")
            flowrate_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 2, flowrate_item)
            
            # Pressure
            pressure = row_data.get('Pressure', 0)
            pressure_item = QTableWidgetItem(f"{pressure:.1f}")
            pressure_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 3, pressure_item)
            
            # Temperature
            temperature = row_data.get('Temperature', 0)
            temp_item = QTableWidgetItem(f"{temperature:.1f}")
            temp_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, temp_item)
            
        # Dynamic height calculation
        # Header height + (rows * row height) + padding (2px borders)
        header_height = self.table.horizontalHeader().height()
        row_height = self.table.verticalHeader().defaultSectionSize()
        total_height = header_height + (len(data) * row_height) + 4
        
        # Enforce minimum and resize
        self.table.setMinimumHeight(total_height)
        self.table.setMaximumHeight(total_height) # Force exact fit
