import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from app.window import MainWindow


def load_styles(app: QApplication) -> None:
    styles_path = Path(__file__).parent / "assets" / "styles.qss"
    if styles_path.exists():
        app.setStyleSheet(styles_path.read_text(encoding="utf-8"))


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("ChemViz")
    load_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
