from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class DashboardScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        header_stack = QVBoxLayout()
        header_stack.setSpacing(6)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Overview of recent equipment analytics.")
        subtitle.setObjectName("pageSubtitle")

        header_stack.addWidget(title)
        header_stack.addWidget(subtitle)

        header_row.addLayout(header_stack)
        header_row.addStretch()

        preview_button = QPushButton("Preview")
        preview_button.setObjectName("ghostButton")
        header_row.addWidget(preview_button)

        layout.addLayout(header_row)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(18)
        self.summary_cards = {}

        cards = [
            ("Total Equipment", "", "blue", "+12.5% from last week", "up"),
            ("Avg Flowrate", "L/s", "purple", "+5.3% from last week", "up"),
            ("Avg Pressure", "bar", "orange", "-1.2% from last week", "down"),
            ("Avg Temperature", "C", "green", "+0.8% from last week", "up"),
        ]

        for idx, (label, unit, variant, delta, trend) in enumerate(cards):
            card, value_widget = self._summary_card(
                label, unit, variant, delta, trend
            )
            self.summary_cards[label] = (value_widget, unit)
            summary_grid.addWidget(card, 0, idx)

        layout.addLayout(summary_grid)

        chart_card = QFrame()
        chart_card.setObjectName("sectionCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(22, 22, 22, 22)
        chart_layout.setSpacing(12)

        chart_title = QLabel("Equipment Trends")
        chart_title.setObjectName("sectionTitle")
        chart_subtitle = QLabel("6-month performance overview")
        chart_subtitle.setObjectName("sectionSubtitle")

        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(chart_subtitle)

        chart_area = QFrame()
        chart_area.setObjectName("chartArea")
        chart_area_layout = QVBoxLayout(chart_area)
        chart_area_layout.setContentsMargins(16, 16, 16, 16)
        chart_area_layout.setSpacing(0)

        chart_placeholder = QLabel("Chart area")
        chart_placeholder.setObjectName("chartPlaceholder")
        chart_area_layout.addWidget(chart_placeholder)

        chart_layout.addWidget(chart_area)
        layout.addWidget(chart_card)

        table_card = QFrame()
        table_card.setObjectName("sectionCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(22, 22, 22, 22)
        table_layout.setSpacing(14)

        table_header = QLabel("Recent Uploads")
        table_header.setObjectName("sectionTitle")
        table_subtitle = QLabel("Latest CSV files processed")
        table_subtitle.setObjectName("sectionSubtitle")

        table_layout.addWidget(table_header)
        table_layout.addWidget(table_subtitle)

        table = QFrame()
        table.setObjectName("tableContainer")
        table_rows = QVBoxLayout(table)
        table_rows.setContentsMargins(0, 0, 0, 0)
        table_rows.setSpacing(0)

        table_rows.addWidget(
            self._table_row(
                ["Filename", "Uploaded By", "Date & Time", "Records", "Status"],
                header=True,
            )
        )

        uploads = [
            (
                "equipment_data_Q1_2026.csv",
                "Dr. Sarah Chen",
                "2026-02-05 14:32",
                "1,247",
                "Completed",
            ),
            (
                "flowrate_analysis_feb.csv",
                "Mark Thompson",
                "2026-02-04 09:15",
                "856",
                "Completed",
            ),
            (
                "pressure_sensors_jan.csv",
                "Dr. Emily Rodriguez",
                "2026-02-03 16:48",
                "2,103",
                "Completed",
            ),
            (
                "temperature_logs_weekly.csv",
                "James Liu",
                "2026-02-02 11:20",
                "645",
                "Processing",
            ),
        ]

        for filename, by, dt, records, status in uploads:
            table_rows.addWidget(
                self._table_row(
                    [filename, by, dt, records, status],
                    status=status,
                )
            )

        table_layout.addWidget(table)
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
            "Total Equipment": summary.get("total_equipment"),
            "Avg Flowrate": summary.get("avg_flowrate"),
            "Avg Pressure": summary.get("avg_pressure"),
            "Avg Temperature": summary.get("avg_temperature"),
        }

        for label, raw_value in mapping.items():
            widget_unit = self.summary_cards.get(label)
            if not widget_unit:
                continue
            widget, unit = widget_unit
            widget.setText(self._format_value(raw_value, unit))

    def _format_value(self, value: object, unit: str) -> str:
        if value in (None, "", "--"):
            return "--"
        try:
            num = float(value)
        except (TypeError, ValueError):
            return str(value)
        if unit:
            return f"{num:.2f} {unit}"
        return f"{num:.0f}"

    def _summary_card(
        self,
        label: str,
        unit: str,
        variant: str,
        delta: str,
        trend: str,
    ) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("kpiCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(8)

        icon = QFrame()
        icon.setObjectName("kpiIcon")
        icon.setProperty("variant", variant)
        icon.setFixedSize(44, 44)

        label_widget = QLabel(label)
        label_widget.setObjectName("kpiLabel")
        value_widget = QLabel("--")
        value_widget.setObjectName("kpiValue")
        delta_widget = QLabel(delta)
        delta_widget.setObjectName("kpiDelta")
        delta_widget.setProperty("trend", trend)

        card_layout.addWidget(icon)
        card_layout.addWidget(label_widget)
        card_layout.addWidget(value_widget)
        card_layout.addWidget(delta_widget)
        return card, value_widget

    def _table_row(
        self,
        values: list[str],
        header: bool = False,
        status: str | None = None,
    ) -> QFrame:
        row = QFrame()
        row.setObjectName("tableHeader" if header else "tableRow")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(16, 10, 16, 10)
        row_layout.setSpacing(12)

        for idx, value in enumerate(values):
            if header:
                label = QLabel(value)
                label.setObjectName("tableHeaderText")
                row_layout.addWidget(label, 1)
                continue

            if idx == len(values) - 1 and status:
                pill = QLabel(status)
                pill.setObjectName("statusPill")
                pill.setProperty("state", "success" if status == "Completed" else "warning")
                row_layout.addWidget(pill, 1)
                continue

            label = QLabel(value)
            label.setObjectName("tableCell")
            row_layout.addWidget(label, 1)

        return row
