FROM python:3.12-slim
RUN --mount=type=bind,source=requirements.txt,target=/opt/app/requirements.txt \
    pip install -r /opt/app/requirements.txt
COPY script.py /opt/app/

CMD ["python", "/opt/app/script.py"]

