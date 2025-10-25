# -- coding: utf-8 --
"""
Case 1 – Ingestão Batch para Data Lake
Etapa: Fonte 3 (API Pública - BrasilAPI / IBGE)
Objetivo: Coletar dados da API pública de UFs do Brasil e salvar na camada Bronze do MinIO.
Estrutura de destino:
datalake/bronze/api/ibge_uf/data_ingestao=YYYY-MM-DD/uf.json
"""

import requests
from minio import Minio
from datetime import date
import json
from io import BytesIO

# ==================================================
# CONFIGURAÇÕES GERAIS
# ==================================================
BUCKET_NAME = "engenharia-de-dados"
BASE_PATH = "bronze/api/ibge_uf"
DATA_INGESTAO = date.today().isoformat()
ARQUIVO_DESTINO = f"{BASE_PATH}/data_ingestao={DATA_INGESTAO}/uf.json"

# ==================================================
# CONEXÃO COM O MINIO
# ==================================================
client = Minio(
    "minio:9000",          # use "localhost:9000" se estiver rodando fora do container
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Criar bucket se não existir
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)
    print(f"🪣 Bucket '{BUCKET_NAME}' criado com sucesso.")
else:
    print(f"🪣 Bucket '{BUCKET_NAME}' já existe.")

# ==================================================
# REQUISIÇÃO À API BRASILAPI
# ==================================================
url = "https://brasilapi.com.br/api/ibge/uf/v1"
print(f"🌎 Coletando dados da API: {url}")

try:
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data)} registros obtidos da API BrasilAPI (IBGE).")

        # Converter o JSON em bytes para envio ao MinIO
        buffer = BytesIO(json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8"))

        # Upload para o MinIO
        client.put_object(
            BUCKET_NAME,
            ARQUIVO_DESTINO,
            buffer,
            length=len(buffer.getvalue()),
            content_type="application/json"
        )

        print(f"🚀 Arquivo salvo com sucesso em: {ARQUIVO_DESTINO}")
        print(f"📦 Data de ingestão: {DATA_INGESTAO}")
    else:
        print(f"❌ Erro na requisição da API. Código de status: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao conectar à API: {e}")

print("\n🏁 Ingestão da API BrasilAPI finalizada com sucesso!")

