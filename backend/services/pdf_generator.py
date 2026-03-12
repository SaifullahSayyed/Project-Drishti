import os
import io
import logging
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)

def generate_citizen_report(predict_response_dict: dict) -> io.BytesIO:
    """
    Generates a PDF report using ReportLab containing the predicted case details,
    the recommended pathway, bottlenecks, and the RAG-generated AI summary.
    """
    buffer = io.BytesIO()
    
    # Try to register a Unicode font if we wanted Hindi later, but for Hackathon English
    # reportlab has standard fonts built in.
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#0D47A1"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    h2_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#1565C0"),
        spaceBefore=15,
        spaceAfter=10
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    bold_style = ParagraphStyle(
        'BoldNorm',
        parent=normal_style,
        fontName='Helvetica-Bold'
    )

    story = []
    
    # 1. Header
    story.append(Paragraph("DRISHTI: AI Case Resolution Report", title_style))
    story.append(Paragraph(f"<b>For Case CNR:</b> {predict_response_dict.get('cnr')}", normal_style))
    story.append(Spacer(1, 20))
    
    # 2. Case Details Table
    case_data = predict_response_dict.get('case_data', {})
    data = [
        ['Case Type', case_data.get('case_type', 'N/A').title().replace('_', ' ')],
        ['Filing Year', str(case_data.get('filing_year', 'N/A'))],
        ['District', case_data.get('district', 'N/A')],
        ['Initial Est. Value', f"₹ {case_data.get('claim_value_inr', 0):,}"],
    ]
    
    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E3F2FD")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#BBDEFB")),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # 3. AI Summary
    story.append(Paragraph("1. Executive Summary", h2_style))
    summary_text = predict_response_dict.get('rag_summary', 'No summary available.')
    # ReportLab Paragraph needs HTML-like linebreaks for newlines
    summary_text = summary_text.replace('\n', '<br/>')
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 15))
    
    # 4. Prediction Stats
    story.append(Paragraph("2. Predictive Analytics", h2_style))
    outcome = predict_response_dict.get('outcome', {})
    
    pred_data = [
        ['Petitioner Win Probability', f"{outcome.get('petitioner_win_prob', 0)}%"],
        ['Estimated Resolution Time', f"{outcome.get('estimated_years', 0)} years"],
        ['Prediction Confidence', f"{outcome.get('confidence_score', 0)}%"],
        ['District Average for this case', f"{outcome.get('district_avg', 0)} years"]
    ]
    
    t2 = Table(pred_data, colWidths=[200, 250])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))
    
    # 5. Pathway Recommendation
    story.append(Paragraph("3. Recommended Pathway", h2_style))
    pathway = predict_response_dict.get('pathway', {})
    
    story.append(Paragraph(f"<b>Track:</b> {pathway.get('recommended', 'Standard Trial')}", normal_style))
    if pathway.get('cost_saving_inr', 0) > 0:
        story.append(Paragraph(f"<b>Estimated Fee Savings:</b> ₹ {pathway.get('cost_saving_inr'):,}", normal_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>How to Apply:</b> {pathway.get('how_to_apply', '')}", normal_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>Nearest Centre:</b> {pathway.get('nearest_centre', '')}", normal_style))
    story.append(Spacer(1, 15))
    
    # 6. Bottlenecks
    story.append(Paragraph("4. Key Litigation Bottlenecks to Avoid", h2_style))
    bottlenecks = predict_response_dict.get('bottlenecks', [])
    
    if bottlenecks:
        for b in bottlenecks:
            bullet = f"• <b>{b.get('name')}</b> (Severity: {b.get('severity').upper()})<br/>" \
                     f"&nbsp;&nbsp;<i>Risk:</i> Adds approx {b.get('avg_delay_months')} months delay.<br/>" \
                     f"&nbsp;&nbsp;<i>Mitigation:</i> {b.get('mitigation')}"
            story.append(Paragraph(bullet, normal_style))
            story.append(Spacer(1, 5))
    else:
         story.append(Paragraph("No major bottlenecks detected.", normal_style))
         
    # Disclaimer
    story.append(Spacer(1, 30))
    disclaimer = """<font size="8" color="#757575">
    DISCLAIMER: This report is generated by DRISHTI AI based on historical eCourts data and statistical modeling. 
    It is provided for informational and planning purposes only and does not constitute formal legal advice. 
    Resolution times and outcomes are probabilistic. Always consult a certified legal professional before taking legal action.
    </font>"""
    story.append(Paragraph(disclaimer, styles['Normal']))
    
    doc.build(story)
    
    buffer.seek(0)
    return buffer
