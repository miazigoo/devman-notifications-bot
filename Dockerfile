FROM python:3.10-slim as builder
WORKDIR /app
COPY . /app
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

CMD ["python", "script.py"]