FROM python:3.11-bullseye

RUN mkdir -p /app
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
