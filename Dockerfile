FROM python:3.11

WORKDIR /python-whatsapp-bot-main

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80ts

CMD ["python", "run.py"]
