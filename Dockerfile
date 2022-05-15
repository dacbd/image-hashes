FROM python:3.9-slim-buster

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENTRYPOINT [ "uvicorn" ]
CMD ["server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
