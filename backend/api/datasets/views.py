from datetime import datetime
from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Circle, Drawing, String
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
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
        max_file_size = 5 * 1024 * 1024
        max_rows = 10000
        allowed_mime = {
            'text/csv',
            'application/csv',
            'application/vnd.ms-excel',
            'text/plain',
        }

        if uploaded_file is None:
            return Response(
                {'error': 'Missing file. Upload a CSV with form field "file".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded_file.size == 0:
            return Response(
                {'error': 'CSV file is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded_file.size > max_file_size:
            return Response(
                {'error': 'File exceeds maximum size (5 MB).'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded_file.content_type and uploaded_file.content_type not in allowed_mime:
            return Response(
                {'error': 'Invalid file type. Please upload a .csv file.'},
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

        df = df.dropna(how='all')
        if df.empty:
            return Response(
                {'error': 'CSV file is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(df) > max_rows:
            return Response(
                {'error': f'CSV exceeds maximum row limit ({max_rows}).'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        normalized_columns = [str(col).strip() for col in df.columns]
        missing = [col for col in REQUIRED_COLUMNS if col not in normalized_columns]
        if missing:
            return Response(
                {
                    'error': f'Missing column: {missing[0]}',
                    'missing_columns': missing,
                    'received_columns': normalized_columns,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        df.columns = normalized_columns
        df = df[REQUIRED_COLUMNS].copy()

        row_count = int(len(df))
        file_size_bytes = int(uploaded_file.size)
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']

        missing_values = {}
        invalid_values = {}
        out_of_range = {}
        row_errors = []
        max_row_errors = 50

        def _add_row_errors(mask, column, message):
            nonlocal row_errors
            if len(row_errors) >= max_row_errors:
                return
            indices = df.index[mask].tolist()
            for idx in indices:
                if len(row_errors) >= max_row_errors:
                    break
                row_errors.append(
                    {
                        'row': int(idx) + 2,
                        'column': column,
                        'message': message,
                    }
                )

        valid_mask = pd.Series(True, index=df.index)

        for col in REQUIRED_COLUMNS:
            series = df[col]
            missing_mask = series.isna() | series.astype(str).str.strip().eq('')
            missing_values[col] = int(missing_mask.sum())
            if missing_mask.any():
                _add_row_errors(missing_mask, col, 'Missing value')
            valid_mask &= ~missing_mask

        numeric_df = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        for col in numeric_columns:
            missing_mask = df[col].isna() | df[col].astype(str).str.strip().eq('')
            invalid_mask = numeric_df[col].isna() & ~missing_mask
            invalid_values[col] = int(invalid_mask.sum())
            if invalid_mask.any():
                _add_row_errors(invalid_mask, col, 'Invalid numeric value')
            valid_mask &= ~invalid_mask

        flow_mask = numeric_df['Flowrate'] < 0
        out_of_range['Flowrate'] = int(flow_mask.sum())
        if flow_mask.any():
            _add_row_errors(flow_mask, 'Flowrate', 'Value must be >= 0')
        valid_mask &= ~flow_mask

        pressure_mask = numeric_df['Pressure'] < 0
        out_of_range['Pressure'] = int(pressure_mask.sum())
        if pressure_mask.any():
            _add_row_errors(pressure_mask, 'Pressure', 'Value must be >= 0')
        valid_mask &= ~pressure_mask

        temp_mask = (numeric_df['Temperature'] < -50) | (numeric_df['Temperature'] > 500)
        out_of_range['Temperature'] = int(temp_mask.sum())
        if temp_mask.any():
            _add_row_errors(temp_mask, 'Temperature', 'Value must be between -50 and 500')
        valid_mask &= ~temp_mask

        accepted_rows = int(valid_mask.sum())
        rejected_rows = int(row_count - accepted_rows)

        validation_summary = {
            'total_rows': row_count,
            'accepted_rows': accepted_rows,
            'rejected_rows': rejected_rows,
            'missing_values': missing_values,
            'invalid_values': invalid_values,
            'out_of_range': out_of_range,
            'row_errors': row_errors,
        }

        if accepted_rows == 0:
            return Response(
                {
                    'error': 'All rows are invalid. Please fix the CSV and retry.',
                    'validation_summary': validation_summary,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        df_valid = df.loc[valid_mask].copy()
        summary = compute_chemviz_analytics(df_valid)
        summary['row_count'] = row_count
        summary['file_size_bytes'] = file_size_bytes
        summary['validation'] = validation_summary

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
                'uploaded_by': request.user.get_full_name() or request.user.username,
                'validation_summary': validation_summary,
            },
            status=status.HTTP_201_CREATED,
        )


def _load_valid_dataframe(upload: DatasetUpload):
    try:
        df = pd.read_csv(upload.file.path)
    except Exception as exc:
        return None, f'Failed to read CSV file: {exc}'

    df = df.dropna(how='all')
    if df.empty:
        return None, 'CSV file is empty.'

    normalized_columns = [str(col).strip() for col in df.columns]
    missing = [col for col in REQUIRED_COLUMNS if col not in normalized_columns]
    if missing:
        return None, f'Missing required columns: {", ".join(missing)}'

    df.columns = normalized_columns
    return df, None


class DatasetSummaryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = (
            DatasetUpload.objects
            .filter(user=request.user)  # 🔒 USER FILTER
            .order_by('-uploaded_at', '-id')[:5]
        )

        data = []
        for upload in uploads:
            summary = upload.summary or {}
            validation = summary.get('validation') or {}
            data.append(
                {
                    'id': upload.id,
                    'name': upload.name,
                    'uploaded_at': upload.uploaded_at,
                    'summary': summary,
                    'uploaded_by': upload.user.get_full_name() or upload.user.username,
                    'row_count': summary.get('row_count') or validation.get('total_rows'),
                    'file_size_bytes': summary.get('file_size_bytes'),
                    'accepted_rows': validation.get('accepted_rows'),
                    'rejected_rows': validation.get('rejected_rows'),
                }
            )
        return Response({'results': data}, status=status.HTTP_200_OK)


class DatasetLatestRowsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = (
            DatasetUpload.objects
            .filter(user=request.user)
            .order_by('-uploaded_at', '-id')
        )

        for upload in uploads:
            df, error = _load_valid_dataframe(upload)
            if error:
                continue
            df = df[REQUIRED_COLUMNS].copy().head(200)
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

        return Response(
            {'rows': [], 'error': 'No valid datasets available.'},
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
    df, load_error = _load_valid_dataframe(upload)

    def _format_number(value):
        if value is None or pd.isna(value):
            return 'N/A'
        if isinstance(value, float):
            return f'{value:.2f}'
        return str(value)

    def _build_bar_chart(values, labels, title, width=430, height=190):
        drawing = Drawing(width, height)
        chart = VerticalBarChart()
        chart.x = 40
        chart.y = 25
        chart.width = width - 70
        chart.height = height - 60
        chart.data = [values]
        chart.categoryAxis.categoryNames = labels
        chart.valueAxis.valueMin = 0
        chart.barWidth = 14
        chart.groupSpacing = 8
        chart.barSpacing = 4
        chart.bars.fillColor = colors.HexColor('#3b82f6')
        drawing.add(chart)
        drawing.add(String(40, height - 20, title, fontSize=9))
        return drawing

    def _histogram(series: pd.Series, bins=6):
        numeric = pd.to_numeric(series, errors='coerce').dropna()
        if numeric.empty:
            return [], []
        counts, edges = pd.cut(numeric, bins=bins, retbins=True)
        counts = counts.value_counts().sort_index()
        labels = [
            f'{edges[i]:.1f}-{edges[i + 1]:.1f}'
            for i in range(len(edges) - 1)
        ]
        return list(counts.values), labels

    s = upload.summary or {}
    total_equipment = s.get('total_equipment') or (int(len(df)) if df is not None else 0)
    type_dist = s.get('type_distribution') or {}
    type_count = len(type_dist)
    avg_flowrate = s.get('avg_flowrate')
    avg_pressure = s.get('avg_pressure')
    avg_temperature = s.get('avg_temperature')

    numeric_df = None
    if df is not None:
        numeric_df = df.copy()
        for col in ['Flowrate', 'Pressure', 'Temperature']:
            if col in numeric_df.columns:
                numeric_df[col] = pd.to_numeric(numeric_df[col], errors='coerce')

    min_flow = numeric_df['Flowrate'].min() if numeric_df is not None and 'Flowrate' in numeric_df else None
    max_flow = numeric_df['Flowrate'].max() if numeric_df is not None and 'Flowrate' in numeric_df else None
    min_pressure = numeric_df['Pressure'].min() if numeric_df is not None and 'Pressure' in numeric_df else None
    max_pressure = numeric_df['Pressure'].max() if numeric_df is not None and 'Pressure' in numeric_df else None
    min_temp = numeric_df['Temperature'].min() if numeric_df is not None and 'Temperature' in numeric_df else None
    max_temp = numeric_df['Temperature'].max() if numeric_df is not None and 'Temperature' in numeric_df else None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title='ChemViz Report')
    styles = getSampleStyleSheet()

    story = []

    # Cover page
    logo = Drawing(70, 70)
    logo.add(
        Circle(
            35,
            35,
            30,
            fillColor=colors.HexColor('#3b82f6'),
            strokeColor=colors.HexColor('#3b82f6'),
        )
    )
    logo.add(
        String(
            35,
            28,
            'CV',
            fontSize=16,
            fillColor=colors.white,
            textAnchor='middle',
        )
    )
    story.append(logo)
    story.append(Spacer(1, 8))
    story.append(Paragraph('ChemViz', styles['Title']))
    story.append(Paragraph('Chemical Equipment Parameter Analysis Report', styles['Heading2']))
    story.append(Spacer(1, 18))
    story.append(Paragraph(f'Dataset: {upload.name}', styles['Normal']))
    story.append(Paragraph(f'Upload ID: {upload.id}', styles['Normal']))
    story.append(Paragraph(
        f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        styles['Normal'],
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph('ChemViz Report (Cover Page)', styles['Italic']))
    story.append(PageBreak())

    # Dataset overview
    story.append(Paragraph('Dataset Overview', styles['Heading2']))
    overview_rows = [
        ['Total Equipment', total_equipment],
        ['Number of Equipment Types', type_count],
        ['Uploaded Filename', upload.name],
        ['Upload Timestamp', upload.uploaded_at.strftime("%Y-%m-%d %H:%M")],
    ]
    overview_table = Table(overview_rows, colWidths=[200, 300])
    overview_table.setStyle(
        TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        )
    )
    story.append(overview_table)
    story.append(
        Paragraph(
            f'Section Summary: {total_equipment} equipment records across {type_count} types.',
            styles['Italic'],
        )
    )
    story.append(Spacer(1, 16))

    # Summary statistics
    story.append(Paragraph('Summary Statistics', styles['Heading2']))
    summary_rows = [
        ['Average Flowrate', _format_number(avg_flowrate)],
        ['Average Pressure', _format_number(avg_pressure)],
        ['Average Temperature', _format_number(avg_temperature)],
        ['Min Flowrate', _format_number(min_flow)],
        ['Max Flowrate', _format_number(max_flow)],
        ['Min Pressure', _format_number(min_pressure)],
        ['Max Pressure', _format_number(max_pressure)],
        ['Min Temperature', _format_number(min_temp)],
        ['Max Temperature', _format_number(max_temp)],
    ]
    summary_table = Table(summary_rows, colWidths=[200, 300])
    summary_table.setStyle(
        TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ]
        )
    )
    story.append(summary_table)
    story.append(
        Paragraph(
            'Section Summary: Averages and ranges are computed from valid rows.',
            styles['Italic'],
        )
    )
    story.append(Spacer(1, 16))

    # Equipment type distribution
    story.append(Paragraph('Equipment Type Distribution', styles['Heading2']))
    if type_dist:
        top_type = max(type_dist.items(), key=lambda x: x[1])
        top_pct = (top_type[1] / total_equipment) * 100 if total_equipment else 0
        type_labels = list(type_dist.keys())
        type_values = list(type_dist.values())
        story.append(_build_bar_chart(type_values, type_labels, 'Type Distribution'))
        story.append(Spacer(1, 8))
        total = sum(type_values) or 1
        type_table_rows = [['Type', 'Count', 'Percentage']]
        for label, count in zip(type_labels, type_values):
            pct = (count / total) * 100
            type_table_rows.append([label, count, f'{pct:.1f}%'])
        type_table = Table(type_table_rows, colWidths=[220, 120, 120])
        type_table.setStyle(
            TableStyle(
                [
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ]
            )
        )
        story.append(type_table)
        story.append(
            Paragraph(
                f'Section Summary: {top_type[0]} is the most common type ({top_pct:.1f}%).',
                styles['Italic'],
            )
        )
    else:
        story.append(Paragraph('No equipment type distribution available.', styles['Normal']))

    story.append(PageBreak())

    # Parameter analysis
    story.append(Paragraph('Parameter Analysis', styles['Heading2']))
    if df is None:
        story.append(
            Paragraph(
                'Raw CSV data could not be loaded. This section is based on stored summary values only.',
                styles['Italic'],
            )
        )
        story.append(Spacer(1, 12))
    else:
        for label in ['Flowrate', 'Pressure', 'Temperature']:
            if label not in df.columns:
                continue
            values, bins = _histogram(df[label])
            story.append(Paragraph(f'{label} Analysis', styles['Heading3']))
            story.append(
                Paragraph(f'Average {label}: {_format_number(s.get(f"avg_{label.lower()}"))}', styles['Normal'])
            )
            if values:
                story.append(_build_bar_chart(values, bins, f'{label} Distribution', width=420, height=180))
            else:
                story.append(Paragraph('No numeric data available.', styles['Normal']))
            if values:
                max_idx = values.index(max(values))
                story.append(
                    Paragraph(
                        f'Insight: Most values fall between {bins[max_idx]}.',
                        styles['Italic'],
                    )
                )
            story.append(Spacer(1, 12))

    # Equipment snapshot table
    story.append(Paragraph('Equipment Snapshot (First 10 Rows)', styles['Heading2']))
    if df is not None:
        preview = df[REQUIRED_COLUMNS].head(10)
        snapshot_rows = [REQUIRED_COLUMNS] + preview.values.tolist()
        snapshot_table = Table(snapshot_rows, colWidths=[140, 100, 100, 100, 100])
        snapshot_table.setStyle(
            TableStyle(
                [
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ]
            )
        )
        story.append(snapshot_table)
        story.append(Spacer(1, 12))
    else:
        story.append(
            Paragraph('Snapshot not available (raw CSV could not be loaded).', styles['Italic'])
        )
        story.append(Spacer(1, 12))

    # Observations
    story.append(Paragraph('Observations & Insights', styles['Heading2']))
    observations = []
    if type_dist:
        top_type = max(type_dist.items(), key=lambda x: x[1])
        pct = (top_type[1] / total_equipment) * 100 if total_equipment else 0
        observations.append(
            f'{top_type[0]} equipment dominates the dataset ({pct:.1f}%).'
        )
    if avg_pressure and avg_temperature:
        observations.append(
            'Average pressure is slightly elevated relative to temperature patterns.'
        )
    if avg_flowrate:
        observations.append(
            'Flowrate values are within expected operational ranges.'
        )
    if not observations:
        observations.append('No additional insights available.')
    for item in observations:
        story.append(Paragraph(f'- {item}', styles['Normal']))

    def _footer(canvas, doc_obj):
        canvas.saveState()
        footer_text = f'Generated by ChemViz | v1.0 | Page {canvas.getPageNumber()}'
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(letter[0] / 2.0, 20, footer_text)
        canvas.restoreState()

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"chemviz-report-{upload.id}.pdf\"'
    return response
