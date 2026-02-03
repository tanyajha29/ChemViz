from django.urls import path

from .views import DatasetReportView, DatasetSummaryListView, DatasetUploadView

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('summaries/', DatasetSummaryListView.as_view(), name='dataset-summaries'),
    path('report/<int:upload_id>/', DatasetReportView.as_view(), name='dataset-report'),
]
