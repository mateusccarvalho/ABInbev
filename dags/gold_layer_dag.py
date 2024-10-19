from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession

# Define os paths
silver_path = '/data/silver'
gold_path = '/data/gold' 

def processar_dados_gold():
    spark = SparkSession.builder \
        .appName("gold_layer_dag") \
        .getOrCreate()

    # Ler os dados da camada Silver
    silver_df = spark.read.parquet(silver_path)

    # Agregar a quantidade de cervejarias por tipo e cidade
    aggregated_df = silver_df.groupBy("brewery_type", "city").count()

    # Salvar os dados agregados na camada Gold em formato Parquet
    aggregated_df.write.parquet(gold_path, mode='overwrite')

    # Parar a sessão do Spark
    spark.stop()

# Definir o DAG
default_args = {
    'owner': 'Mateus Carvalho',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('gold_layer_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    processar_dados_gold_task = PythonOperator(
        task_id='processar_dados_gold',
        python_callable=processar_dados_gold
    )
