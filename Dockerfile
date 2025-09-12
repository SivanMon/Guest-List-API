FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY guestlist-server.py ./guestlist-server.py
COPY index.html ./index.html

# Expose port
EXPOSE 1111

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:1111/health')" || exit 1

# Run the application
CMD ["python", "guestlist-server.py"]
