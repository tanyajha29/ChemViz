import sys
from PyQt5.QtWidgets import QApplication

from app.window import MainWindow

def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("ChemViz")

    window = MainWindow()
    window.apply_theme("dark")
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
