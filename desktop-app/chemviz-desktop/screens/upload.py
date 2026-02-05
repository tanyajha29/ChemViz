from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class UploadScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        header = QLabel("Upload CSV")
        header.setObjectName("pageTitle")
        sub = QLabel("Upload datasets to generate analytics and reports.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        upload_card = QFrame()
        upload_card.setObjectName("glassCard")
        card_layout = QVBoxLayout(upload_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Dataset name (optional)")

        hint = QLabel("Drag & drop a CSV file here or click to browse.")
        hint.setObjectName("cardLabel")
        browse = QPushButton("Browse CSV")
        browse.setObjectName("primaryButton")
        browse.clicked.connect(self._browse_file)

        self.file_label = QLabel("No file selected.")
        self.file_label.setObjectName("cardSubtitle")

        self.upload_button = QPushButton("Upload")
        self.upload_button.setObjectName("primaryButton")
        self.upload_button.clicked.connect(self._upload_file)

        self.status_label = QLabel("")
        self.status_label.setObjectName("cardSubtitle")

        checklist = QLabel(
            "Checklist:\n"
            "• Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature\n"
            "• Uploads stored: last 5 per user"
        )
        checklist.setObjectName("cardSubtitle")

        card_layout.addWidget(self.name_input)
        card_layout.addWidget(hint)
        card_layout.addWidget(browse)
        card_layout.addWidget(self.file_label)
        card_layout.addWidget(self.upload_button)
        card_layout.addWidget(self.status_label)
        card_layout.addWidget(checklist)

        layout.addWidget(upload_card)
        layout.addStretch()

        self.file_path = ""

    def _browse_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if path:
            self.file_path = path
            self.file_label.setText(path)

    def _upload_file(self) -> None:
        if not self.file_path:
            self.status_label.setText("Please select a CSV file.")
            return
        self.status_label.setText("Uploading...")
        try:
            client.upload_csv(self.file_path, self.name_input.text().strip())
            self.status_label.setText("Upload complete.")
        except Exception:
            self.status_label.setText("Upload failed. Check the CSV and try again.")
