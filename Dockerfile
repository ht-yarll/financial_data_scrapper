FROM astrocrpublic.azurecr.io/runtime:3.0-2

RUN pip install -r requirements.txt psycopg2-binary apache-airflow-providers-http