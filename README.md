# **BEES Data Engineering – Breweries Case**

Este repositório faz referência ao case da ABInbev/BEES para o teste de Data Engineer. Ele aborda o processamento de dados de cervejarias usando uma arquitetura baseada em contêineres.

## 📝 Descrição do Projeto
Este projeto foi desenvolvido para demonstrar a capacidade de consumir, transformar e armazenar dados de uma API de cervejarias utilizando tecnologias modernas de Data Engineering. A orquestração de tarefas foi realizada com Apache Airflow, e o processamento de dados foi feito usando Apache Spark. O Jupyter Notebook foi utilizado para visualização e análise dos dados transformados.

## 📂 Estrutura do Projeto
O projeto segue uma arquitetura baseada em contêineres:
~~~
├── dags
│   ├── bronze_layer_dag.py       # DAG responsável pela ingestão de dados da API
│   ├── silver_layer_dag.py       # DAG para transformar os dados da camada Bronze para a Silver
├── data
│   └── bronze                    # Pasta para iniciar a hierarquia de pastas para salvar os arquivos brutos
│       └── YYYY                  # Hierarquia de Ano
│       └── MM                    # Hierarquia de Mês
│       └── DD                    # Hierarquia de Dia
│           └── Beweries.json     # Arquivo bruto salvo diariamente
│   └── silver                    # Pasta para salvar os dados em formato .parquet]
│       └── *.parquet             # Arquivos em parquet.parquet
│   └── ntb_gold                  # Pasta para salvar o notebook
│       └── ntb_gold.ipynb        # Notebook para análise e visualização dos dados
├── docker-compose.yml            # Arquivo para orquestrar os serviços em contêineres
├── Dockerfile                    # Arquivo Docker para configurar o ambiente Airflow + Spark
└── README.md                     # Documentação do projeto
~~~

## 🛠️ Tecnologias Utilizadas
- Docker: Contêinerização dos serviços e fácil replicação do ambiente.
- Apache Spark: Para processamento distribuído e transformação dos dados.
- Apache Airflow: Para orquestração e agendamento de tarefas.
- Jupyter Notebook: Para visualização e exploração dos dados processados.
- Python: Linguagem principal utilizada no projeto.
- Pandas (opcional): Para manipulação de dados no notebook.

## 🥉 Camada Bronze
Os dados brutos são salvos na camada Bronze em formato JSON, organizados em uma hierarquia de diretórios no seguinte formato:
~~~
YYYY/MM/DD/breweries.json
~~~
Essa organização facilita a consulta e o processamento incremental dos dados, permitindo a captura de dados diários de forma estruturada.

## 🥈 Camada Silver
Na camada Silver, os dados passam por um processamento para inclusão de colunas que acompanham o ciclo de vida das informações. O processo é o seguinte:

O pipeline verifica se já existem dados na camada Silver. Se não houver dados:
- A camada Silver é criada a partir dos dados da Bronze.
São adicionadas duas colunas:
- insert_date: Preenchida com a data em que o dado foi inserido.
- update_date: Inicialmente nula, esta coluna só será populada se o dado for atualizado no futuro.
Se já houver dados na camada Silver, o pipeline realiza um merge entre os dados novos e os antigos. Neste merge:
- A coluna insert_date mantém o valor original do dado.
- A coluna update_date é atualizada com a data atual apenas se os dados tiverem sido modificados.

## 🥇 Camada Gold
A camada Gold é gerada a partir de um notebook que lê os dados processados na Silver, em formato Parquet, e realiza análises e visualizações. O notebook utiliza a biblioteca Matplotlib para criar gráficos que auxiliam na interpretação dos dados, gerando insights a partir das informações disponíveis na camada Silver.

## 🚀 Como Executar o Projeto
Clone este repositório:

~~~
git clone https://github.com/mateusccarvalho/ABInbev
~~~
Navegue até o diretório do projeto:
~~~
cd ABInbev
~~~
Suba os contêineres com Docker Compose:
~~~
docker-compose up -d
~~~
Isso iniciará os serviços do Airflow, Spark e Jupyter Notebook.

Acesse o Apache Airflow em seu navegador para monitorar as DAGs:
~~~
http://localhost:8080
~~~
Credenciais padrão:

- Usuário: airflow
- Senha: airflow

Acesse o Jupyter Notebook:
~~~
http://localhost:8888/
~~~

## 📊 Análise dos Dados
Dentro do Jupyter Notebook, o arquivo ntb_gold.ipynb contém a análise e visualização dos dados. Ele demonstra:

- Gráfico mostrando o número de cervejarias por estado e tipo.
  ![image](https://github.com/user-attachments/assets/5e9875b2-6b52-453a-89d7-318042d0b4c9)
- Gráfico mostrando o tipo de cervejaria
  ![image](https://github.com/user-attachments/assets/3a3fb7e0-554d-4ae2-a7f2-2975ea798521)
- Gráfico ilustrando a distribuição das cervejarias por país.
  ![image](https://github.com/user-attachments/assets/dd4df2a0-251c-47a9-acf8-1d1082fe108c)

## ⚠️ Agradecimento
Este repositório utilizou como base o seguinte projeto para desenvolvimento dos arquivos Docker:
https://github.com/airscholar/SparkingFlow
