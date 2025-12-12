FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create writable directory for SQLite
RUN mkdir -p /app/instance && chmod 777 /app/instance

EXPOSE 5000

# Set database path to writable location (note: 4 slashes for absolute path)
ENV DATABASE_URL=sqlite:////app/instance/alerts.db

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:flask_app", "--workers", "1"]