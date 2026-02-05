from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class ChartsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        header = QLabel("Charts")
        header.setObjectName("pageTitle")
        sub = QLabel("Visualize equipment distribution and averages.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        chart_card = QFrame()
        chart_card.setObjectName("glassCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.addWidget(QLabel("Matplotlib chart area (placeholder)"))

        layout.addWidget(chart_card)
        layout.addStretch()
