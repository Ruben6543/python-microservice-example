FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p ../servicio_basico
COPY schema_municipio.json ../servicio_basico/

EXPOSE 5000

CMD ["python", "app.py"]