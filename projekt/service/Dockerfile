# Docker slika za spletno storitev projektne naloge (napoved PM10)
FROM python:3.12-slim

WORKDIR /app

# namestitev odvisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# koda storitve, skupni modul za predprocesiranje in serializirani modeli
COPY app.py .
COPY prep_projekt.py .
COPY models/ ./models/

EXPOSE 5001

CMD ["python", "app.py"]
