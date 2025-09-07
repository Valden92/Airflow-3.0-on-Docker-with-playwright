
import logging
from datetime import datetime
from importlib import import_module

from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
    dag_id="playwright_crawler",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    def run_playwright_crawler():
        main_module = import_module(f"crawlers.playwright.my_crawler.main")
        logging.info('Run crawler from DAG...')
        main_module.main()
        logging.info('Close task work.')


    time_task = PythonOperator(
        task_id='run_playwright_crawler',
        python_callable=run_playwright_crawler,
        dag=dag,
    )

    time_task