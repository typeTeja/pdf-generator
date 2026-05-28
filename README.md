# WeasyPrint PDF Microservice

A lightweight, production-ready Python FastAPI microservice to generate high-quality PDF documents using Jinja2 templates and WeasyPrint. This service is fully containerized using Docker, making it easy to deploy on any VPS, Coolify, or containerized platform with all system-level dependencies pre-configured.

---

## Project Structure

```text
testpdf/
├── app/
│   ├── main.py                  # FastAPI application with endpoints
│   ├── requirements.txt         # Package dependencies (copy)
│   ├── generated/               # Directory for temporary PDF files (auto-created)
│   ├── static/                  # Directory for static assets
│   └── templates/
│       └── offer_letter.html    # Jinja2 HTML template with print-optimized CSS
├── requirements.txt             # Package dependencies (root)
└── README.md                    # Installation, VPS Setup, & Troubleshooting
```

---

## 1. Local Development & Setup

### Prerequisites
Make sure you have Python 3.11+ installed.

### Step 1: Install System Libraries
WeasyPrint relies on Cairo, Pango, and GDK-PixBuf for rendering.
- **macOS (via Homebrew):**
  ```bash
  brew install cairo pango gdk-pixbuf libffi
  ```
- **Ubuntu/Debian:**
  Refer to [2. Ubuntu VPS Setup](#2-ubuntu-vps-setup) below.

### Step 2: Set up Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 2. Ubuntu VPS Setup (No Docker)

When deploying to a raw Ubuntu VPS or inside a Coolify environment running on the host (Nixpacks/Buildpacks), you **must** install WeasyPrint's system dependencies on the VPS itself.

### Step 1: Install Required System Packages
SSH into your VPS and execute:
```bash
sudo apt update
sudo apt install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libcairo2 \
    libglib2.0-0 \
    libffi-dev \
    shared-mime-info
```

### Step 2: Install Fonts (Optional but Highly Recommended)
By default, VPS servers contain very few fonts, which can result in WeasyPrint using generic fallbacks. Install standard fonts for clean rendering:
```bash
sudo apt install -y fonts-dejavu-core ttf-mscorefonts-installer fonts-liberation
# Refresh the font cache
sudo fc-cache -fv
```

---

## 3. Docker Deployment & Coolify Setup

This repository contains a pre-configured `Dockerfile` and `docker-compose.yml` to package all system libraries required by WeasyPrint (like Pango, Cairo, etc.) and system fonts.

### A. Local Execution with Docker Compose
To build and run the application locally inside Docker:
```bash
docker compose up --build -d
```
The API will be available at `http://localhost:8000`.

### B. Local Execution with Docker CLI
If you want to run it without compose:
```bash
# Build the image
docker build -t pdf-generator .

# Run the container
docker run -d -p 8000:8000 --name pdf-generator-container pdf-generator
```

### C. Coolify / VPS Docker Deployment
1. **Repository:** Link your Git repository in Coolify.
2. **Build Pack:** Select **Dockerfile**. Coolify will automatically detect the root `Dockerfile` and build the container image.
3. **Port:** Set the destination port to `8000`.
4. **Volume (Optional):** You can mount `/app/app/generated` to persist the generated PDF files on the host system.

---

## 4. Systemd Service Setup (For Manual VPS Deployment)

To keep your FastAPI app running in the background and ensure it automatically restarts on system reboot, configure a systemd service.

1. Create a service file:
   ```bash
   sudo nano /etc/systemd/system/pdf-microservice.service
   ```

2. Add the following content (adjust paths and user):
   ```ini
   [Unit]
   Description=FastAPI WeasyPrint PDF Microservice
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/testpdf
   ExecStart=/home/ubuntu/testpdf/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
   Restart=always
   Environment="PATH=/home/ubuntu/testpdf/venv/bin:/usr/local/bin:/usr/bin:/bin"

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start pdf-microservice.service
   sudo systemctl enable pdf-microservice.service
   ```

4. Check the status:
   ```bash
   sudo systemctl status pdf-microservice.service
   ```

---

## 5. Nginx Reverse Proxy Setup

To expose your microservice over HTTP/HTTPS with custom domain mapping, configure Nginx.

1. Create Nginx server block configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/pdf.example.com
   ```

2. Configuration Content:
   ```nginx
   server {
       listen 80;
       server_name pdf.example.com; # Replace with your sub/domain

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
           
           # Increase timeouts for large PDF rendering tasks
           proxy_read_timeout 90;
           proxy_connect_timeout 90;
           proxy_send_timeout 90;
       }
   }
   ```

3. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/pdf.example.com /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 6. Troubleshooting Guide

### A. Missing Cairo/Pango Libraries (`dlopen() failed`, `weasyprint.env.can_import`)
* **Symptom:** API fails at start, `/health` endpoint shows WeasyPrint status as `degraded` or `Unavailable`, or logs show `OSError: cannot load library 'gobject-2.0'` or `cannot load library 'libgobject-2.0-0'`.
* **Fix:** 
  1. For non-Docker deployments, make sure you ran `sudo apt install -y libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libcairo2 libglib2.0-0 libffi-dev shared-mime-info`.
  2. For Docker deployments, ensure that the Dockerfile successfully installs WeasyPrint's system dependencies. The provided Dockerfile does this automatically.

### B. Font Rendering Issues (Squares instead of letters, bad text spacing)
* **Symptom:** The generated PDF displays empty squares `[] [] []` instead of characters, or formatting is misaligned.
* **Fix:** 
  1. The server lacks unicode and system fonts. Install fonts: `sudo apt install -y fonts-dejavu-core fonts-liberation ttf-mscorefonts-installer`.
  2. In your HTML CSS, stick to robust cross-platform fonts: `font-family: system-ui, -apple-system, sans-serif` or load external fonts with absolute paths using standard `@font-face` if necessary.

### C. Permission Issues (`PermissionError: [Errno 13] Permission denied`)
* **Symptom:** Logs show WeasyPrint cannot write to `app/generated/`.
* **Fix:** 
  1. Ensure the user running the FastAPI daemon (`systemd` or Coolify worker) has write permission on the `app/generated` directory:
     ```bash
     sudo chown -R ubuntu:ubuntu /home/ubuntu/testpdf/app/generated
     chmod -R 775 /home/ubuntu/testpdf/app/generated
     ```

### D. Coolify Startup Failures
* **Symptom:** Coolify deploys successfully but logs show crash/loop restarts.
* **Fix:** Check if the host port `8000` is already in use by another app or container. In Coolify, modify the "App Port" field to an unused port if necessary, and ensure your Python application is starting on that same port.

### E. PDF Generation Errors (Jinja2 Template Errors or HTML syntax)
* **Symptom:** `/test-pdf` returns `500 Internal Server Error`.
* **Fix:**
  1. Check the logs generated by the FastAPI microservice.
  2. Ensure the template placeholders match the variables passed in `main.py` under the dictionary `data`.
  3. Validate that you are not loading external HTTP assets (like images or CSS files) inside WeasyPrint without permitting net access, or use base64 / inline SVGs instead.
