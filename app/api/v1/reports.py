from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.models import User
from app.services.pdf_generator import generate_financial_report
import io

router = APIRouter()

@router.post("/generate")
async def generate_report(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a PDF financial report for the current user."""
    
    # Gather user data (you can expand this with actual financial data from your database)
    user_data = {
        "name": current_user.full_name,
        "email": current_user.email,
        "monthly_income": 0,  # You'll replace this with real data later
        "monthly_expenses": 0,
    }
    
    # Generate the PDF
    pdf_content = generate_financial_report(user_data, "Sample chat summary")
    
    # Return the PDF as a downloadable file
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=financial_report.pdf"}
    )