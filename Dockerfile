FROM python:3.10-slim as builder
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
CMD ["python", "script.py"]

