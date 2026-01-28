"""
History Panel Widget - Displays dataset history
"""
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
import re


class HistoryPanel(QFrame):
    """Widget for displaying dataset history"""
    
    # Signal emitted when a dataset is selected
    dataset_selected = pyqtSignal(int)
    
    # Signal emitted when refresh is requested
    refresh_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize history panel
        
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
            HistoryPanel {
                background-color: #CDB885;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Header with title and refresh button
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        # Title
        title = QLabel("Recent Datasets")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        
        # Refresh button
        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.setMaximumWidth(100)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 500;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        
        header_layout.addWidget(title)
        header_layout.addWidget(self.refresh_btn)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: #f9fafb;
                padding: 4px;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 10px;
                margin: 4px;
            }
            QListWidget::item:hover {
                background-color: #f3f4f6;
                border-color: #3b82f6;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                border-color: #3b82f6;
                color: #1e40af;
            }
        """)
        self.list_widget.itemClicked.connect(self._handle_item_clicked)
        
        # Empty state label
        self.empty_label = QLabel("No datasets yet.\nUpload a CSV to get started.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 12px;
            padding: 20px;
        """)
        self.empty_label.hide()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.empty_label)
        
        self.setLayout(layout)
    
    def _handle_item_clicked(self, item: QListWidgetItem):
        """Handle item selection"""
        dataset_id = item.data(Qt.UserRole)
        if dataset_id:
            self.dataset_selected.emit(dataset_id)
    
    def set_history(self, history: list):
        """
        Update the history list
        
        Args:
            history: List of dataset dictionaries with id, filename, uploaded_at
        """
        self.list_widget.clear()
        
        if not history:
            self.list_widget.hide()
            self.empty_label.show()
            return
        
        self.list_widget.show()
        self.empty_label.hide()
        
        for dataset in history:
            # Format the uploaded_at timestamp
            try:
                # Parse ISO format timestamp
                dt = datetime.fromisoformat(dataset['uploaded_at'].replace('Z', '+00:00'))
                time_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = dataset['uploaded_at']
            
            # Clean up filename (remove path and handle Windows backslashes)
            clean_filename = dataset['filename'].replace('\\', '/').split('/')[-1]
            
            # Remove Django's random hash suffix (e.g., _Xywndvj)
            # Pattern: _ followed by 7 alphanumerics, just before the extension
            name_parts = clean_filename.rsplit('.', 1)
            if len(name_parts) == 2:
                name, ext = name_parts
                # Matches _ followed by exactly 7 alphanumeric chars at the end of the name
                name = re.sub(r'_[a-zA-Z0-9]{7}$', '', name)
                clean_filename = f"{name}.{ext}"
            
            # Create list item
            item_text = f"{clean_filename}\n{time_str}"
            item = QListWidgetItem(item_text)
            item.setToolTip(dataset['filename'])  # Show full path on hover
            item.setData(Qt.UserRole, dataset['id'])
            
            # Style the item
            font = QFont()
            font.setPointSize(10)
            item.setFont(font)
            
            self.list_widget.addItem(item)
    
    def select_dataset(self, dataset_id: int):
        """
        Select a dataset in the list
        
        Args:
            dataset_id: ID of dataset to select
        """
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.UserRole) == dataset_id:
                self.list_widget.setCurrentItem(item)
                break
    
    def set_loading(self, loading: bool):
        """
        Set loading state
        
        Args:
            loading: Whether data is loading
        """
        self.refresh_btn.setEnabled(not loading)
        if loading:
            self.refresh_btn.setText("Loading...")
        else:
            self.refresh_btn.setText("↻ Refresh")
