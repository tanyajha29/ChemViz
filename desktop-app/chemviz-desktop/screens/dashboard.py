from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QStyle,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class DashboardScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.theme = "dark"
        self.metric = "Flowrate"
        self.latest_rows: list[dict] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(18)
        self.summary_cards = {}

        cards = [
            ("Total Equipment", "", "blue", QStyle.SP_FileDialogListView),
            ("Avg Flowrate", "L/s", "purple", QStyle.SP_ArrowUp),
            ("Avg Pressure", "bar", "orange", QStyle.SP_ArrowRight),
            ("Avg Temperature", "C", "green", QStyle.SP_DriveHDIcon),
            ("Datasets Stored", "", "blue", QStyle.SP_DirOpenIcon),
        ]

        columns = 3
        for idx, (label, unit, variant, icon) in enumerate(cards):
            card, value_widget = self._summary_card(
                label, unit, variant, icon
            )
            self.summary_cards[label] = (value_widget, unit)
            row = idx // columns
            col = idx % columns
            summary_grid.addWidget(card, row, col)

        layout.addLayout(summary_grid)

        charts_grid = QGridLayout()
        charts_grid.setSpacing(18)

        self.type_card = self._chart_card(
            "Equipment Type Distribution",
            "Counts per equipment category",
        )
        self.type_canvas = self._chart_canvas()
        self.type_card.layout().addWidget(self.type_canvas)

        self.avg_card = self._chart_card(
            "Average Parameters",
            "Flowrate, Pressure, Temperature",
        )
        self.avg_canvas = self._chart_canvas()
        self.avg_card.layout().addWidget(self.avg_canvas)

        charts_grid.addWidget(self.type_card, 0, 0)
        charts_grid.addWidget(self.avg_card, 0, 1)
        layout.addLayout(charts_grid)

        self.deep_card = self._chart_card(
            "Single Metric Deep Dive",
            "Flowrate, Pressure, or Temperature",
        )
        deep_layout = self.deep_card.layout()

        toggle_row = QHBoxLayout()
        toggle_row.setSpacing(10)

        self.btn_flow = self._metric_button("Flowrate")
        self.btn_pressure = self._metric_button("Pressure")
        self.btn_temp = self._metric_button("Temperature")

        toggle_row.addWidget(self.btn_flow)
        toggle_row.addWidget(self.btn_pressure)
        toggle_row.addWidget(self.btn_temp)
        toggle_row.addStretch()

        deep_layout.addLayout(toggle_row)

        self.deep_canvas = self._chart_canvas()
        deep_layout.addWidget(self.deep_canvas)

        layout.addWidget(self.deep_card)

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

        self.table_rows = table_rows

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
            results = []

        uploads = results
        mapping = {
            "Total Equipment": summary.get("total_equipment"),
            "Avg Flowrate": summary.get("avg_flowrate"),
            "Avg Pressure": summary.get("avg_pressure"),
            "Avg Temperature": summary.get("avg_temperature"),
            "Datasets Stored": len(uploads),
        }

        for label, raw_value in mapping.items():
            widget_unit = self.summary_cards.get(label)
            if not widget_unit:
                continue
            widget, unit = widget_unit
            widget.setText(self._format_value(raw_value, unit))

        type_dist = summary.get("type_distribution", {}) if summary else {}
        self._plot_type_distribution(type_dist)
        self._plot_averages(summary)
        self._render_table(uploads)

        try:
            latest = client.fetch_latest_rows()
            self.latest_rows = latest.get("rows", [])
        except Exception:
            self.latest_rows = []

        self._plot_deep_dive()

    def set_theme(self, theme: str) -> None:
        self.theme = theme
        self.refresh()

    def _metric_button(self, label: str) -> QPushButton:
        button = QPushButton(label)
        button.setObjectName("metricToggle")
        button.setProperty("active", label == self.metric)
        button.clicked.connect(lambda: self._set_metric(label))
        return button

    def _set_metric(self, label: str) -> None:
        self.metric = label
        for btn in (self.btn_flow, self.btn_pressure, self.btn_temp):
            btn.setProperty("active", btn.text() == label)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._plot_deep_dive()

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
        icon: QStyle.StandardPixmap,
    ) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("kpiCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(8)

        icon_frame = QFrame()
        icon_frame.setObjectName("kpiIcon")
        icon_frame.setProperty("variant", variant)
        icon_frame.setFixedSize(44, 44)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)

        icon_label = QLabel()
        icon_label.setObjectName("kpiIconGlyph")
        icon_label.setPixmap(self.style().standardIcon(icon).pixmap(22, 22))
        icon_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        label_widget = QLabel(label)
        label_widget.setObjectName("kpiLabel")
        value_widget = QLabel("--")
        value_widget.setObjectName("kpiValue")

        card_layout.addWidget(icon_frame)
        card_layout.addWidget(label_widget)
        card_layout.addWidget(value_widget)
        return card, value_widget

    def _chart_card(self, title: str, subtitle: str) -> QFrame:
        card = QFrame()
        card.setObjectName("sectionCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(12)

        chart_title = QLabel(title)
        chart_title.setObjectName("sectionTitle")
        chart_subtitle = QLabel(subtitle)
        chart_subtitle.setObjectName("sectionSubtitle")

        card_layout.addWidget(chart_title)
        card_layout.addWidget(chart_subtitle)
        return card

    def _chart_canvas(self) -> FigureCanvas:
        fig = Figure(figsize=(4, 3))
        return FigureCanvas(fig)

    def _apply_matplotlib_style(self, axes) -> None:
        fig = axes.figure
        if self.theme == "light":
            fig.patch.set_facecolor("#ffffff")
            axes.set_facecolor("#ffffff")
            axes.tick_params(colors="#334155")
            axes.title.set_color("#0f172a")
            axes.grid(color="#e2e8f0", alpha=0.6)
        else:
            fig.patch.set_facecolor("#0f172a")
            axes.set_facecolor("#0f172a")
            axes.tick_params(colors="#94a3b8")
            axes.title.set_color("#e2e8f0")
            axes.grid(color="#1f2937", alpha=0.6)

    def _plot_type_distribution(self, type_dist: dict) -> None:
        fig = self.type_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        self._apply_matplotlib_style(ax)

        if not type_dist:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.type_canvas.draw()
            return

        labels = list(type_dist.keys())
        values = list(type_dist.values())
        ax.bar(labels, values, color="#3b82f6", alpha=0.85)
        ax.set_ylabel("Count")
        ax.set_title("Equipment Type Distribution")
        ax.tick_params(axis="x", rotation=30)
        self.type_canvas.draw()

    def _plot_averages(self, summary: dict) -> None:
        fig = self.avg_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        self._apply_matplotlib_style(ax)

        labels = ["Flowrate", "Pressure", "Temperature"]
        values = [
            summary.get("avg_flowrate") if summary else None,
            summary.get("avg_pressure") if summary else None,
            summary.get("avg_temperature") if summary else None,
        ]
        if not any(v is not None for v in values):
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.avg_canvas.draw()
            return

        safe_values = [v if v is not None else 0 for v in values]
        ax.bar(labels, safe_values, color="#38bdf8", alpha=0.85)
        ax.set_title("Average Parameters")
        self.avg_canvas.draw()

    def _render_table(self, uploads: list[dict]) -> None:
        while self.table_rows.count() > 1:
            item = self.table_rows.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        if not uploads:
            empty_row = self._table_row(
                ["No uploads yet.", "", "", "", ""], status=None
            )
            self.table_rows.addWidget(empty_row)
            return

        for upload in uploads:
            name = upload.get("name", "Dataset")
            uploaded_at = self._format_datetime(upload.get("uploaded_at", ""))
            summary = upload.get("summary", {})
            total = summary.get("total_equipment", "--")
            status = "Completed"
            self.table_rows.addWidget(
                self._table_row(
                    [name, "Current User", uploaded_at, str(total), status],
                    status=status,
                )
            )

    def _format_datetime(self, value: str | None) -> str:
        if not value:
            return ""
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return value

    def _plot_deep_dive(self) -> None:
        fig = self.deep_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        self._apply_matplotlib_style(ax)

        if not self.latest_rows:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.deep_canvas.draw()
            return

        metric_key = self.metric
        values = []
        for row in self.latest_rows:
            name = row.get("Equipment Name", "Equipment")
            raw = row.get(metric_key)
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            values.append((name, value))

        if not values:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.deep_canvas.draw()
            return

        values = sorted(values, key=lambda item: item[1], reverse=True)[:15]
        labels = [item[0] for item in values]
        data = [item[1] for item in values]

        ax.bar(labels, data, color="#7c3aed", alpha=0.85)
        ax.set_title(f"{metric_key} (Top 15)")
        ax.tick_params(axis="x", rotation=30)
        self.deep_canvas.draw()

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
