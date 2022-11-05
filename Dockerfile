FROM python:3.10-alpine3.16
WORKDIR /opt/
COPY . .
CMD ["python3", "main.py"]