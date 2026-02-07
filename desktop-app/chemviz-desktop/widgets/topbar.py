from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QStyle


class TopBar(QFrame):
    profile_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("topBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        title_block = QVBoxLayout()
        title_block.setSpacing(4)

        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("topBarTitle")

        self.subtitle_label = QLabel("Overview of recent equipment analytics.")
        self.subtitle_label.setObjectName("topBarSubtitle")

        title_block.addWidget(self.title_label)
        title_block.addWidget(self.subtitle_label)

        layout.addLayout(title_block)
        layout.addStretch()

        self.profile_button = QPushButton("Profile")
        self.profile_button.setObjectName("topBarButton")
        self.profile_button.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        self.profile_button.clicked.connect(self.profile_requested.emit)

        layout.addWidget(self.profile_button)

    def set_title(self, title: str, subtitle: str) -> None:
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
