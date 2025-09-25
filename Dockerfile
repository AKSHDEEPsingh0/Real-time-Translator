# Stage 1: Build dependencies and install system packages
FROM python:3.10-slim as builder

# Install system dependencies for PyAudio and Tesseract
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    tesseract-ocr-spa \
    tesseract-ocr-fra \
    tesseract-ocr-hin \
    tesseract-ocr-jpn \
    tesseract-ocr-mar \
    tesseract-ocr-tel \
    tesseract-ocr-tam \
    tesseract-ocr-ben \
    tesseract-ocr-ara \
    && rm -rf /var/lib/apt/lists/*

# Install Streamlit and other Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create a final, smaller image
FROM python:3.10-slim

# Copy the Tesseract OCR engine from the builder image
COPY --from=builder /usr/bin/tesseract /usr/bin/tesseract
COPY --from=builder /usr/share/tesseract-ocr /usr/share/tesseract-ocr

# Copy Python packages from the builder image
COPY --from=builder /app/ /app/
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application using the full path
CMD ["/usr/local/bin/python3", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
