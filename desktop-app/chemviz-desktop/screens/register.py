import re

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class RegisterScreen(QWidget):
    register_success = pyqtSignal()
    login_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(460)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(26, 24, 26, 24)
        card_layout.setSpacing(10)

        logo = QFrame()
        logo.setObjectName("authLogo")
        logo.setFixedSize(52, 52)
        logo_layout = QVBoxLayout(logo)
        logo_layout.setContentsMargins(0, 0, 0, 0)

        logo_label = QLabel("CV")
        logo_label.setObjectName("authLogoText")
        logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        title = QLabel("Create account")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Set up access for your equipment analytics.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm password")
        self.confirm.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorText")

        self.button = QPushButton("Create Account")
        self.button.setObjectName("primaryButton")
        self.button.clicked.connect(self._handle_register)

        self.link_button = QPushButton("Already have an account? Sign in")
        self.link_button.setObjectName("authLink")
        self.link_button.clicked.connect(self.login_requested.emit)

        card_layout.addWidget(logo, alignment=Qt.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.email)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.confirm)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(self.button)
        card_layout.addWidget(self.link_button, alignment=Qt.AlignCenter)

        layout.addWidget(card, alignment=Qt.AlignHCenter)
        layout.addStretch()

    def _handle_register(self) -> None:
        self.error_label.setText("")
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text()
        confirm = self.confirm.text()

        if not username or not email or not password:
            self.error_label.setText("Username, email, and password are required.")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.error_label.setText("Enter a valid email address.")
            return

        if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            self.error_label.setText("Password must be 8+ characters with letters and numbers.")
            return

        if password != confirm:
            self.error_label.setText("Passwords do not match.")
            return

        try:
            client.register(username, email, password)
            QMessageBox.information(self, "Success", "Account created successfully.")
            self.register_success.emit()
        except Exception:
            self.error_label.setText("Registration failed. Try a different username.")
