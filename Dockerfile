# ── Hassan Janjua's Task Board ──────────────────────────────
# Dockerfile for Flask Web Application
# Course: DevOps for Cloud Computing | COMSATS University
# ─────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
