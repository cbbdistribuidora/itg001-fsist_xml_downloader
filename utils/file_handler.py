import os
import shutil
import zipfile
from datetime import datetime
from config import CAMINHO_DOWNLOAD, PASTA_DESTINO

def mover_e_extrair_zip():
    # Cria subpasta com a data de hoje
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    pasta_data = os.path.join(PASTA_DESTINO, data_hoje)
    os.makedirs(pasta_data, exist_ok=True)

    # Procura o arquivo .zip mais recente na pasta de downloads
    arquivos_zip = [f for f in os.listdir(CAMINHO_DOWNLOAD) if f.endswith('.zip')]
    if not arquivos_zip:
        print("Nenhum arquivo .zip encontrado na pasta de Downloads.")
        return

    arquivos_zip.sort(key=lambda f: os.path.getmtime(os.path.join(CAMINHO_DOWNLOAD, f)), reverse=True)
    zip_origem = os.path.join(CAMINHO_DOWNLOAD, arquivos_zip[0])
    zip_destino = os.path.join(pasta_data, arquivos_zip[0])

    # Move o arquivo .zip para a pasta do dia
    shutil.move(zip_origem, zip_destino)
    print(f"ZIP movido para: {zip_destino}")

    # Extrai o conteúdo
    with zipfile.ZipFile(zip_destino, 'r') as zip_ref:
        zip_ref.extractall(pasta_data)
        print(f"Arquivos extraídos para: {pasta_data}")

    # Remove o .zip após extração
    os.remove(zip_destino)
    print("ZIP removido após extração.")