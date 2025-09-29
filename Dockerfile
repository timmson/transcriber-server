FROM python:3.12

WORKDIR /app

COPY model /app/model
COPY requirements.txt /app/
RUN pip3 install --upgrade pip -r requirements.txt

COPY server.py /app/

ENTRYPOINT ["python3", "server.py"]
