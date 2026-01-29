"""
Chemical Equipment Visualizer - Desktop Application
Main entry point for the PyQt5 desktop client
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui import MainWindow
from ui.auth_window import LoginWindow, SignupWindow
from api import APIClient


from config import API_BASE_URL


class AppController:
    """Manages application flow"""
    def __init__(self):
        self.api_client = APIClient(base_url=API_BASE_URL)
        self.login_window = None
        self.signup_window = None
        self.main_window = None

    def start(self):
        """Start the application"""
        # Check if we have a valid token
        if self.api_client.token and self.api_client.check_connection():
             self.show_main()
        else:
             self.show_login()

    def show_login(self):
        """Show login window"""
        if self.main_window:
            self.main_window.close()
        if self.signup_window:
            self.signup_window.close()

        self.login_window = LoginWindow(self.api_client)
        self.login_window.login_success.connect(self.show_main)
        self.login_window.open_signup.connect(self.show_signup)
        self.login_window.show()

    def show_signup(self):
        """Show signup window"""
        if self.login_window:
            self.login_window.close()
        
        self.signup_window = SignupWindow(self.api_client)
        self.signup_window.open_login.connect(self.show_login)
        self.signup_window.show()

    def show_main(self):
        """Show main dashboard"""
        if self.login_window:
            self.login_window.close()
        
        self.main_window = MainWindow()
        # Wire up logout if we add a logout button to MainWindow later
        # For now, if the token becomes invalid during use, MainWindow handles re-auth partially
        # But for full logout we would need a signal from MainWindow
        self.main_window.logout_requested.connect(self.handle_logout)
        self.main_window.show()
    
    def handle_logout(self):
        """Handle logout request"""
        self.api_client.logout()
        self.show_login()


def main():
    """Main application entry point"""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("FOSSEE")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Init Controller
    controller = AppController()
    controller.start()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
