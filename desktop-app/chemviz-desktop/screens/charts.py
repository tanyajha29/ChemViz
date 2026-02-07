from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


class ChartsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.theme = "dark"
        self.metric = "Flowrate"
        self.latest_rows: list[dict] = []

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("pageScroll")
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        scroll.setWidget(container)
        root_layout.addWidget(scroll)

        header = QLabel("Charts")
        header.setObjectName("pageTitle")
        sub = QLabel("Advanced data visualization and analytics.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        grid = QGridLayout()
        grid.setSpacing(18)

        self.type_card = self._build_chart_card(
            "Equipment Type Distribution",
            "Counts per equipment category",
        )
        self.type_canvas = self._chart_canvas(240)
        self.type_card.layout().addWidget(self.type_canvas)

        self.avg_card = self._build_chart_card(
            "Average Metrics",
            "Flowrate, Pressure, Temperature",
        )
        self.avg_canvas = self._chart_canvas(240)
        self.avg_card.layout().addWidget(self.avg_canvas)

        grid.addWidget(self.type_card, 0, 0)
        grid.addWidget(self.avg_card, 0, 1)

        layout.addLayout(grid)

        self.deep_card = self._build_chart_card(
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
        self.deep_canvas = self._chart_canvas(280)
        deep_layout.addWidget(self.deep_canvas)
        layout.addWidget(self.deep_card)

        self.scatter_card = self._build_chart_card(
            "Pressure vs Temperature",
            "Scatter view of equipment metrics",
        )
        self.scatter_canvas = self._chart_canvas(280)
        self.scatter_card.layout().addWidget(self.scatter_canvas)
        layout.addWidget(self.scatter_card)
        layout.addStretch()

    def refresh(self) -> None:
        try:
            data = client.fetch_summaries()
            results = data.get("results", [])
            summary = results[0]["summary"] if results else {}
        except Exception:
            summary = {}

        type_dist = summary.get("type_distribution", {}) if summary else {}
        self._plot_type_distribution(type_dist)
        self._plot_averages(summary)

        try:
            latest = client.fetch_latest_rows()
            self.latest_rows = latest.get("rows", [])
        except Exception:
            self.latest_rows = []

        self._plot_deep_dive()
        self._plot_scatter()

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

    def _build_chart_card(self, title: str, subtitle: str) -> QFrame:
        card = QFrame()
        card.setObjectName("chartTile")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("tileTitle")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("tileSubtitle")
        subtitle_label.setWordWrap(True)

        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)
        return card

    def _chart_canvas(self, min_height: int = 240) -> FigureCanvas:
        fig = Figure(figsize=(4, 3))
        canvas = FigureCanvas(fig)
        canvas.setObjectName("chartCanvas")
        canvas.setMinimumHeight(min_height)
        canvas.setSizePolicy(
            canvas.sizePolicy().Expanding,
            canvas.sizePolicy().Expanding,
        )
        return canvas

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
        bars = ax.bar(labels, values, color="#3b82f6")
        for bar in bars:
            bar.set_alpha(0.8)
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
        ax.bar(labels, safe_values, color="#38bdf8")
        ax.set_title("Average Metrics")
        self.avg_canvas.draw()

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

    def _plot_scatter(self) -> None:
        fig = self.scatter_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        self._apply_matplotlib_style(ax)

        if not self.latest_rows:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.scatter_canvas.draw()
            return

        points = []
        for row in self.latest_rows:
            try:
                pressure = float(row.get("Pressure"))
                temperature = float(row.get("Temperature"))
            except (TypeError, ValueError):
                continue
            points.append((pressure, temperature))

        if not points:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color="#94a3b8")
            ax.set_xticks([])
            ax.set_yticks([])
            self.scatter_canvas.draw()
            return

        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        ax.scatter(x_vals, y_vals, color="#22d3ee", alpha=0.7)
        ax.set_title("Pressure vs Temperature")
        ax.set_xlabel("Pressure")
        ax.set_ylabel("Temperature")
        self.scatter_canvas.draw()
