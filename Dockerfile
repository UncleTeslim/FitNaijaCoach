# Use slim Python image for smaller size
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variables
ENV STREAMLIT_TELEMETRY_ENABLED=false \
    STREAMLIT_HEADLESS=true \
    OPENAI_API_KEY=${OPENAI_API_KEY}

# Expose the correct port (match your app)
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]
