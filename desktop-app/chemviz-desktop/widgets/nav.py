from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout


class NavWidget(QFrame):
    route_changed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("navPanel")
        self.setFixedWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        self.btn_dashboard = self._make_button("Dashboard", "dashboard")
        self.btn_upload = self._make_button("Upload CSV", "upload")
        self.btn_charts = self._make_button("Charts", "charts")

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_charts)
        layout.addStretch()

    def _make_button(self, text: str, route: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.clicked.connect(lambda: self.route_changed.emit(route))
        return button

    def set_active(self, route: str) -> None:
        mapping = {
            "dashboard": self.btn_dashboard,
            "upload": self.btn_upload,
            "charts": self.btn_charts,
        }
        for key, button in mapping.items():
            button.setProperty("active", key == route)
            button.style().unpolish(button)
            button.style().polish(button)
