from minio import Minio
from datetime import date
import os

# === CONFIGURAÇÕES ===
BUCKET_NAME = "engenharia-de-dados"
BASE_PATH = "bronze/json"
DATA_INGESTAO = date.today().isoformat()

# Conexão com o MinIO
client = Minio(
    "minio:9000",          # ou "localhost:9000" se estiver fora do container
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Criar bucket se não existir
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)
    print(f"🪣 Bucket '{BUCKET_NAME}' criado.")
else:
    print(f"🪣 Bucket '{BUCKET_NAME}' já existe.")

# Caminhos locais → destino no MinIO
ARQUIVOS_JSON = {
    "dados_extrato.json": f"{BASE_PATH}/extratos/data_ingestao={DATA_INGESTAO}/dados_extrato.json",
    "dados_pedidos.json": f"{BASE_PATH}/pedidos_externos/data_ingestao={DATA_INGESTAO}/dados_pedidos.json",
    "dados_produtos.json": f"{BASE_PATH}/produtos_parceiros/data_ingestao={DATA_INGESTAO}/dados_produtos.json",
    "dados_tags.json": f"{BASE_PATH}/tags_produtos/data_ingestao={DATA_INGESTAO}/dados_tags.json"
}

# Upload de cada arquivo JSON
for arquivo_local, destino in ARQUIVOS_JSON.items():
    caminho_local = os.path.join("json", arquivo_local)
    if os.path.exists(caminho_local):
        client.fput_object(BUCKET_NAME, destino, caminho_local)
        print(f"✅ Enviado: {arquivo_local} → {destino}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho_local}")

print("\n🏁 Ingestão de arquivos JSON concluída com sucesso!")
