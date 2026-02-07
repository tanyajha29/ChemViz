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


class LoginScreen(QWidget):
    login_success = pyqtSignal()
    register_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(420)
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

        title = QLabel("Welcome back")
        title.setObjectName("authTitle")

        subtitle = QLabel("Sign in to access your analytics.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setWordWrap(True)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorText")

        self.button = QPushButton("Sign In")
        self.button.setObjectName("primaryButton")
        self.button.clicked.connect(self._handle_login)

        self.link_button = QPushButton("New here? Create an account")
        self.link_button.setObjectName("authLink")
        self.link_button.clicked.connect(self.register_requested.emit)

        title.setAlignment(Qt.AlignCenter)
        subtitle.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(logo, alignment=Qt.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(self.button)
        card_layout.addWidget(self.link_button, alignment=Qt.AlignCenter)

        layout.addWidget(card, alignment=Qt.AlignHCenter)
        layout.addStretch()

    def _handle_login(self) -> None:
        self.error_label.setText("")
        username = self.username.text().strip()
        password = self.password.text()

        if not username or not password:
            self.error_label.setText("Please enter username and password.")
            return

        try:
            client.login(username, password)
            QMessageBox.information(self, "Success", "Login successful.")
            self.login_success.emit()
        except Exception:
            self.error_label.setText("Login failed. Check credentials.")
