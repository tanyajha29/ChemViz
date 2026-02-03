from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
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


class DatasetReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, upload_id):
        try:
            upload = DatasetUpload.objects.get(id=upload_id)
        except DatasetUpload.DoesNotExist:
            return Response(
                {'error': 'Dataset upload not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            df = pd.read_csv(upload.file.path)
        except Exception as exc:
            return Response(
                {'error': 'Failed to read CSV file.', 'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title='ChemViz Report')
        styles = getSampleStyleSheet()

        story = []
        story.append(Paragraph('ChemViz Report', styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f'Dataset: {upload.name}', styles['Heading2']))
        story.append(Paragraph(f'Uploaded: {upload.uploaded_at}', styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph('Summary Statistics', styles['Heading3']))
        summary_items = upload.summary or {}
        summary_rows = [
            ['Total Equipment', summary_items.get('total_equipment')],
            ['Average Flowrate', summary_items.get('avg_flowrate')],
            ['Average Pressure', summary_items.get('avg_pressure')],
            ['Average Temperature', summary_items.get('avg_temperature')],
        ]
        summary_table = Table(summary_rows, colWidths=[200, 300])
        summary_table.setStyle(
            TableStyle(
                [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
            )
        )
        story.append(summary_table)
        story.append(Spacer(1, 16))

        story.append(Paragraph('Equipment Data (First 25 Rows)', styles['Heading3']))
        columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        existing_columns = [col for col in columns if col in df.columns]
        preview = df[existing_columns].head(25)

        table_data = [existing_columns] + preview.fillna('').values.tolist()
        data_table = Table(table_data, repeatRows=1)
        data_table.setStyle(
            TableStyle(
                [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECECEC')),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]
            )
        )
        story.append(data_table)

        doc.build(story)
        buffer.seek(0)

        response = Response(
            buffer.getvalue(),
            status=status.HTTP_200_OK,
            content_type='application/pdf',
        )
        response['Content-Disposition'] = f'attachment; filename="chemviz-report-{upload_id}.pdf"'
        return response
