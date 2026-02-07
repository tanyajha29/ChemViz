from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
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
            user=request.user,  # 🔒 USER BINDING
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
        uploads = (
            DatasetUpload.objects
            .filter(user=request.user)  # 🔒 USER FILTER
            .order_by('-uploaded_at', '-id')[:5]
        )

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


class DatasetLatestRowsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        upload = (
            DatasetUpload.objects
            .filter(user=request.user)
            .order_by('-uploaded_at', '-id')
            .first()
        )
        if not upload:
            return Response({'rows': []}, status=status.HTTP_200_OK)

        try:
            df = pd.read_csv(upload.file.path)
        except Exception as exc:
            return Response(
                {'error': 'Failed to read CSV file.', 'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if df.empty:
            return Response({'rows': []}, status=status.HTTP_200_OK)

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

        df = df[REQUIRED_COLUMNS].copy()
        df = df.head(200)
        rows = df.to_dict(orient='records')

        return Response(
            {
                'id': upload.id,
                'name': upload.name,
                'uploaded_at': upload.uploaded_at,
                'rows': rows,
            },
            status=status.HTTP_200_OK,
        )


class DatasetReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, upload_id):
        try:
            upload = DatasetUpload.objects.get(
                id=upload_id,
                user=request.user  # 🔒 OWNER CHECK
            )
        except DatasetUpload.DoesNotExist:
            return Response(
                {'error': 'Dataset not found or access denied.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return _build_report_response(upload)


class DatasetLatestReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        upload = (
            DatasetUpload.objects
            .filter(user=request.user)
            .order_by('-uploaded_at', '-id')
            .first()
        )
        if not upload:
            return Response(
                {'error': 'No datasets available.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return _build_report_response(upload)


def _build_report_response(upload: DatasetUpload):
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
    s = upload.summary or {}
    summary_rows = [
        ['Total Equipment', s.get('total_equipment')],
        ['Average Flowrate', s.get('avg_flowrate')],
        ['Average Pressure', s.get('avg_pressure')],
        ['Average Temperature', s.get('avg_temperature')],
    ]

    table = Table(summary_rows, colWidths=[200, 300])
    table.setStyle(
        TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 16))

    type_dist = s.get('type_distribution') or {}
    if type_dist:
        story.append(Paragraph('Equipment Type Distribution', styles['Heading3']))
        drawing = Drawing(420, 220)
        chart = VerticalBarChart()
        chart.x = 40
        chart.y = 30
        chart.width = 360
        chart.height = 150
        chart.data = [list(type_dist.values())]
        chart.categoryAxis.categoryNames = list(type_dist.keys())
        chart.valueAxis.valueMin = 0
        chart.barWidth = 18
        chart.groupSpacing = 10
        chart.barSpacing = 4
        chart.bars.fillColor = colors.HexColor('#3b82f6')
        drawing.add(chart)
        drawing.add(String(40, 190, 'Equipment Type Distribution', fontSize=10))
        story.append(drawing)
    else:
        story.append(Paragraph('No equipment type distribution available.', styles['Normal']))

    doc.build(story)

    buffer.seek(0)
    response = Response(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="chemviz-report-{upload.id}.pdf"'
    return response
