"""
PDF Generation utilities
"""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import matplotlib.pyplot as plt
import io

class ReportGenerator:
    """Generates PDF reports for Equipment Datasets"""
    
    def __init__(self, buffer):
        self.buffer = buffer
        self.doc = SimpleDocTemplate(self.buffer, pagesize=letter)
        self.elements = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='Header1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='Header2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.black,
            spaceBefore=15,
            spaceAfter=10
        ))
    
    def _create_pie_chart(self, distribution):
        """Create a pie chart for equipment types"""
        labels = list(distribution.keys())
        sizes = list(distribution.values())
        
        plt.figure(figsize=(6, 4))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Equipment Distribution')
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return Image(img_buffer, width=400, height=260)

    def _create_bar_chart(self, averages):
        """Create a bar chart for average metrics"""
        metrics = ['Flowrate', 'Pressure', 'Temp']
        values = [averages.get('flowrate', 0), averages.get('pressure', 0), averages.get('temperature', 0)]
        
        plt.figure(figsize=(6, 4))
        plt.bar(metrics, values, color=['#3b82f6', '#10b981', '#f59e0b'])
        plt.ylabel('Value')
        plt.title('Average Metrics')
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return Image(img_buffer, width=400, height=260)

    def generate(self, dataset):
        """Build the PDF document"""
        data = dataset.summary
        
        # --- Header ---
        title = Paragraph("Chemical Equipment Parameter Visualizer", self.styles['Header1'])
        self.elements.append(title)
        
        meta_info = [
            [Paragraph(f"<b>Dataset ID:</b> {dataset.id}", self.styles['Normal'])],
            [Paragraph(f"<b>Uploaded At:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal'])],
            [Paragraph(f"<b>Generated At:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal'])],
        ]
        self.elements.append(Table(meta_info, hAlign='LEFT'))
        self.elements.append(Spacer(1, 20))
        
        # --- Summary Section ---
        self.elements.append(Paragraph("Dataset Summary", self.styles['Header2']))
        
        summary_data = [
            ["Metric", "Value"],
            ["Total Equipment", str(data.get('total_equipment', 0))],
            ["Average Flowrate", f"{data.get('averages', {}).get('flowrate', 0)} m³/h"],
            ["Average Pressure", f"{data.get('averages', {}).get('pressure', 0)} bar"],
            ["Average Temperature", f"{data.get('averages', {}).get('temperature', 0)} °C"],
        ]
        
        t = Table(summary_data, colWidths=[200, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#E0E0E0')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 10))

        # --- Metrics Chart ---
        if 'averages' in data:
            self.elements.append(self._create_bar_chart(data['averages']))
        self.elements.append(Spacer(1, 20))
        
        # --- Distribution Section ---
        self.elements.append(Paragraph("Equipment Type Distribution", self.styles['Header2']))
        
        dist_data = [["Equipment Type", "Count"]]
        distribution = data.get('type_distribution', {})
        for type_name, count in distribution.items():
            dist_data.append([type_name, str(count)])
            
        t_dist = Table(dist_data, colWidths=[200, 200])
        t_dist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#E0E0E0')),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        self.elements.append(t_dist)

        # --- Pie Chart ---
        if distribution:
            self.elements.append(self._create_pie_chart(distribution))

        self.elements.append(Spacer(1, 30))
        
        # --- Footer ---
        footer_text = Paragraph("Generated by Chemical Equipment Parameter Visualizer", self.styles['Italic'])
        self.elements.append(footer_text)
        
        # Build
        self.doc.build(self.elements)

def generate_pdf_report(dataset):
    """
    Wrapper to create PDF buffer
    """
    buffer = BytesIO()
    report = ReportGenerator(buffer)
    report.generate(dataset)
    buffer.seek(0)
    return buffer
