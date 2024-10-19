from pyspark.sql import SparkSession

# Cria uma sessão Spark
spark = SparkSession.builder \
    .appName("Read Gold Layer") \
    .getOrCreate()

# Define o caminho da camada Gold
gold_path = 'C:\ABInbev\data\gold'  

# Lê os dados da camada Gold
gold_df = spark.read.parquet(gold_path)

# Exibe os dados
gold_df.show(truncate=False)

# Para ver o esquema dos dados
gold_df.printSchema()

# Para realizar operações adicionais, você pode usar métodos como:
# gold_df.groupBy('brewery_type', 'brewery_location').count().show()
