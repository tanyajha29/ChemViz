from pathlib import Path

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from screens.charts import ChartsScreen
from screens.dashboard import DashboardScreen
from screens.history import HistoryScreen
from screens.login import LoginScreen
from screens.profile import ProfileScreen
from screens.upload import UploadScreen
from widgets.nav import NavWidget
from widgets.topbar import TopBar
from services.api_client import client


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ChemViz Desktop")
        self.resize(1360, 820)
        self.current_theme = "dark"

        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)

        self.login_screen = LoginScreen()
        self.login_screen.login_success.connect(self._on_login_success)

        self.dashboard_screen = DashboardScreen()
        self.upload_screen = UploadScreen()
        self.upload_screen.upload_success.connect(self._on_upload_success)
        self.charts_screen = ChartsScreen()
        self.history_screen = HistoryScreen()
        self.profile_screen = ProfileScreen()

        self.app_shell = self._build_shell()

        self.root_stack.addWidget(self.login_screen)
        self.root_stack.addWidget(self.app_shell)
        self.root_stack.setCurrentWidget(self.login_screen)

    def _build_shell(self) -> QWidget:
        shell = QWidget()
        layout = QHBoxLayout(shell)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        self.nav = NavWidget()
        self.nav.route_changed.connect(self._on_route_change)
        self.nav.theme_toggled.connect(self.toggle_theme)
        self.nav.logout_requested.connect(self._on_logout)

        self.top_bar = TopBar()
        self.top_bar.profile_requested.connect(lambda: self._on_route_change("profile"))

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.dashboard_screen)
        self.content_stack.addWidget(self.upload_screen)
        self.content_stack.addWidget(self.charts_screen)
        self.content_stack.addWidget(self.history_screen)
        self.content_stack.addWidget(self.profile_screen)

        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(18)
        content_layout.addWidget(self.top_bar)
        content_layout.addWidget(self.content_stack, stretch=1)

        layout.addWidget(self.nav)
        layout.addWidget(content_wrapper, stretch=1)
        return shell

    def _on_login_success(self) -> None:
        self.root_stack.setCurrentWidget(self.app_shell)
        self.nav.set_active("dashboard")
        self.content_stack.setCurrentWidget(self.dashboard_screen)
        self._set_topbar("Dashboard", "Overview of recent equipment analytics.")
        self.dashboard_screen.refresh()
        self.history_screen.refresh()
        self.charts_screen.refresh()
        self.profile_screen.refresh()
        self._animate_widget(self.content_stack.currentWidget())

    def _on_route_change(self, route: str) -> None:
        if route == "dashboard":
            self.content_stack.setCurrentWidget(self.dashboard_screen)
            self._set_topbar("Dashboard", "Overview of recent equipment analytics.")
        elif route == "upload":
            self.content_stack.setCurrentWidget(self.upload_screen)
            self._set_topbar("Upload CSV", "Import equipment data for analysis.")
        elif route == "charts":
            self.content_stack.setCurrentWidget(self.charts_screen)
            self._set_topbar("Charts", "Advanced data visualization and analytics.")
            self.charts_screen.refresh()
        elif route == "history":
            self.content_stack.setCurrentWidget(self.history_screen)
            self._set_topbar("History", "Review past analyses and data uploads.")
            self.history_screen.refresh()
        elif route == "profile":
            self.content_stack.setCurrentWidget(self.profile_screen)
            self._set_topbar("Profile", "Account details and session information.")
            self.profile_screen.refresh()

        self.nav.set_active(route)
        self._animate_widget(self.content_stack.currentWidget())

    def apply_theme(self, theme: str) -> None:
        base_dir = Path(__file__).resolve().parent.parent / "assets"
        styles_path = base_dir / (
            "styles.qss" if theme == "dark" else "styles-light.qss"
        )
        if styles_path.exists():
            app = QApplication.instance()
            if app:
                app.setStyleSheet(styles_path.read_text(encoding="utf-8"))
            self.current_theme = theme
            self.nav.set_theme_label(theme)
            self.charts_screen.set_theme(theme)

    def _on_upload_success(self) -> None:
        self.dashboard_screen.refresh()
        self.history_screen.refresh()
        self.charts_screen.refresh()

    def _on_logout(self) -> None:
        client.logout()
        self.root_stack.setCurrentWidget(self.login_screen)

    def _set_topbar(self, title: str, subtitle: str) -> None:
        self.top_bar.set_title(title, subtitle)

    def _animate_widget(self, widget: QWidget) -> None:
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(260)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start(QPropertyAnimation.DeleteWhenStopped)

    def toggle_theme(self) -> None:
        next_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(next_theme)
