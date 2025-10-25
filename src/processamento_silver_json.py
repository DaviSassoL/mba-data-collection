# -- coding: utf-8 --
"""
Case 1 – Processamento da Camada Silver
Fonte: API BrasilAPI (IBGE)
Objetivo: Ler dados brutos da camada Bronze e gerar dados confiáveis (trusted) na camada Silver.
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from datetime import date

# ===============================
# CONFIGURAÇÕES
# ===============================
BUCKET = "engenharia-de-dados"
CAMINHO_BRONZE = f"s3a://{BUCKET}/Bronze/api/ibge_uf/"
CAMINHO_SILVER = f"s3a://{BUCKET}/Silver/ibge_uf/"
DATA_INGESTAO = date.today().isoformat()

# ===============================
# SPARK SESSION
# ===============================
spark = SparkSession.builder.appName("ProcessamentoSilverAPI").getOrCreate()

# Configurar acesso ao MinIO
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")

# ===============================
# LEITURA DO ARQUIVO BRONZE
# ===============================
print("📥 Lendo arquivo uf.json da camada Bronze...")
df_ibge = spark.read.json(f"{CAMINHO_BRONZE}data_ingestao={DATA_INGESTAO}/uf.json")

# ===============================
# DEFINIÇÃO DE SCHEMA EXPLÍCITO
# ===============================
schema_ibge = StructType([
    StructField("id", IntegerType(), True),
    StructField("sigla", StringType(), True),
    StructField("nome", StringType(), True)
])

df_ibge = spark.createDataFrame(df_ibge.rdd, schema=schema_ibge)

# ===============================
# ESCRITA NA CAMADA SILVER
# ===============================
print("💾 Gravando dados tratados na camada Silver...")
df_ibge.write.mode("overwrite").parquet(CAMINHO_SILVER)

print(f"✅ Dados do IBGE processados com sucesso!")
print(f"📦 Caminho de saída: {CAMINHO_SILVER}")

