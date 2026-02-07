from datetime import datetime

from PyQt5.QtWidgets import (
    QFrame,
    QFileDialog,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.api_client import client


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
        self.timeline_layout = QVBoxLayout(timeline)
        self.timeline_layout.setContentsMargins(22, 22, 22, 22)
        self.timeline_layout.setSpacing(16)

        self.empty_label = QLabel("No uploads yet. Upload a CSV to see history.")
        self.empty_label.setObjectName("historySubtitle")
        self.timeline_layout.addWidget(self.empty_label)

        layout.addWidget(timeline)
        layout.addStretch()

    def refresh(self) -> None:
        for idx in reversed(range(self.timeline_layout.count())):
            item = self.timeline_layout.itemAt(idx)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        try:
            data = client.fetch_summaries()
            uploads = data.get("results", [])
        except Exception:
            uploads = []

        if not uploads:
            self.empty_label = QLabel("No uploads yet. Upload a CSV to see history.")
            self.empty_label.setObjectName("historySubtitle")
            self.timeline_layout.addWidget(self.empty_label)
            return

        for upload in uploads:
            name = upload.get("name", "Dataset")
            uploaded_at = self._format_datetime(upload.get("uploaded_at"))
            upload_id = upload.get("id")
            row = self._history_row(
                "CSV Upload",
                f"{name} processed",
                uploaded_at,
                upload_id,
                name,
            )
            self.timeline_layout.addWidget(row)

    def _history_row(
        self,
        title: str,
        details: str,
        meta: str,
        upload_id: int | None,
        dataset_name: str,
    ) -> QFrame:
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

        row_layout.addStretch()

        if upload_id:
            download_btn = QPushButton("Download PDF")
            download_btn.setObjectName("historyAction")
            download_btn.clicked.connect(
                lambda _, uid=upload_id, name=dataset_name: self._download_report(uid, name)
            )
            row_layout.addWidget(download_btn)

        return row

    def _download_report(self, upload_id: int, name: str) -> None:
        suggested = f"{name or 'chemviz-report'}.pdf"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            suggested,
            "PDF Files (*.pdf)",
        )
        if not path:
            return
        try:
            content = client.fetch_report(upload_id)
            with open(path, "wb") as handle:
                handle.write(content)
            QMessageBox.information(self, "Download Complete", "PDF report saved.")
        except Exception:
            QMessageBox.critical(self, "Download Failed", "Unable to download PDF report.")

    def _format_datetime(self, value: str | None) -> str:
        if not value:
            return ""
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y - %H:%M")
        except ValueError:
            return value
