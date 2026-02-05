from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginScreen(QWidget):
    login_success = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.addStretch()

        card = QFrame()
        card.setObjectName("glassCard")
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        title = QLabel("ChemViz Login")
        title.setObjectName("cardTitle")

        subtitle = QLabel("Sign in to access your equipment analytics.")
        subtitle.setObjectName("cardSubtitle")
        subtitle.setWordWrap(True)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("Sign In")
        self.button.setObjectName("primaryButton")
        self.button.clicked.connect(self._emit_login)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.button)

        layout.addWidget(card)
        layout.addStretch()

    def _emit_login(self) -> None:
        self.login_success.emit()
