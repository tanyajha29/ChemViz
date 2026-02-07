from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

from services.api_client import client


class UploadScreen(QWidget):
    upload_success = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        header = QLabel("Upload CSV")
        header.setObjectName("pageTitle")
        sub = QLabel("Import equipment data for analysis.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        upload_card = QFrame()
        upload_card.setObjectName("uploadCard")
        card_layout = QVBoxLayout(upload_card)
        card_layout.setContentsMargins(26, 26, 26, 26)
        card_layout.setSpacing(16)

        drop_zone = QFrame()
        drop_zone.setObjectName("uploadDrop")
        drop_layout = QVBoxLayout(drop_zone)
        drop_layout.setContentsMargins(24, 24, 24, 24)
        drop_layout.setSpacing(12)

        icon = QFrame()
        icon.setObjectName("uploadIcon")
        icon.setFixedSize(56, 56)

        hint = QLabel("Drag and drop your CSV file here")
        hint.setObjectName("cardTitle")
        hint.setAlignment(Qt.AlignCenter)

        sub_hint = QLabel("or click to browse from your computer")
        sub_hint.setObjectName("cardSubtitle")
        sub_hint.setAlignment(Qt.AlignCenter)

        browse = QPushButton("Select File")
        browse.setObjectName("primaryButton")
        browse.clicked.connect(self._browse_file)

        format_hint = QLabel("Supported format: CSV - Max file size: 100MB")
        format_hint.setObjectName("cardSubtitle")
        format_hint.setAlignment(Qt.AlignCenter)

        drop_layout.addWidget(icon, alignment=Qt.AlignCenter)
        drop_layout.addWidget(hint)
        drop_layout.addWidget(sub_hint)
        drop_layout.addWidget(browse, alignment=Qt.AlignCenter)
        drop_layout.addWidget(format_hint)

        self.file_label = QLabel("No file selected.")
        self.file_label.setObjectName("cardSubtitle")
        self.file_label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Upload")
        self.upload_button.setObjectName("primaryButton")
        self.upload_button.clicked.connect(self._upload_file)

        self.status_label = QLabel("")
        self.status_label.setObjectName("cardSubtitle")
        self.status_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(drop_zone)
        card_layout.addWidget(self.file_label)
        card_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.status_label)

        layout.addWidget(upload_card)

        info_grid = QGridLayout()
        info_grid.setSpacing(18)

        info_cards = [
            ("Required Columns", ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]),
            ("Data Format", ["ISO 8601 timestamps", "Numeric values only", "UTF-8 encoding"]),
            ("Best Practices", ["Validate data first", "Check for duplicates", "Use consistent units"]),
        ]

        for idx, (title, items) in enumerate(info_cards):
            card = QFrame()
            card.setObjectName("infoCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(10)

            header_row = QHBoxLayout()
            header_row.setSpacing(10)

            icon = QFrame()
            icon.setObjectName("infoIcon")
            icon.setFixedSize(36, 36)

            header_label = QLabel(title)
            header_label.setObjectName("cardTitle")

            header_row.addWidget(icon)
            header_row.addWidget(header_label)
            header_row.addStretch()

            card_layout.addLayout(header_row)

            for item in items:
                line = QLabel(f"- {item}")
                line.setObjectName("cardSubtitle")
                card_layout.addWidget(line)

            row = idx // 3
            col = idx % 3
            info_grid.addWidget(card, row, col)

        layout.addLayout(info_grid)
        layout.addStretch()

        self.file_path = ""

    def _browse_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if path:
            self.file_path = path
            self.file_label.setText(path)
            self.status_label.setText("")

    def _upload_file(self) -> None:
        if not self.file_path:
            self.status_label.setText("Please select a CSV file.")
            return
        self.status_label.setText("Uploading...")
        try:
            client.upload_csv(self.file_path, "")
            self.status_label.setText("Upload complete.")
            self.upload_success.emit()
        except Exception:
            self.status_label.setText("Upload failed. Check the CSV and try again.")
