from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from services.api_client import client


class DashboardScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        header = QLabel("Dashboard")
        header.setObjectName("pageTitle")
        sub = QLabel("Overview of recent equipment analytics.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(16)
        self.summary_cards = {}
        labels = [
            "Total Equipment",
            "Avg Flowrate",
            "Avg Pressure",
            "Avg Temperature",
        ]
        for idx, label in enumerate(labels):
            card, value_widget = self._summary_card(label, "—")
            self.summary_cards[label] = value_widget
            summary_grid.addWidget(card, 0, idx)

        layout.addLayout(summary_grid)

        chart_card = QFrame()
        chart_card.setObjectName("glassCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_header = QLabel("Equipment Trends")
        chart_header.setObjectName("sectionHeader")
        chart_layout.addWidget(chart_header)
        chart_layout.addWidget(QLabel("Charts (Chart area placeholder)"))

        table_card = QFrame()
        table_card.setObjectName("glassCard")
        table_layout = QVBoxLayout(table_card)
        table_header = QLabel("Recent Uploads")
        table_header.setObjectName("sectionHeader")
        table_layout.addWidget(table_header)
        table_layout.addWidget(QLabel("Latest uploads table (placeholder)"))

        layout.addWidget(chart_card)
        layout.addWidget(table_card)
        layout.addStretch()

    def refresh(self) -> None:
        try:
            data = client.fetch_summaries()
            results = data.get("results", [])
            summary = results[0]["summary"] if results else {}
        except Exception:
            summary = {}

        mapping = {
            "Total Equipment": summary.get("total_equipment", "—"),
            "Avg Flowrate": summary.get("avg_flowrate", "—"),
            "Avg Pressure": summary.get("avg_pressure", "—"),
            "Avg Temperature": summary.get("avg_temperature", "—"),
        }
        for label, value in mapping.items():
            widget = self.summary_cards.get(label)
            if widget is not None:
                widget.setText(str(value))

    def _summary_card(self, label: str, value: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("kpiCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(6)

        label_widget = QLabel(label)
        label_widget.setObjectName("kpiLabel")
        value_widget = QLabel(value)
        value_widget.setObjectName("kpiValue")

        card_layout.addWidget(label_widget)
        card_layout.addWidget(value_widget)
        return card, value_widget
