from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class DashboardScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        header = QLabel("Dashboard")
        header.setObjectName("pageTitle")
        sub = QLabel("Overview of recent equipment analytics.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(12)
        cards = [
            ("Total Equipment", "120"),
            ("Avg Flowrate", "3.2"),
            ("Avg Pressure", "1.4"),
            ("Avg Temperature", "67.1"),
        ]
        for idx, (label, value) in enumerate(cards):
            card = self._summary_card(label, value)
            summary_grid.addWidget(card, 0, idx)

        layout.addLayout(summary_grid)

        chart_card = QFrame()
        chart_card.setObjectName("glassCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.addWidget(QLabel("Charts (Chart area placeholder)"))

        table_card = QFrame()
        table_card.setObjectName("glassCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.addWidget(QLabel("Latest uploads table (placeholder)"))

        layout.addWidget(chart_card)
        layout.addWidget(table_card)
        layout.addStretch()

    def _summary_card(self, label: str, value: str) -> QFrame:
        card = QFrame()
        card.setObjectName("glassCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(6)

        label_widget = QLabel(label)
        label_widget.setObjectName("cardLabel")
        value_widget = QLabel(value)
        value_widget.setObjectName("cardValue")

        card_layout.addWidget(label_widget)
        card_layout.addWidget(value_widget)
        return card
