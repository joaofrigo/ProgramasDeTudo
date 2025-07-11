
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from urllib.parse import urlencode
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
from supabase import create_client
from urllib.parse import urlparse
from .models import *


def home_view(request):
    """
    Exibe a lista de lutadores e provê botões para adicionar e remover.
    """
    lutadores = Lutador.objects.all()
    contexto = {'lutadores': lutadores}
    return render(request, 'home.html', contexto)

def deletar_imagem_bucket(url_imagem):
    SUPABASE_URL = "https://ilermoovzaxjeenkfmts.supabase.co"
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    parsed_url = urlparse(url_imagem)
    caminho = parsed_url.path  # ex: /storage/v1/object/public/imagens.ia//lutador.png
    
    prefixo = "/storage/v1/object/public/imagens.ia/"
    if caminho.startswith(prefixo):
        nome_arquivo = caminho[len(prefixo):]
    else:
        nome_arquivo = caminho.lstrip("/")
    
    if nome_arquivo != "lutador.png":  # não remove a imagem padrão
        supabase.storage.from_("imagens.ia").remove([nome_arquivo])

@require_POST
def remover_lutador(request, id_lutador):
    lutador = get_object_or_404(Lutador, pk=id_lutador)
    
    if lutador.url_imagem:
        try:
            deletar_imagem_bucket(lutador.url_imagem)
        except Exception as e:
            print(f"Erro ao deletar imagem do bucket: {e}")
    
    lutador.delete()
    return redirect('home')


from .gera import gerar_imagem_flux
from pathlib import Path

load_dotenv()
def upload_imagem_bucket(caminho_local, nome_arquivo):
    SUPABASE_URL = "https://ilermoovzaxjeenkfmts.supabase.co"
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    with open(caminho_local, "rb") as f:
        supabase.storage.from_("imagens.ia").upload(
            path=nome_arquivo,
            file=f,
            file_options={"content-type": "image/png", "upsert": "true"}
        )
    return f"{SUPABASE_URL}/storage/v1/object/public/imagens.ia/{nome_arquivo}"

def criar_lutador_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    lutadores = Lutador.objects.all()
    usuario = Usuario.objects.get(pk=usuario_id)

    if request.method == 'POST':
        if Lutador.objects.filter(usuario=usuario).count() >= 2:
            messages.error(request, "Você já atingiu o limite de 2 lutadores.")
            return render(request, 'criar_lutador.html', {
                'lutadores': lutadores
            })

        nome = request.POST['nome']
        idade = request.POST.get('idade') or None
        profissao = request.POST.get('profissao') or ''
        historia = request.POST.get('historia') or ''
        aparencia = request.POST.get('aparencia') or ''

        novo = Lutador.objects.create(
            nome=nome,
            idade=idade,
            profissao=profissao,
            historia=historia,
            usuario=usuario
        )

        for amigo_id in request.POST.getlist('amizades'):
            if amigo_id:
                Amizade.objects.create(lutador=novo, amigo_id=int(amigo_id))

        for inimigo_id in request.POST.getlist('inimizades'):
            if inimigo_id:
                Inimizade.objects.create(lutador=novo, inimigo_id=int(inimigo_id))

        pasta_saida = Path(__file__).resolve().parent / "lutadores"
        pasta_saida.mkdir(exist_ok=True)
        nome_arquivo = f"{nome}.png"
        caminho_completo = str(pasta_saida / nome_arquivo)

        imagem_gerada = False

        if aparencia:
            try:
                gerar_imagem_flux(aparencia, output_path=caminho_completo)
                imagem_gerada = True
                print(f"Imagem gerada: {nome_arquivo}")
            except Exception as e:
                messages.warning(request, f"Erro ao gerar imagem: {e}")

        if not imagem_gerada:
            caminho_completo = str(pasta_saida / "lutador.png")
            nome_arquivo = "lutador.png"
            print("Imagem padrão utilizada: lutador.png")

        try:
            url_imagem = upload_imagem_bucket(caminho_completo, nome_arquivo)
            novo.url_imagem = url_imagem
        except Exception as e:
            messages.warning(request, f"Erro ao enviar imagem para o bucket: {e}")

        novo.save()
        return redirect('home')

    return render(request, 'criar_lutador.html', {
        'lutadores': lutadores
    })


from django.shortcuts import render, get_object_or_404
from .models import Lutador

def ver_lutador_view(request, id_lutador):
    lutador = get_object_or_404(Lutador, id_lutador=id_lutador)
    lutadores = Lutador.objects.exclude(id_lutador=lutador.id_lutador)

    amizades_ids = list(lutador.amizades.values_list('amigo_id', flat=True))
    inimizades_ids = list(lutador.inimizades.values_list('inimigo_id', flat=True))

    return render(request, 'ver_lutador.html', {
        'lutador': lutador,
        'lutadores': lutadores,
        'amizades_ids': amizades_ids,
        'inimizades_ids': inimizades_ids,
        'url_imagem': lutador.url_imagem  # adiciona a URL da imagem do bucket
    })





@require_POST
def editar_lutador_view(request, id_lutador):
    lutador = get_object_or_404(Lutador, id_lutador=id_lutador)

    lutador.nome = request.POST.get('nome', lutador.nome)
    idade = request.POST.get('idade')
    lutador.idade = int(idade) if idade else None
    lutador.profissao = request.POST.get('profissao', lutador.profissao)
    lutador.historia = request.POST.get('historia', lutador.historia)
    lutador.save()

    # Atualizar amizades
    amizades_ids = request.POST.getlist('amizades')
    lutador.amizades.all().delete()
    for amigo_id in amizades_ids:
        Amizade.objects.create(lutador=lutador, amigo_id=int(amigo_id))

    # Atualizar inimizades
    inimizades_ids = request.POST.getlist('inimizades')
    lutador.inimizades.all().delete()
    for inimigo_id in inimizades_ids:
        Inimizade.objects.create(lutador=lutador, inimigo_id=int(inimigo_id))

    return redirect('ver_lutador', id_lutador=lutador.id_lutador)

def adicionar_golpe_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(pk=usuario_id)
    lutadores = Lutador.objects.all()

    if request.method == 'POST':
        lutador_id = request.POST.get('lutador_id')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        forca = request.POST.get('forca')

        lutador = get_object_or_404(Lutador, id_lutador=lutador_id)

        Golpe.objects.create(
            lutador=lutador,
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            forca=forca,
            usuario=usuario 
        )

        return redirect('home')

    return render(request, 'adicionar_golpe.html', {'lutadores': lutadores})


def lista_golpes_view(request):
    golpes = Golpe.objects.select_related('lutador').all()
    return render(request, 'lista_golpes.html', {'golpes': golpes})

def ver_golpe_view(request, id_golpe):
    golpe = get_object_or_404(Golpe, id_golpe=id_golpe)
    lutadores = Lutador.objects.all()
    return render(request, 'ver_golpe.html', {'golpe': golpe, 'lutadores': lutadores})


@require_POST
def editar_golpe_view(request, id_golpe):
    golpe = get_object_or_404(Golpe, id_golpe=id_golpe)

    golpe.nome = request.POST.get('nome', golpe.nome)
    golpe.descricao = request.POST.get('descricao', golpe.descricao)
    golpe.forca = request.POST.get('forca', golpe.forca)
    golpe.tipo = request.POST.get('tipo', golpe.tipo)
    lutador_id = request.POST.get('lutador')
    if lutador_id:
        golpe.lutador = get_object_or_404(Lutador, id_lutador=int(lutador_id))
    golpe.save()

    return redirect('ver_golpe', id_golpe=golpe.id_golpe)

@require_POST
def remover_golpe_view(request, id_golpe):
    golpe = get_object_or_404(Golpe, id_golpe=id_golpe)
    golpe.delete()
    return redirect('lista_golpes')

def login_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        try:
            usuario = Usuario.objects.get(nome=nome, senha=senha)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nome'] = usuario.nome  # salva o nome na sessão
            return redirect('home')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def registro_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(nome=nome).exists():
            messages.error(request, 'Nome de usuário já existe')
        else:
            usuario = Usuario.objects.create(nome=nome, email=email, senha=senha)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nome'] = usuario.nome
            return redirect('home')

    return render(request, 'registro.html')

def google_oauth_callback_view(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Código de autorização não fornecido.')
        return redirect('login')

    # Trocar código pelo token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    if token_response.status_code != 200:
        messages.error(request, 'Falha ao obter token do Google.')
        return redirect('login')

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        messages.error(request, 'Token de acesso inválido.')
        return redirect('login')

    # Buscar dados do usuário no Google
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token}
    userinfo_response = requests.get(userinfo_url, params=params)
    if userinfo_response.status_code != 200:
        messages.error(request, 'Falha ao obter dados do usuário Google.')
        return redirect('login')

    userinfo = userinfo_response.json()
    email = userinfo.get('email')
    nome = userinfo.get('name') or userinfo.get('email')

    if not email:
        messages.error(request, 'E-mail do usuário não disponível.')
        return redirect('login')

    # Verifica se usuário existe; cria se não existir
    usuario, created = Usuario.objects.get_or_create(email=email, defaults={'nome': nome, 'senha': ''})

    # Salva dados na sessão
    request.session['usuario_id'] = usuario.id
    request.session['usuario_nome'] = usuario.nome

    return redirect('home')

def google_oauth_login_view(request):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)



def teste_multiplayer(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    return render(request, "teste_multiplayer.html", {"usuario_id": usuario_id})

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo") # retorna uma resposta em html
