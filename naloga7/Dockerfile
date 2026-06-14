# Docker slika za spletno storitev naloge 7
FROM python:3.12-slim

WORKDIR /app

# namestitev odvisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# kopiranje aplikacije in serializiranih modelov
COPY app.py .
COPY models/ ./models/

EXPOSE 5000

# zagon storitve preko produkcijskega streznika
CMD ["python", "app.py"]
