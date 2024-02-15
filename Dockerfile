FROM python:3.10-slim
RUN --mount=type=bind,source=requirements.txt,target=/opt/app/requirements.txt \
    pip install -r /opt/app/requirements.txt
COPY . /opt/app
CMD ["python", "script.py"]

