import pandas as pd
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .analytics import REQUIRED_COLUMNS, compute_chemviz_analytics
from .models import DatasetUpload


class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        name = request.data.get('name')

        if uploaded_file is None:
            return Response(
                {'error': 'Missing file. Upload a CSV with form field "file".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not uploaded_file.name.lower().endswith('.csv'):
            return Response(
                {'error': 'Invalid file type. Please upload a .csv file.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)
        except Exception as exc:
            return Response(
                {'error': 'Failed to read CSV file.', 'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if df.empty:
            return Response(
                {'error': 'CSV file is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        normalized_columns = [str(col).strip() for col in df.columns]
        missing = [col for col in REQUIRED_COLUMNS if col not in normalized_columns]
        if missing:
            return Response(
                {
                    'error': 'Missing required columns.',
                    'missing_columns': missing,
                    'received_columns': normalized_columns,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = compute_chemviz_analytics(df)

        upload = DatasetUpload.objects.create(
            name=name or uploaded_file.name,
            file=uploaded_file,
            summary=summary,
        )

        return Response(
            {
                'id': upload.id,
                'name': upload.name,
                'uploaded_at': upload.uploaded_at,
                'summary': upload.summary,
            },
            status=status.HTTP_201_CREATED,
        )


class DatasetSummaryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = DatasetUpload.objects.order_by('-uploaded_at', '-id')[:5]
        data = [
            {
                'id': upload.id,
                'name': upload.name,
                'uploaded_at': upload.uploaded_at,
                'summary': upload.summary,
            }
            for upload in uploads
        ]
        return Response({'results': data}, status=status.HTTP_200_OK)
