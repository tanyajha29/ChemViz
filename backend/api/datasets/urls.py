from django.urls import path

from .views import (
    DatasetLatestReportView,
    DatasetLatestRowsView,
    DatasetReportView,
    DatasetSummaryListView,
    DatasetUploadView,
)

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('summary/', DatasetSummaryListView.as_view(), name='dataset-summary'),
    path('history/', DatasetSummaryListView.as_view(), name='dataset-history'),
    path('summaries/', DatasetSummaryListView.as_view(), name='dataset-summaries'),
    path('latest/', DatasetLatestRowsView.as_view(), name='dataset-latest'),
    path('report/<int:upload_id>/', DatasetReportView.as_view(), name='dataset-report'),
    path('report/pdf/', DatasetLatestReportView.as_view(), name='dataset-report-latest'),
]
