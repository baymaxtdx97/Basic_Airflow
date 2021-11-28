from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

from datetime import datetime

args = {'start_date': datetime(2021,11,26), 'catchup': False, 'depend_on_past':False}

dag = DAG(
    dag_id='insertion_and_transfer',
    default_args=args, 
    schedule_interval="@daily"
    )


def transfer_data(table_name):
    src_request ="""SELECT * FROM {}""".format(table_name)
    src_pg_hook = PostgresHook(postgres_conn_id = 'postgres_default_project_x')
    src_connection = src_pg_hook.get_conn()
    src_cursor = src_connection.cursor()
    src_cursor.execute(src_request)
    results = src_cursor.fetchall()

    # Inserting Rows Now

    dest_pg_hook = PostgresHook(postgres_conn_id = 'postgres_default_project_y')
    dest_connection = dest_pg_hook.get_conn()
    dest_cursor = dest_connection.cursor()

    for result in results:
        request = """INSERT INTO {table} VALUES ({id},{value})""".format(table=table_name, id=result[0], value=result[1])
        dest_cursor.execute(request)
    
        dest_connection.commit()


with dag:

    table_x_insertion_task = PostgresOperator(
        task_id = "table_x_insertion",
        postgres_conn_id = "postgres_default_project_x",
        sql = 'sql/insert_values.sql')

    create_task = PythonOperator(task_id='transfer', python_callable=transfer_data, op_kwargs={'table_name': 'new_table'})
    
    table_x_insertion_task >> create_task

    
