import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QLineEdit,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class ProfileScreen(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.editing = False
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

        self.username_input = QLineEdit()
        self.username_input.setObjectName("profileInput")
        self.username_input.setReadOnly(True)

        self.email_input = QLineEdit()
        self.email_input.setObjectName("profileInput")
        self.email_input.setReadOnly(True)

        self.role_label = QLabel("Role: --")
        self.role_label.setObjectName("profileRow")
        self.status_label = QLabel("")
        self.status_label.setObjectName("cardSubtitle")

        card_layout.addWidget(QLabel("Username"))
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(QLabel("Email"))
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.role_label)
        card_layout.addWidget(self.status_label)

        self.edit_button = QPushButton("Edit Profile")
        self.edit_button.setObjectName("primaryButton")
        self.edit_button.clicked.connect(self._toggle_edit)
        card_layout.addWidget(self.edit_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("ghostButton")
        self.cancel_button.clicked.connect(self._cancel_edit)
        self.cancel_button.setVisible(False)
        card_layout.addWidget(self.cancel_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout_requested.emit)
        card_layout.addWidget(self.logout_button)

        layout.addWidget(self.card)
        layout.addStretch()

    def refresh(self) -> None:
        try:
            profile = client.fetch_profile()
            username = profile.get("username", "")
            email = profile.get("email", "")
            role = profile.get("role", "--")
            self.username_input.setText(username)
            self.email_input.setText(email)
            self.role_label.setText(f"Role: {role}")
            self.status_label.setText("")
        except Exception:
            self.status_label.setText("Unable to load profile.")

    def _toggle_edit(self) -> None:
        if not self.editing:
            self.editing = True
            self.username_input.setReadOnly(False)
            self.email_input.setReadOnly(False)
            self.edit_button.setText("Save Changes")
            self.cancel_button.setVisible(True)
            return

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()

        if not username or not email:
            self.status_label.setText("Username and email are required.")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.status_label.setText("Enter a valid email address.")
            return

        try:
            updated = client.update_profile(username, email)
            self.username_input.setText(updated.get("username", username))
            self.email_input.setText(updated.get("email", email))
            self.role_label.setText(f"Role: {updated.get('role', 'User')}")
            QMessageBox.information(self, "Success", "Profile updated.")
            self._stop_edit()
        except Exception:
            self.status_label.setText("Unable to update profile.")

    def _cancel_edit(self) -> None:
        self._stop_edit()
        self.refresh()

    def _stop_edit(self) -> None:
        self.editing = False
        self.username_input.setReadOnly(True)
        self.email_input.setReadOnly(True)
        self.edit_button.setText("Edit Profile")
        self.cancel_button.setVisible(False)
