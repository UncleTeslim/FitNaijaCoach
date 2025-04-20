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

# Set environment variables directly through Hugging Face's interface, 
# don't specify OPENAI_API_KEY here since it's handled by Hugging Face
ENV STREAMLIT_TELEMETRY_ENABLED=false \
    STREAMLIT_HEADLESS=true

# Expose the correct port (Streamlit usually uses 8501)
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
