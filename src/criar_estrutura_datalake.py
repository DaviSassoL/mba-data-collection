from minio import Minio
from datetime import datetime
from io import BytesIO

# --- CONFIGURAÇÕES ---
BUCKETS = ["bronze", "silver"]
DATA_ATUAL = datetime.now().strftime("%Y%m%d")

# Estrutura com partições de data na camada bronze
ESTRUTURA = {
    "bronze": [
        f"bronze/dbloja/data={DATA_ATUAL}/",
        f"bronze/json/data={DATA_ATUAL}/",
        f"bronze/ibge/data={DATA_ATUAL}/",
    ],
    "silver": [
        "silver/dbloja/",
        "silver/json/",
        "silver/ibge/",
    ]
}

# --- CONEXÃO COM O MINIO ---
client = Minio(
    "minio:9000",          # use "localhost:9000" se estiver fora do container
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# --- CRIAR BUCKETS SE NECESSÁRIO ---
for bucket in BUCKETS:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"🪣 Bucket '{bucket}' criado com sucesso.")
    else:
        print(f"🪣 Bucket '{bucket}' já existe.")

# --- CRIAR ESTRUTURA DE DIRETÓRIOS ---
for bucket, pastas in ESTRUTURA.items():
    for path in pastas:
        # cria um objeto placeholder dentro do caminho
        buffer = BytesIO(b"estrutura inicial")
        objeto = f"{path}.keep"
        client.put_object(bucket, objeto, buffer, length=len(buffer.getvalue()))
        print(f"📁 Estrutura criada: {bucket}/{path}")

print("\n✅ Estrutura completa do Data Lake criada com sucesso!")

