from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from services.api_client import client


class ProfileScreen(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        header = QLabel("Profile")
        header.setObjectName("pageTitle")
        sub = QLabel("Account details and session information.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        self.card = QFrame()
        self.card.setObjectName("profileCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(12)

        self.username_label = QLabel("Username: --")
        self.username_label.setObjectName("profileRow")
        self.email_label = QLabel("Email: --")
        self.email_label.setObjectName("profileRow")
        self.role_label = QLabel("Role: --")
        self.role_label.setObjectName("profileRow")
        self.status_label = QLabel("")
        self.status_label.setObjectName("cardSubtitle")

        card_layout.addWidget(self.username_label)
        card_layout.addWidget(self.email_label)
        card_layout.addWidget(self.role_label)
        card_layout.addWidget(self.status_label)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout_requested.emit)
        card_layout.addWidget(self.logout_button)

        layout.addWidget(self.card)
        layout.addStretch()

    def refresh(self) -> None:
        try:
            profile = client.fetch_profile()
            username = profile.get("username", "--")
            email = profile.get("email", "--")
            role = profile.get("role", "--")
            self.username_label.setText(f"Username: {username}")
            self.email_label.setText(f"Email: {email}")
            self.role_label.setText(f"Role: {role}")
            self.status_label.setText("")
        except Exception:
            self.status_label.setText("Unable to load profile.")
