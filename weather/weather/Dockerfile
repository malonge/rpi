FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade -r requirements.txt

COPY main.py /app/

CMD ["python3", "main.py"]
