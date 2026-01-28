from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFrame, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class AuthWindow(QWidget):
    """Base class for Auth windows"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setFixedSize(450, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #4F200D;
                color: #ffffff;
            }
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #374151;
                background-color: #1F2937;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton#linkButton {
                background-color: transparent;
                color: #60A5FA;
                text-align: center;
                border: none;
            }
            QPushButton#linkButton:hover {
                color: #93C5FD;
                text-decoration: underline;
            }
        """)

class LoginWindow(AuthWindow):
    login_success = pyqtSignal()
    open_signup = pyqtSignal()

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Icon/Logo Placeholder
        logo_label = QLabel("⚗️")
        logo_label.setStyleSheet("font-size: 64px;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title_label = QLabel("Welcome Back")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        sub_label = QLabel("Sign in to access your dashboard")
        sub_label.setStyleSheet("color: #9CA3AF; margin-bottom: 20px;")
        sub_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub_label)

        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login Button
        login_btn = QPushButton("Sign In")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self._handle_login)
        layout.addWidget(login_btn)

        # Switch to Signup
        signup_layout = QHBoxLayout()
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet("color: #9CA3AF;")
        signup_btn = QPushButton("Create Account")
        signup_btn.setObjectName("linkButton")
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.clicked.connect(self.open_signup.emit)
        
        signup_layout.addStretch()
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_btn)
        signup_layout.addStretch()
        
        layout.addLayout(signup_layout)

        self.setLayout(layout)

    def _handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            self.api_client.login(username, password)
            self.login_success.emit()
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", str(e))


class SignupWindow(AuthWindow):
    signup_success = pyqtSignal()
    open_login = pyqtSignal()

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Icon/Logo Placeholder
        logo_label = QLabel("🚀")
        logo_label.setStyleSheet("font-size: 64px;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title_label = QLabel("Create Account")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Subtitle
        sub_label = QLabel("Join to visualize your equipment parameters")
        sub_label.setStyleSheet("color: #9CA3AF; margin-bottom: 20px;")
        sub_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub_label)

        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_input)

        # Signup Button
        signup_btn = QPushButton("Create Account")
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.clicked.connect(self._handle_signup)
        layout.addWidget(signup_btn)

        # Switch to Login
        login_layout = QHBoxLayout()
        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: #9CA3AF;")
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("linkButton")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.open_login.emit)
        
        login_layout.addStretch()
        login_layout.addWidget(login_label)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()

        layout.addLayout(login_layout)

        self.setLayout(layout)

    def _handle_signup(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            self.api_client.register(username, email, password)
            QMessageBox.information(self, "Success", "Account created! Please sign in.")
            self.open_login.emit()
        except Exception as e:
            QMessageBox.critical(self, "Registration Failed", str(e))
