from pyspark.sql.types import DateType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, lit, when
from pyspark.sql.utils import AnalysisException
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import os
from datetime import datetime

# Define o path base para a Bronze (sem a parte do diretório de data)
bronze_base_path = '/data/bronze'
# Define o path para a Silver
silver_path = '/data/silver'

def get_latest_bronze_dir(base_path):
    # Lista os diretórios de ano
    years = sorted([d for d in os.listdir(base_path) if d.isdigit()], reverse=True)
    if not years:
        raise ValueError(f"Nenhum diretório de ano encontrado em {base_path}")
    
    # Percorre o ano mais recente
    for year in years:
        year_path = os.path.join(base_path, year)
        months = sorted([d for d in os.listdir(year_path) if d.isdigit()], reverse=True)
        if not months:
            continue  
        
        # Percorre o mês mais recente
        for month in months:
            month_path = os.path.join(year_path, month)
            days = sorted([d for d in os.listdir(month_path) if d.isdigit()], reverse=True)
            if not days:
                continue  
            
            # Retorna o caminho do último dia encontrado
            latest_day = days[0]
            return os.path.join(month_path, latest_day)

    raise ValueError("Nenhum diretório válido encontrado")

def processar_dados_silver():
    # Inicializa SparkSession
    spark = SparkSession.builder \
        .appName('silver_layer_dag') \
        .getOrCreate()
    
    # Tenta carregar os dados da camada Silver Caso não exista, cria a partir da Bronze
    try:
        df_silver = spark.read.parquet(silver_path)
    except AnalysisException:  
        df_silver = None

    # Identificar o caminho mais recente na Bronze
    latest_bronze_path = get_latest_bronze_dir(bronze_base_path)

    # Verifica se Silver é None
    if df_silver is None:
        # Lê dados da camada Bronze a partir do diretório mais recente
        df_bronze = spark.read.json(latest_bronze_path)
        
        # Adiciona colunas de data
        df_bronze = df_bronze.withColumn('insert_date', current_date())
        df_bronze = df_bronze.withColumn('update_date', lit(None).cast(DateType()))

        # Salva o DF Bronze como Silver (Parquet) 
        df_bronze.write.mode('overwrite').parquet(silver_path)
        print(f"Dados da Bronze ({latest_bronze_path}) salvos na Silver.")
    
    else:
        # Lê os dados da Bronze a partir do último diretório
        df_bronze = spark.read.json(latest_bronze_path)

        # Realiza o merge entre os dados da Bronze e Silver
        df_merged = df_silver.alias('old').join(df_bronze.alias('new'), ['id'], 'outer')

        # Condição para identificar se os dados foram atualizados
        update_condition = (col('old.name') != col('new.name')) | col('new.name').isNotNull()

        # Define a lógica para 'insert_date' e 'update_date'
        df_merged = df_merged.withColumn(
            'insert_date',
            when(col('old.insert_date').isNotNull(), col('old.insert_date')).otherwise(current_date())
        ).withColumn(
            'update_date',
            when(update_condition & col('new.name').isNotNull(), current_date())
            .otherwise(col('old.update_date'))
        )

        # Seleciona as colunas desejadas
        df_merged = df_merged.select(
            col("new.id"),
            col("new.brewery_type"), 
            col("new.name"),
            col("new.address_1"),
            col("new.city"),
            col("new.state"),
            col("new.phone"),
            col("new.latitude"),
            col("new.longitude"),
            col("new.postal_code"),
            col("new.street"),
            col("new.website_url"),
            col("new.country"),
            col("insert_date"),  
            col("update_date")   
        )

        # Salva o DataFrame mesclado de volta na camada Silver
        df_merged.write.mode('overwrite').parquet(silver_path)
        print(f"Dados mesclados e salvos na Silver.")

# Definir a DAG
default_args = {
    'owner': 'Mateus Carvalho',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('silver_layer_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    processar_dados_silver_task = PythonOperator(
        task_id='processar_dados_silver',
        python_callable=processar_dados_silver
    )



# Definir a DAG
default_args = {
    'owner': 'Mateus Carvalho',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('silver_layer_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    processar_dados_silver_task = PythonOperator(
        task_id='processar_dados_silver',
        python_callable=processar_dados_silver
    )
