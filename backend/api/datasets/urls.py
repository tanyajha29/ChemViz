from django.urls import path

from .views import DatasetSummaryListView, DatasetUploadView

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('summaries/', DatasetSummaryListView.as_view(), name='dataset-summaries'),
]
