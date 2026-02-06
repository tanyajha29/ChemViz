from PyQt5.QtWidgets import QFrame, QLabel, QGridLayout, QVBoxLayout, QWidget


class ChartsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        header = QLabel("Charts")
        header.setObjectName("pageTitle")
        sub = QLabel("Advanced data visualization and analytics.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        grid = QGridLayout()
        grid.setSpacing(18)

        cards = [
            ("Flow Distribution", "Equipment flowrate distribution analysis", "chart"),
            ("Pressure Correlation", "Pressure vs. temperature correlation", "trend"),
            ("Time Series Analysis", "Multi-variable temporal patterns", "chart"),
            ("Anomaly Detection", "Outlier identification and alerts", "trend"),
        ]

        for idx, (title, description, variant) in enumerate(cards):
            card = QFrame()
            card.setObjectName("chartTile")
            card.setProperty("variant", variant)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(10)

            icon = QFrame()
            icon.setObjectName("tileIcon")
            icon.setProperty("variant", variant)
            icon.setFixedSize(44, 44)

            title_label = QLabel(title)
            title_label.setObjectName("tileTitle")
            desc_label = QLabel(description)
            desc_label.setObjectName("tileSubtitle")
            desc_label.setWordWrap(True)

            card_layout.addWidget(icon)
            card_layout.addWidget(title_label)
            card_layout.addWidget(desc_label)
            card_layout.addStretch()

            row = idx // 2
            col = idx % 2
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()
