FROM python:3.11

WORKDIR /WhatsAPP
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8080"]
