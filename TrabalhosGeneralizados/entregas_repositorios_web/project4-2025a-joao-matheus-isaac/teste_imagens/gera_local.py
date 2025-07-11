import sys
import os
from pathlib import Path

from dotenv import load_dotenv
import torch
from diffusers import FluxPipeline

load_dotenv()  # Carrega variáveis do .env

def carregar_pipeline():
    print("HF_TOKEN está setado?", bool(os.getenv("HF_TOKEN")))
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        use_auth_token=True
    )
    pipe.to("cuda")
    return pipe

def gerar_imagem_flux(pipe, descricao: str, output_path: str = "lutador.png"):
    prompt = f"Lutador, {descricao}"
    print("Gerando imagem para o prompt:", prompt)
    imagem = pipe(
        prompt=prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cuda").manual_seed(0)
    ).images[0]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    imagem.save(output_path)
    print("Imagem salva em:", output_path)
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python gera_local.py \"descrição do lutador\"", file=sys.stderr)
        sys.exit(1)
    descricao = sys.argv[1]
    try:
        pipe = carregar_pipeline()
        caminho = gerar_imagem_flux(pipe, descricao)
        print("Concluído.")
    except Exception as err:
        print("Erro fatal:", err, file=sys.stderr)
        sys.exit(1)
