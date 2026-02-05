from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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

        hint = QLabel("Drag & drop a CSV file here or click to browse.")
        hint.setObjectName("cardLabel")
        browse = QPushButton("Browse CSV")
        browse.setObjectName("primaryButton")

        checklist = QLabel(
            "Checklist:\n"
            "• Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature\n"
            "• Uploads stored: last 5 per user"
        )
        checklist.setObjectName("cardSubtitle")

        card_layout.addWidget(hint)
        card_layout.addWidget(browse)
        card_layout.addWidget(checklist)

        layout.addWidget(upload_card)
        layout.addStretch()
