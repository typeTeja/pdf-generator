Build a lightweight Python PDF microservice to test whether WeasyPrint works correctly after deployment on a VPS using Coolify WITHOUT Docker.

Requirements:

Tech Stack:

* Python 3.11
* FastAPI
* Uvicorn
* Jinja2
* WeasyPrint

Goal:
Verify PDF generation works correctly after deployment on Coolify VPS environment.

Features:

1. FastAPI server
2. Health check endpoint
3. PDF generation endpoint
4. Render HTML template using Jinja2
5. Generate PDF using WeasyPrint
6. Return downloadable PDF
7. Minimal production-ready structure
8. No database
9. No authentication
10. No Docker

Project Structure:

app/
├── main.py
├── requirements.txt
├── templates/
│   └── offer_letter.html
├── static/
└── generated/

Endpoints:

GET /health

Response:
{
"status": "ok"
}

GET /test-pdf

Requirements:

* Render sample admission offer letter
* Generate PDF using WeasyPrint
* Save temporarily in generated/
* Return PDF response

HTML Template should include:

* College name
* Student name
* Application number
* Fee structure table
* Principal signature placeholder
* Footer
* QR placeholder

Use clean HTML + CSS suitable for WeasyPrint.

Python Requirements:

* Use FastAPI
* Use Jinja2Templates
* Use HTML.write_pdf()
* Add proper exception handling
* Add logs for:

  * template rendering
  * PDF generation
  * file save path
  * errors

Generate:

1. main.py
2. requirements.txt
3. sample HTML template
4. folder structure
5. VPS setup instructions
6. Coolify deployment instructions
7. systemd service setup
8. Nginx reverse proxy config
9. troubleshooting section

Ubuntu VPS Requirements:
Include commands to install required system packages for WeasyPrint:

sudo apt update

sudo apt install -y 
libpango-1.0-0 
libpangoft2-1.0-0 
libharfbuzz0b 
libcairo2 
libffi-dev 
shared-mime-info

Python Install Steps:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run Command:

uvicorn app.main:app --host 0.0.0.0 --port 8000

Coolify Notes:

* Deploy as Python application
* Start command:
  uvicorn app.main:app --host 0.0.0.0 --port 8000
* Port: 8000

Add sample Nginx config:

server {
server_name pdf.example.com;

```
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

}

Add troubleshooting section for:

* missing cairo libraries
* font rendering issues
* permission issues
* Coolify startup failures
* PDF generation errors

Important:
Keep the project extremely small and simple.
Goal is ONLY to verify WeasyPrint works correctly after deployment.
