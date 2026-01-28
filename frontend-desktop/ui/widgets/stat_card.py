"""
Stat Card Widget - Displays summary statistics
"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class StatCard(QFrame):
    """Widget to display a single statistic with title and value"""
    
    def __init__(self, title: str, parent=None):
        """
        Initialize stat card
        
        Args:
            title: Title of the statistic
            parent: Parent widget
        """
        super().__init__(parent)
        self.title = title
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Card styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            StatCard {
                background-color: #CDB885;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
            StatCard:hover {
                border-color: #3b82f6;
            }
        """)
        self.setFixedHeight(80)  # Set fixed height for compactness
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 10, 12, 10)  # Reduced padding
        layout.setSpacing(4)  # Reduced spacing
        
        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            color: #1f2937;
            font-size: 18px;
            font-weight: bold;
        """)
        
        # Value label
        self.value_label = QLabel("—")
        value_font = QFont()
        value_font.setPointSize(14)  # Reduced from 18
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("""
            color: #111827;
            font-weight: bold;
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_value(self, value: str):
        """
        Update the displayed value
        
        Args:
            value: Value to display
        """
        self.value_label.setText(value)
