from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from screens.charts import ChartsScreen
from screens.dashboard import DashboardScreen
from screens.login import LoginScreen
from screens.upload import UploadScreen
from widgets.nav import NavWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ChemViz Desktop")
        self.resize(1200, 720)

        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)

        self.login_screen = LoginScreen()
        self.login_screen.login_success.connect(self._on_login_success)

        self.dashboard_screen = DashboardScreen()
        self.upload_screen = UploadScreen()
        self.charts_screen = ChartsScreen()

        self.app_shell = self._build_shell()

        self.root_stack.addWidget(self.login_screen)
        self.root_stack.addWidget(self.app_shell)
        self.root_stack.setCurrentWidget(self.login_screen)

    def _build_shell(self) -> QWidget:
        shell = QWidget()
        layout = QHBoxLayout(shell)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        self.nav = NavWidget()
        self.nav.route_changed.connect(self._on_route_change)

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.dashboard_screen)
        self.content_stack.addWidget(self.upload_screen)
        self.content_stack.addWidget(self.charts_screen)

        layout.addWidget(self.nav)
        layout.addWidget(self.content_stack, stretch=1)
        return shell

    def _on_login_success(self) -> None:
        self.root_stack.setCurrentWidget(self.app_shell)
        self.nav.set_active("dashboard")
        self.content_stack.setCurrentWidget(self.dashboard_screen)
        self.dashboard_screen.refresh()

    def _on_route_change(self, route: str) -> None:
        if route == "dashboard":
            self.content_stack.setCurrentWidget(self.dashboard_screen)
        elif route == "upload":
            self.content_stack.setCurrentWidget(self.upload_screen)
        elif route == "charts":
            self.content_stack.setCurrentWidget(self.charts_screen)
