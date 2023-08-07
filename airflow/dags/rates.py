"""
### DAG documentation
This is a simple ETL data pipeline example which extract rates data from API
and load in into postgresql
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.hooks.base import BaseHook

import requests
import psycopg2
import decimal
from time import localtime, strftime
from datetime import datetime


default_args = {
    "owner": "airflow",
    'start_date': days_ago(1)
}

variables = Variable.set(key="currency_load_variables",
                         value={"table_name": "rates",
                                "rate_base": "BTC",
                                "rate_target": "RUB",
                                "connection_name": "db_conn",
                                "url_base": "https://api.exchangerate.host/"},
                         serialize_json=True)
dag_variables = Variable.get("currency_load_variables", deserialize_json=True)


def get_conn_credentials(conn_id) -> BaseHook.get_connection:
    """
    Function returns dictionary with connection credentials

    :param conn_id: str with airflow connection id
    :return: Connection
    """
    conn = BaseHook.get_connection(conn_id)
    return conn


def import_codes(**kwargs):
    hist_date = "latest"
    url = dag_variables.get('url_base') + hist_date
    ingest_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    try:
        response = requests.get(url, params={'base': dag_variables.get('rate_base')})
    except Exception as err:
        print(f'Error occurred: {err}')
        return
    data = response.json()
    rate_date = data['date']
    value_ = str(decimal.Decimal(data['rates']['RUB']))[:20]

    ti = kwargs['ti']
    ti.xcom_push(key='results', value={"rate_date": rate_date, "value_": value_, "ingest_datetime": ingest_datetime})


def insert_data(**kwargs):
    task_instance = kwargs['task_instance']
    results = task_instance.xcom_pull(key='results', task_ids='import_rates')

    print("rate_date: ", results["rate_date"])
    print("value_: ", results["value_"])

    ingest_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    pg_conn = get_conn_credentials(dag_variables.get('connection_name'))
    pg_hostname, pg_port, pg_username, pg_pass, pg_db = pg_conn.host, pg_conn.port, pg_conn.login, pg_conn.password, pg_conn.schema
    conn = psycopg2.connect(host=pg_hostname, port=pg_port, user=pg_username, password=pg_pass, database=pg_db)

    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {dag_variables.get('table_name')} (ingest_datetime, rate_date, rate_base, "
                   f"rate_target,value_ ) VALUES('{ingest_datetime}','{results['rate_date']}', "
                   f"'{dag_variables.get('rate_base')}', '{dag_variables.get('rate_target')}', "
                   f"'{results['value_']}');")
    conn.commit()

    cursor.close()
    conn.close()


with DAG(dag_id="parsing-dag", schedule_interval="*/10 * * * *",
         default_args=default_args, tags=["1T", "test"], catchup=False) as dag:
    dag.doc_md = __doc__

    hello_bash_task = BashOperator(task_id='bash_task',
                                   bash_command="echo 'Good morning my diggers!'")

    import_rates_from_api = PythonOperator(task_id='import_rates',
                                           python_callable=import_codes)

    insert_rates_to_pg = PythonOperator(task_id='insert_data',
                                        python_callable=insert_data)

hello_bash_task >> import_rates_from_api >> insert_rates_to_pg


