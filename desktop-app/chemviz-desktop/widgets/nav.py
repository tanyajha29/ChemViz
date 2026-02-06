from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


class NavWidget(QFrame):
    route_changed = pyqtSignal(str)
    theme_toggled = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("navPanel")
        self.setFixedWidth(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 22, 18, 22)
        layout.setSpacing(18)

        header = QFrame()
        header.setObjectName("navHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        logo = QFrame()
        logo.setObjectName("logoBadge")
        logo.setFixedSize(44, 44)

        logo_label = QLabel("CV")
        logo_label.setObjectName("logoGlyph")
        logo_layout = QHBoxLayout(logo)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        app_name = QLabel("ChemViz")
        app_name.setObjectName("appName")

        header_layout.addWidget(logo)
        header_layout.addWidget(app_name)
        header_layout.addStretch()

        layout.addWidget(header)

        self.btn_dashboard = self._make_button("Dashboard", "dashboard")
        self.btn_upload = self._make_button("Upload CSV", "upload")
        self.btn_charts = self._make_button("Charts", "charts")
        self.btn_history = self._make_button("History", "history")

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_charts)
        layout.addWidget(self.btn_history)
        layout.addStretch()

        footer = QFrame()
        footer.setObjectName("navFooter")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        self.theme_button = QPushButton("Switch to Light")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.theme_toggled.emit)

        footer_layout.addWidget(self.theme_button)

        version_label = QLabel("ChemViz Analytics")
        version_label.setObjectName("navMeta")
        version_sub = QLabel("Version 2.4.0")
        version_sub.setObjectName("navMetaMuted")

        footer_layout.addWidget(version_label)
        footer_layout.addWidget(version_sub)

        layout.addWidget(footer)

    def _make_button(self, text: str, route: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("navItem")
        button.clicked.connect(lambda: self.route_changed.emit(route))
        return button

    def set_active(self, route: str) -> None:
        mapping = {
            "dashboard": self.btn_dashboard,
            "upload": self.btn_upload,
            "charts": self.btn_charts,
            "history": self.btn_history,
        }
        for key, button in mapping.items():
            button.setProperty("active", key == route)
            button.style().unpolish(button)
            button.style().polish(button)

    def set_theme_label(self, theme: str) -> None:
        if theme == "dark":
            self.theme_button.setText("Switch to Light")
        else:
            self.theme_button.setText("Switch to Dark")
