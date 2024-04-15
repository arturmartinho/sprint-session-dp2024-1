from django.http import HttpResponse
from .models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Formulario, Pergunta, Opcao

def cadastrar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        Usuarios.objects.create(email=email,senha=senha)
        return redirect('cadastrar')
    todos_usuarios = Usuarios.objects.all().order_by('-id')
    return render(request, 'cadastrar/cadastrar.html', {'usuarios': todos_usuarios})
    # return HttpResponse("Olá mundo! Este é o app notes de DevLife do Insper.")

def criar_formulario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')  # Usar get() para evitar exceção se a chave não existir
        formulario = Formulario.objects.create(nome=nome)
        return redirect('detalhes_formulario', formulario_id=formulario.id)
    return render(request, 'criar_formulario.html')

def detalhes_formulario(request, formulario_id):
    formulario = Formulario.objects.get(id=formulario_id)
    perguntas = Pergunta.objects.filter(formulario=formulario)
    return render(request, 'detalhes_formulario.html', {'formulario': formulario, 'perguntas': perguntas})

def adicionar_pergunta(request, formulario_id):
    if request.method == 'POST':
        texto = request.POST['texto']
        tipo = request.POST['tipo']
        formulario = Formulario.objects.get(id=formulario_id)
        pergunta = Pergunta.objects.create(formulario=formulario, texto=texto, tipo=tipo)
        # Se for uma pergunta de múltipla escolha, adicione opções
        if tipo == Pergunta.MULTIPLA_ESCOLHA:
            opcoes = request.POST.getlist('opcao')
            for opcao_texto in opcoes:
                Opcao.objects.create(pergunta=pergunta, texto=opcao_texto)
        return redirect('detalhes_formulario', formulario_id=formulario_id)
    return render(request, 'adicionar_pergunta.html')


