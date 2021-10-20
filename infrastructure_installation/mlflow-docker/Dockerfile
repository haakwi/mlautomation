FROM python:3.8-buster

RUN mkdir /opt/mlflow

WORKDIR /opt/mlflow
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["mlflow", "server", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root","gs://mlopshhz", "--host","0.0.0.0"]