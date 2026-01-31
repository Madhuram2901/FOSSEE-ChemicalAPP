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

    def _create_scatter_plot(self, table_data):
        """Create a scatter plot for Pressure vs Temperature correlation"""
        pressures = [float(row.get('Pressure', 0)) for row in table_data]
        temps = [float(row.get('Temperature', 0)) for row in table_data]
        
        plt.figure(figsize=(6, 4))
        plt.scatter(pressures, temps, color='black', alpha=0.6)
        plt.xlabel('Pressure (bar)')
        plt.ylabel('Temperature (°C)')
        plt.title('Pressure-Temperature Correlation')
        plt.grid(True, linestyle='--', alpha=0.3)
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return Image(img_buffer, width=400, height=260)

    def generate(self, dataset):
        """Build the PDF document"""
        data = dataset.summary
        table_rows = data.get('table', [])
        
        # --- Header ---
        title = Paragraph("Chemical Process Analytical Report", self.styles['Header1'])
        self.elements.append(title)
        
        meta_info = [
            [Paragraph(f"<b>Dataset:</b> {dataset.original_filename or f'#{dataset.id}'}", self.styles['Normal']),
             Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Normal'])],
        ]
        t_meta = Table(meta_info, colWidths=[250, 250])
        t_meta.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT')]))
        self.elements.append(t_meta)
        self.elements.append(Spacer(1, 20))
        
        # --- AI Insights Section ---
        if 'ai_insights' in data:
            self.elements.append(Paragraph("Automated System Insights (powered by Gemini)", self.styles['Header2']))
            insights = data['ai_insights']
            if isinstance(insights, str):
                cleaned_insights = insights.replace('•', '<br/>•')
                self.elements.append(Paragraph(cleaned_insights, self.styles['Italic']))
            self.elements.append(Spacer(1, 15))

        # Risk, Stability and Correlation Calculations
        avg_p = float(data.get('averages', {}).get('pressure', 1))
        avg_t = float(data.get('averages', {}).get('temperature', 1))
        within_bounds = 0
        critical_assets = []
        
        # Pearson correlation calculation
        import math
        ps = [float(row.get('Pressure', 0)) for row in table_rows]
        ts = [float(row.get('Temperature', 0)) for row in table_rows]
        n = len(ps)
        corr_label = "N/A"
        
        if n > 1:
            try:
                sum_p = sum(ps)
                sum_t = sum(ts)
                sum_p2 = sum(p**2 for p in ps)
                sum_t2 = sum(t**2 for t in ts)
                sum_pt = sum(ps[i] * ts[i] for i in range(n))
                
                num = (n * sum_pt) - (sum_p * sum_t)
                den = math.sqrt((n * sum_p2 - sum_p**2) * (n * sum_t2 - sum_t**2))
                r = num / den if den != 0 else 0
                
                if abs(r) > 0.7: corr_label = "Strong"
                elif abs(r) > 0.4: corr_label = "Moderate"
                else: corr_label = "Weak"
            except:
                pass

        for row in table_rows:
            p = float(row.get('Pressure', 0))
            t = float(row.get('Temperature', 0))
            if p <= avg_p * 1.2 and t <= avg_t * 1.2:
                within_bounds += 1
            if p > avg_p * 1.5 or t > avg_t * 1.5:
                critical_assets.append([row.get('Equipment Name'), row.get('Type'), f"{p} bar", f"{t} °C", "CRITICAL"])
        
        stability_score = f"{(within_bounds / len(table_rows) * 100):.0f}%" if table_rows else "N/A"

        # --- Summary Section ---
        self.elements.append(Paragraph("Operational Summary", self.styles['Header2']))
        summary_data = [
            ["Metric", "Value / Global Average"],
            ["Total Equipment Count", str(data.get('total_equipment', 0))],
            ["System Stability Score", stability_score],
            ["P-T Correlation Strength", corr_label],
            ["System Mean Flowrate", f"{data.get('averages', {}).get('flowrate', 0)} m³/h"],
            ["System Mean Pressure", f"{data.get('averages', {}).get('pressure', 0)} bar"],
            ["System Mean Temperature", f"{data.get('averages', {}).get('temperature', 0)} °C"],
        ]
        
        t = Table(summary_data, colWidths=[250, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#000000')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9F9F9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 10))

        # --- Risk Assets ---
        if critical_assets:
            self.elements.append(Paragraph("⚠️ High-Risk Assets Detected", self.styles['Header2']))
            risk_table_data = [["Equipment", "Type", "Pressure", "Temp", "Status"]] + critical_assets[:10]
            t_risk = Table(risk_table_data, colWidths=[120, 100, 80, 80, 100])
            t_risk.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            self.elements.append(t_risk)
            self.elements.append(Spacer(1, 15))

        # --- Charts ---
        self.elements.append(Paragraph("Analytical Visualizations", self.styles['Header2']))
        if 'averages' in data:
            self.elements.append(self._create_bar_chart(data['averages']))
        if table_rows:
            self.elements.append(Spacer(1, 10))
            self.elements.append(self._create_scatter_plot(table_rows))
        
        distribution = data.get('type_distribution', {})
        if distribution:
            self.elements.append(Spacer(1, 20))
            self.elements.append(Paragraph("Equipment Distribution", self.styles['Header2']))
            self.elements.append(self._create_pie_chart(distribution))

        self.elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(name='Footer', parent=self.styles['Italic'], fontSize=8, textColor=colors.grey, alignment=1)
        self.elements.append(Paragraph("Confidential Process Report • Generated by Chemical Parameter Visualizer AI Engine", footer_style))
        
        self.doc.build(self.elements)

def generate_pdf_report(dataset):
    """Wrapper to create PDF buffer"""
    buffer = BytesIO()
    report = ReportGenerator(buffer)
    report.generate(dataset)
    buffer.seek(0)
    return buffer
