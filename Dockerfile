FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=10000


EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
