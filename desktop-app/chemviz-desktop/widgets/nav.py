from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStyle


class NavWidget(QFrame):
    route_changed = pyqtSignal(str)
    logout_requested = pyqtSignal()

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

        self.btn_dashboard = self._make_button(
            "Dashboard", "dashboard", QStyle.SP_DesktopIcon
        )
        self.btn_upload = self._make_button(
            "Upload CSV", "upload", QStyle.SP_ArrowUp
        )
        self.btn_charts = self._make_button(
            "Charts", "charts", QStyle.SP_FileDialogDetailedView
        )
        self.btn_history = self._make_button(
            "History", "history", QStyle.SP_BrowserReload
        )
        self.btn_profile = self._make_button(
            "Profile", "profile", QStyle.SP_DirHomeIcon
        )

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_charts)
        layout.addWidget(self.btn_history)
        layout.addWidget(self.btn_profile)
        layout.addStretch()

        footer = QFrame()
        footer.setObjectName("navFooter")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.logout_button.clicked.connect(self.logout_requested.emit)

        footer_layout.addWidget(self.logout_button)

        version_label = QLabel("ChemViz Analytics")
        version_label.setObjectName("navMeta")
        version_sub = QLabel("Version 2.4.0")
        version_sub.setObjectName("navMetaMuted")

        footer_layout.addWidget(version_label)
        footer_layout.addWidget(version_sub)

        layout.addWidget(footer)

    def _make_button(
        self, text: str, route: str, icon: QStyle.StandardPixmap
    ) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("navItem")
        button.setIcon(self.style().standardIcon(icon))
        button.clicked.connect(lambda: self.route_changed.emit(route))
        return button

    def set_active(self, route: str) -> None:
        mapping = {
            "dashboard": self.btn_dashboard,
            "upload": self.btn_upload,
            "charts": self.btn_charts,
            "history": self.btn_history,
            "profile": self.btn_profile,
        }
        for key, button in mapping.items():
            button.setProperty("active", key == route)
            button.style().unpolish(button)
            button.style().polish(button)
