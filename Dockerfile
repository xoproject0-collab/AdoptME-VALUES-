FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN playwright install chromium

EXPOSE 10000

CMD ["python","app.py"]
