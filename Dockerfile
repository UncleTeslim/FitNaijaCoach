# Use slim Python image
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app


COPY requirements.txt . 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1

# Use environment-provided port on Render
ENV PORT=10000


EXPOSE $PORT

# Start the app using gunicorn for production (change app:app to match your entry point)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
