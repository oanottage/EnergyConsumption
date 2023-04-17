from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/Users/oanottage/Desktop/BTS/BDI/Final_Project/Scripts')
import bronze_layer
import silver_layer


# Default arguments for the DAG starting April 8th, 2023 at 5:00 AM
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 8, 5, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Create ETL DAG
etl_dag = DAG(
  'etl',
  default_args=default_args,
  description='ETL API data into bronze and silver layers',
  schedule_interval=timedelta(days=1)
)

#Task to Collect Energy and Weather API data
bronze_task = PythonOperator(
task_id='bronze',
python_callable=bronze_layer.bronze,
dag=etl_dag)


#Task to Combine data into one table and store to database
silver_task = PythonOperator(
    task_id='silver',
    python_callable=silver_layer.silver,
    dag=etl_dag
)

bronze_task >> silver_task


