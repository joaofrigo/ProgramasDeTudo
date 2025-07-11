
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


def home_view(request):
    """
    Exibe a lista de lutadores e provê botões para adicionar e remover.
    """
    lutadores = Lutador.objects.all()
    contexto = {'lutadores': lutadores}
    return render(request, 'home.html', contexto)

@require_POST
def remover_lutador(request, id_lutador):
    """
    Remove o lutador de acordo com o ID enviado pelo form.
    """
    lutador = get_object_or_404(Lutador, pk=id_lutador)
    lutador.delete()
    return redirect('home')

def criar_lutador_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    lutadores = Lutador.objects.all()
    usuario = Usuario.objects.get(pk=usuario_id)

    if request.method == 'POST':
        # Verifica limite somente após POST
        if Lutador.objects.filter(usuario=usuario).count() >= 2:
            messages.error(request, "Você já atingiu o limite de 2 lutadores.")
            return render(request, 'criar_lutador.html', {
                'lutadores': lutadores
            })

        nome = request.POST['nome']
        idade = request.POST.get('idade') or None
        profissao = request.POST.get('profissao') or ''
        historia = request.POST.get('historia') or ''

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

        return redirect('home')

    return render(request, 'criar_lutador.html', {
        'lutadores': lutadores
    })

def ver_lutador_view(request, id_lutador):
    lutador = get_object_or_404(Lutador, id_lutador=id_lutador)
    lutadores = Lutador.objects.exclude(id_lutador=lutador.id_lutador)  # todos menos o atual

    amizades_ids = list(lutador.amizades.values_list('amigo_id', flat=True))
    inimizades_ids = list(lutador.inimizades.values_list('inimigo_id', flat=True))

    return render(request, 'ver_lutador.html', {
        'lutador': lutador,
        'lutadores': lutadores,
        'amizades_ids': amizades_ids,
        'inimizades_ids': inimizades_ids,
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
            return redirect('home')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo") # retorna uma resposta em html