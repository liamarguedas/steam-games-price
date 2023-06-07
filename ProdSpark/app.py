from pyspark import SparkContext
from pyspark.ml.pipeline import PipelineModel
import pickle

sc = SparkContext()

# Carregue o modelo salvo em disco
with open("Data-Science\Steam-Games-Price\Modelo\TrainedModel.pkl", "rb") as f:
    modelo_serializado = pickle.load(f)

# Carregue o modelo serializado em Spark
modelo_spark = PipelineModel.load(modelo_serializado)

# Faça previsões em dados novos
dados_novos = spark.read.csv("arquivo.csv", header=True, inferSchema=True)
previsoes = modelo_spark.transform(dados_novos)

# Guardar previsões
previsoes.write.format("csv").save("company-path")