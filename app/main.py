import os
import logging
import traceback
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("pdf_microservice")

app = FastAPI(
    title="WeasyPrint PDF Generation Microservice",
    description="A lightweight microservice to test and run WeasyPrint PDF generation on VPS/Coolify.",
    version="1.0.0"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
GENERATED_DIR = BASE_DIR / "generated"

# Ensure directories exist
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# Configure Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Lazy import WeasyPrint or verify it is installed and available
weasyprint_available = False
weasyprint_error_msg = ""
try:
    import weasyprint
    from weasyprint import HTML
    weasyprint_available = True
    logger.info("WeasyPrint successfully imported.")
except Exception as e:
    weasyprint_error_msg = f"{type(e).__name__}: {str(e)}"
    logger.error(f"Failed to import WeasyPrint. This usually means system libraries (libpango, libcairo, etc.) are missing. Error: {weasyprint_error_msg}")
    logger.error(traceback.format_exc())

@app.get("/")
def home(request: Request):
    """
    Serves the portal home page allowing users to enter a candidate name
    and download the generated PDF.
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify service status.
    Also returns whether WeasyPrint dependencies are loaded successfully.
    """
    status = "ok"
    details = {}
    if not weasyprint_available:
        status = "degraded"
        details["weasyprint"] = f"Unavailable. System libraries might be missing. Error: {weasyprint_error_msg}"
    else:
        details["weasyprint"] = "Available"
        
    return {
        "status": status,
        "details": details
    }

@app.get("/test-pdf")
def test_pdf(name: str = "Alex Mercer"):
    """
    Renders an admission offer letter template, converts it to PDF via WeasyPrint,
    saves the PDF to the generated/ directory, and serves it as a downloadable attachment.
    """
    if not weasyprint_available:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "WeasyPrint is not available on this host.",
                "reason": weasyprint_error_msg,
                "solution": "Please check that system libraries (libpango, libcairo, shared-mime-info, etc.) are installed on your VPS. Refer to README.md for instructions."
            }
        )

    # Mock dynamic data for rendering the offer letter
    data = {
        "college_name": "Antigravity Institute of Technology",
        "student_name": name,
        "application_number": "AIT-2026-77891",
        "course_name": "Master of Science in Agentic Systems Engineering",
        "academic_year": "2026-2027",
        "issue_date": "May 27, 2026",
        "admission_deadline": "June 15, 2026",
        "fees": [
            {"item": "Tuition Fee (Per Semester)", "amount": "$12,500.00"},
            {"item": "Laboratory & Research Fee", "amount": "$1,500.00"},
            {"item": "Student Services & Amenities Fee", "amount": "$600.00"},
            {"item": "Health Insurance & Welfare", "amount": "$400.00"}
        ],
        "total_fee": "$15,000.00"
    }

    try:
        # 1. Render HTML using Jinja2
        logger.info("Starting Jinja2 template rendering...")
        template_name = "offer_letter.html"
        
        # Verify template exists
        if not (TEMPLATES_DIR / template_name).exists():
            raise FileNotFoundError(f"Template file '{template_name}' not found in {TEMPLATES_DIR}")
            
        template = templates.env.get_template(template_name)
        html_content = template.render(data)
        logger.info("Jinja2 template rendering complete.")

        # 2. Define target PDF output path (sanitize name for filename safety)
        safe_name = "".join(c if c.isalnum() else "_" for c in name).strip("_")
        if not safe_name:
            safe_name = "applicant"
        pdf_filename = f"offer_letter_{safe_name}_{data['application_number']}.pdf"
        pdf_path = GENERATED_DIR / pdf_filename
        logger.info(f"Target PDF save path: {pdf_path}")

        # 3. Generate PDF using WeasyPrint
        logger.info("Starting WeasyPrint PDF generation...")
        
        # We set base_url so WeasyPrint can resolve paths relative to the app directory if needed.
        html_doc = HTML(string=html_content, base_url=str(BASE_DIR))
        html_doc.write_pdf(target=str(pdf_path))
        
        logger.info(f"WeasyPrint PDF generation complete. Saved file size: {os.path.getsize(pdf_path)} bytes")

        # 4. Return PDF FileResponse
        return FileResponse(
            path=str(pdf_path),
            filename=pdf_filename,
            media_type="application/pdf"
        )

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error occurred during PDF generation: {str(e)}")
        logger.error(error_details)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to generate PDF",
                "message": str(e),
                "traceback": error_details if app.debug else "Enable debug mode or inspect server logs for details."
            }
        )
