# Use official Python image
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app

# Install dependencies early to leverage Docker caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Streamlit-specific: Disable telemetry and use headless mode
ENV STREAMLIT_TELEMETRY_ENABLED=false \
    STREAMLIT_HEADLESS=true

# Start Streamlit app
CMD ["run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
