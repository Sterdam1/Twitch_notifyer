FROM python:3.11.9-alpine

WORKDIR /app

COPY /app/requirements.txt ./

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY /app .

CMD ["python", "./main.py"]