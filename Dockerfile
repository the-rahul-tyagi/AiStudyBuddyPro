# 1. Use a modern, supported Python base image (Debian 12 'Bookworm')
FROM python:3.11-slim-bookworm

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies required for pdfkit
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application files
COPY . .

# 6. Create a non-root user and grant permissions to the app directory
RUN useradd -m devopsuser && \
    chown -R devopsuser:devopsuser /app
USER devopsuser

# 7. Expose Streamlit's default port
EXPOSE 8501

# 8. Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]