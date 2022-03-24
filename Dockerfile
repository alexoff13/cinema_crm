FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y build-essential python3-dev python2.7-dev \
    git 

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app /app
COPY manage.py .
COPY initial_data.py .
COPY entrypoint.sh .
COPY .env .
CMD ["python3", "initial_data.py"]
ENTRYPOINT ["bash", "entrypoint.sh"]
