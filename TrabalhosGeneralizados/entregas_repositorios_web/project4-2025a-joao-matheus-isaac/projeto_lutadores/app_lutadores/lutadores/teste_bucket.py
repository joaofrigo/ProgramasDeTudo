import os
from dotenv import load_dotenv
from supabase import create_client
from pathlib import Path

load_dotenv()  # Carrega variáveis do .env

def upload_imagem_bucket(caminho_local, nome_arquivo):
    SUPABASE_URL = "https://ilermoovzaxjeenkfmts.supabase.co"
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    with open(caminho_local, "rb") as f:
        supabase.storage.from_("imagens.ia").upload(
            path=nome_arquivo,
            file=f,
            file_options={"content-type": "image/png", "upsert": "true"}  # 'upsert' deve ser string
        )
    print(f"Imagem {nome_arquivo} enviada ao bucket.")

if __name__ == "__main__":
    pasta_saida = Path(__file__).parent
    caminho_imagem = pasta_saida / "lutador.png"
    nome_arquivo = "lutador.png"
    try:
        upload_imagem_bucket(str(caminho_imagem), nome_arquivo)
    except Exception as e:
        print(f"Erro ao enviar imagem para o bucket: {e}")
