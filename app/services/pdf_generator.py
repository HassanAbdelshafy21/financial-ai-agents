from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_financial_report(user_data: dict, chat_summary: str = "") -> bytes:
    """
    Generate a PDF financial report for a user.
    
    Args:
        user_data: Dict containing user info and financial data
        chat_summary: Summary of recent financial conversations
        
    Returns:
        bytes: PDF file content
    """
    # Create a BytesIO buffer for the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor='blue'
    )
    
    # Add title
    story.append(Paragraph("Financial Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Add user info
    story.append(Paragraph(f"Generated for: {user_data.get('name', 'User')}", styles['Normal']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Add financial summary section
    story.append(Paragraph("Financial Summary", styles['Heading2']))
    if user_data.get('monthly_income'):
        story.append(Paragraph(f"Monthly Income: ${user_data['monthly_income']:,.2f}", styles['Normal']))
    if user_data.get('monthly_expenses'):
        story.append(Paragraph(f"Monthly Expenses: ${user_data['monthly_expenses']:,.2f}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Add chat summary if provided
    if chat_summary:
        story.append(Paragraph("Recent Financial Conversations", styles['Heading2']))
        story.append(Paragraph(chat_summary, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Add recommendations section
    story.append(Paragraph("Recommendations", styles['Heading2']))
    story.append(Paragraph("• Review your budget monthly", styles['Normal']))
    story.append(Paragraph("• Build an emergency fund of 3-6 months expenses", styles['Normal']))
    story.append(Paragraph("• Consider increasing retirement contributions", styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content