import json

import pandas as pd
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DatasetUpload

REQUIRED_COLUMNS = [
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature',
]


class DatasetUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

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

        numeric_summary = json.loads(df.describe(include='number').to_json())
        summary = {
            'row_count': int(len(df)),
            'column_count': int(len(df.columns)),
            'columns': normalized_columns,
            'numeric_summary': numeric_summary,
        }

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
