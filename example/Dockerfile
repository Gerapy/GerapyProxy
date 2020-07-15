FROM python:3.7

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python3 run.py