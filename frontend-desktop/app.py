"""
Chemical Equipment Parameter Visualizer - Desktop Application
Built with PyQt5
"""

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create and configure the main label
        label = QLabel("Chemical Equipment Parameter Visualizer – Desktop App Initialized")
        label.setAlignment(Qt.AlignCenter)
        
        # Set font styling
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        label.setFont(font)

        # Add label to layout
        layout.addWidget(label)

        # Center the window on screen
        self.center_on_screen()

    def center_on_screen(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Chemical Equipment Parameter Visualizer")
    app.setOrganizationName("Equipment Visualizer")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
