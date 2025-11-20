FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p ../servicio_demo
COPY schema_demo.json ../servicio_demo/

EXPOSE 5003

CMD ["python", "app.py"]