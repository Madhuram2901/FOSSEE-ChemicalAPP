"""
Upload Panel Widget - Handles CSV file upload
"""
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import os


class UploadPanel(QFrame):
    """Widget for CSV file upload"""
    
    # Signal emitted when a file is selected for upload
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize upload panel
        
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
            UploadPanel {
                background-color: #CDB885;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced padding
        layout.setSpacing(10)  # Reduced spacing
        
        # Title
        title = QLabel("Upload CSV")
        title_font = QFont()
        title_font.setPointSize(12)  # Reduced from 14
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #111827;")
        
        # Description - removed to save space
        
        # Upload button
        self.upload_btn = QPushButton("Choose CSV File")
        self.upload_btn.setMinimumHeight(36)  # Reduced from 40
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
                cursor: not-allowed;
            }
        """)
        self.upload_btn.clicked.connect(self._handle_upload)
        
    
        # Requirements info - more compact
        requirements = QLabel(
            "Required: Equipment Name, Type,\nFlowrate, Pressure, Temperature"
        )
        requirements.setStyleSheet("""
            color: #6b7280;
            font-size: 16px;
            font-weight: bold;
            background-color: #EFE1B5;
            border-radius: 4px;
            padding: 6px;
        """)
        
        layout.addWidget(title)
        layout.addWidget(self.upload_btn)
        layout.addWidget(requirements)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def _handle_upload(self):
        """Handle file selection"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Validate file extension
            if not file_path.lower().endswith('.csv'):
                QMessageBox.warning(
                    self,
                    "Invalid File",
                    "Please select a CSV file (.csv extension)"
                )
                return
                    
            # Emit signal
            self.file_selected.emit(file_path)
    
    def set_loading(self, loading: bool):
        """
        Set loading state
        
        Args:
            loading: Whether upload is in progress
        """
        self.upload_btn.setEnabled(not loading)
        if loading:
            self.upload_btn.setText("Uploading...")
        else:
            self.upload_btn.setText("Choose CSV File")
