import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_credit_memo_pdf(
    applicant_name,
    loan_type,
    requested_amount,
    approved_amount,
    interest_rate,
    tenure_months,
    dti_or_dscr_value,
    risk_level,
    approval_status,
    officer_notes
):
    """
    Generates a PDF Credit Approval Memo in memory and returns a BytesIO object.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # --- Custom Typography & Palette Styles ---
    primary_color = colors.HexColor("#296DAB")
    dark_slate = colors.HexColor("#1E293B")
    light_bg = colors.HexColor("#F8F9FA")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=dark_slate,
        leading=13
    )

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white
    )

    # --- Document Header ---
    story.append(Paragraph("CREDIT APPROVAL MEMORANDUM", title_style))
    story.append(Paragraph("CONFIDENTIAL | FINANCIAL RISK & CREDIT ANALYSIS DIVISION", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=15))

    # --- Summary Metadata Grid ---
    status_bg = colors.HexColor("#DCFCE7") if "Approved" in approval_status else colors.HexColor("#FEE2E2")
    status_text_color = colors.HexColor("#166534") if "Approved" in approval_status else colors.HexColor("#991B1B")

    summary_data = [
        [
            Paragraph("<b>Applicant / Entity:</b>", body_style), Paragraph(str(applicant_name), body_style),
            Paragraph("<b>Date:</b>", body_style), Paragraph("03 Aug 2026", body_style)
        ],
        [
            Paragraph("<b>Loan Type:</b>", body_style), Paragraph(str(loan_type), body_style),
            Paragraph("<b>Decision Status:</b>", body_style), Paragraph(f"<b>{approval_status}</b>", ParagraphStyle('Status', parent=body_style, textColor=status_text_color))
        ],
        [
            Paragraph("<b>Risk Rating:</b>", body_style), Paragraph(str(risk_level), body_style),
            Paragraph("<b>Primary Metric:</b>", body_style), Paragraph(str(dti_or_dscr_value), body_style)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[1.3*inch, 2.3*inch, 1.2*inch, 2.2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # --- Approved Financial Terms Table ---
    story.append(Paragraph("1. Approved Financial Structure", section_heading))
    
    terms_data = [
        [
            Paragraph("Requested Amount", header_cell_style),
            Paragraph("Approved Limit", header_cell_style),
            Paragraph("Interest Rate", header_cell_style),
            Paragraph("Tenure (Months)", header_cell_style)
        ],
        [
            Paragraph(f"฿{requested_amount:,.2f}", body_style),
            Paragraph(f"฿{approved_amount:,.2f}", body_style),
            Paragraph(f"{interest_rate:.2f}% p.a.", body_style),
            Paragraph(f"{tenure_months} Months", body_style)
        ]
    ]

    terms_table = Table(terms_data, colWidths=[1.75*inch, 1.75*inch, 1.75*inch, 1.75*inch])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
    ]))
    story.append(terms_table)
    story.append(Spacer(1, 15))

    # --- Credit Assessment & Justification ---
    story.append(Paragraph("2. Credit Officer Justification & Analysis Notes", section_heading))
    notes_paragraph = Paragraph(officer_notes.replace('\n', '<br/>'), body_style)
    notes_table = Table([[notes_paragraph]], colWidths=[7.0*inch])
    notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 25))

    # --- Signatures Block ---
    story.append(Paragraph("3. Signatures & Approvals", section_heading))
    story.append(Spacer(1, 10))

    sig_data = [
        [
            Paragraph("______________________________<br/><b>Credit Analyst</b><br/>Date: ____/____/________", body_style),
            Paragraph("______________________________<br/><b>Senior Risk Officer</b><br/>Date: ____/____/________", body_style),
            Paragraph("______________________________<br/><b>Managing Director</b><br/>Date: ____/____/________", body_style)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)

    # Build Document
    doc.build(story)
    buffer.seek(0)
    return buffer
