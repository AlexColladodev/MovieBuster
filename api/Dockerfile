FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Configuración de la variable de entorno MONGO_URI
ENV MONGO_URI="mongodb://mongo-6-0-qxx.onrender.com:27017/MovieBuster?ssl=false"

EXPOSE 5000

CMD ["python", "src/app.py"]
