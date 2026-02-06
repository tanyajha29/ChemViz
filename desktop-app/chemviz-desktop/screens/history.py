from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class HistoryScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(26)

        header = QLabel("History")
        header.setObjectName("pageTitle")
        sub = QLabel("Review past analyses and data uploads.")
        sub.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(sub)

        timeline = QFrame()
        timeline.setObjectName("historyCard")
        timeline_layout = QVBoxLayout(timeline)
        timeline_layout.setContentsMargins(22, 22, 22, 22)
        timeline_layout.setSpacing(16)

        items = [
            ("CSV Upload", "equipment_data_Q1_2026.csv processed", "February 5, 2026 - 14:32"),
            ("Analysis Run", "Flowrate analysis completed for February data", "February 4, 2026 - 09:15"),
            ("CSV Upload", "pressure_sensors_jan.csv processed", "February 3, 2026 - 16:48"),
            ("Report Generated", "Monthly equipment performance report created", "February 2, 2026 - 11:20"),
        ]

        for title, details, meta in items:
            row = QFrame()
            row.setObjectName("historyItem")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(16, 12, 16, 12)
            row_layout.setSpacing(14)

            icon = QFrame()
            icon.setObjectName("historyIcon")
            icon.setFixedSize(40, 40)

            text_stack = QVBoxLayout()
            text_stack.setSpacing(4)

            title_label = QLabel(title)
            title_label.setObjectName("historyTitle")
            details_label = QLabel(details)
            details_label.setObjectName("historySubtitle")
            meta_label = QLabel(meta)
            meta_label.setObjectName("historyMeta")

            text_stack.addWidget(title_label)
            text_stack.addWidget(details_label)
            text_stack.addWidget(meta_label)

            row_layout.addWidget(icon)
            row_layout.addLayout(text_stack)
            timeline_layout.addWidget(row)

        layout.addWidget(timeline)
        layout.addStretch()
