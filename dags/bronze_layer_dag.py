from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import os

# Função para consumir e salvar os dados da API
def consumir_dados():
    url = "https://api.openbrewerydb.org/breweries"
    response = requests.get(url)
    data = response.json()

    # Obter a data atual e formatá-la como yyyy/mm/dd
    current_date = datetime.now().strftime('%Y/%m/%d')

    # Definir o caminho de destino seguindo a estrutura yyyy/mm/dd
    bronze_raw_path = f'/data/bronze/{current_date}/breweries.json'

    # Criar diretórios se não existirem
    os.makedirs(os.path.dirname(bronze_raw_path), exist_ok=True)
    
    # Persistir dados brutos
    with open(bronze_raw_path, 'w') as f:
        json.dump(data, f)

# Definir a DAG
default_args = {
    'owner': 'Mateus Carvalho',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('bronze_layer_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    consumir_dados_task = PythonOperator(
        task_id='consumir_dados',
        python_callable=consumir_dados
    )
