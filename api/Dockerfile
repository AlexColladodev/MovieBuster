FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV MONGO_URI="mongodb+srv://AlexColladodev:Alex-25-MovieBuster@moviebuster.lezf0.mongodb.net/?retryWrites=true&w=majority&appName=MovieBuster"

EXPOSE 5000

CMD ["python", "src/app.py"]
