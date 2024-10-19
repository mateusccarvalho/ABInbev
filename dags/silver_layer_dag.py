from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
import os

# Define os paths
bronze_path = '/data/bronze'
silver_path = '/data/silver'

def processar_dados():
    spark = SparkSession.builder \
        .appName("silver_layer_dag") \
        .getOrCreate()

    # Listar todos os arquivos JSON na camada Bronze
    all_files = []
    for root, dirs, files in os.walk(bronze_path):
        for file in files:
            if file.endswith('.json'):
                all_files.append(os.path.join(root, file))

    if all_files:
        new_data_df = spark.read.json(all_files)

        new_data_df.write.partitionBy("brewery_type").parquet(silver_path, mode='overwrite')

    else:
        print("Nenhum arquivo JSON encontrado na camada Bronze.")

    # Parar a sessão do Spark
    spark.stop()

# Definir o DAG
default_args = {
    'owner': 'Mateus Carvalho',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('silver_layer_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    processar_dados_task = PythonOperator(task_id='processar_dados', python_callable=processar_dados)
