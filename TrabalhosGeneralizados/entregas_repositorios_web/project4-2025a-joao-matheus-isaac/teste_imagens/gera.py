# gera.py
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "black-forest-labs/FLUX.1-dev"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def testar_endpoint():
    resp = requests.get(API_URL, headers=HEADERS, timeout=30)
    print("GET status:", resp.status_code)
    print("GET body:", resp.text[:200])

def proximo_nome_arquivo(base_name="lutador", ext=".png"):
    if not os.path.exists(base_name + ext):
        return base_name + ext
    i = 1
    while os.path.exists(f"{base_name}{i}{ext}"):
        i += 1
    return f"{base_name}{i}{ext}"

def gerar_imagem_flux(descricao: str, output_path: str = None):
    if output_path is None:
        output_path = proximo_nome_arquivo()
    prompt = f"Lutador, {descricao}"
    payload = {"inputs": prompt}
    resp = requests.post(API_URL, headers=HEADERS, json=payload)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return output_path

if __name__ == "__main__":
    testar_endpoint()
    if len(sys.argv) < 2:
        print("Uso: python gera.py \"descrição do lutador\"", file=sys.stderr)
        sys.exit(1)
    descricao = sys.argv[1]
    try:
        caminho = gerar_imagem_flux(descricao)
        print("Imagem salva em:", caminho)
    except Exception as err:
        print("Erro:", err, file=sys.stderr)
        sys.exit(1)
