import re

import requests
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

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")

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
        card_layout.addWidget(self.full_name)
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
        full_name = self.full_name.text().strip()
        email = self.email.text().strip().lower()
        password = self.password.text().strip()
        confirm = self.confirm.text().strip()

        if not full_name or not email or not password:
            self.error_label.setText("Full name, email, and password are required.")
            return

        if len(full_name) < 2 or not re.fullmatch(r"[A-Za-z ]+", full_name):
            self.error_label.setText("Full name must be 2+ characters (letters and spaces).")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.error_label.setText("Enter a valid email address.")
            return

        if len(password) < 8:
            self.error_label.setText("Password must be at least 8 characters.")
            return

        if " " in password:
            self.error_label.setText("Password cannot contain spaces.")
            return

        if not re.search(r"[A-Z]", password):
            self.error_label.setText("Password must include an uppercase letter.")
            return

        if not re.search(r"[a-z]", password):
            self.error_label.setText("Password must include a lowercase letter.")
            return

        if not re.search(r"\d", password):
            self.error_label.setText("Password must include a number.")
            return

        if not confirm:
            self.error_label.setText("Confirm password is required.")
            return

        if password != confirm:
            self.error_label.setText("Passwords do not match.")
            return

        try:
            client.register(full_name, email, password, confirm)
            QMessageBox.information(self, "Success", "Account created successfully.")
            self.register_success.emit()
        except requests.HTTPError as exc:
            message = "Registration failed. Please try again."
            if exc.response is not None:
                try:
                    data = exc.response.json()
                    if isinstance(data, dict) and data:
                        message = str(next(iter(data.values())))
                except ValueError:
                    pass
            self.error_label.setText(message)
        except Exception:
            self.error_label.setText("Registration failed. Please try again.")
