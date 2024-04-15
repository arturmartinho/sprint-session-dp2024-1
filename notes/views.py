from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Formulario, Pergunta, Opcao

# def cadastrar(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         senha = request.POST.get('senha')

#         Usuarios.objects.create(email=email,senha=senha)
#         return redirect('cadastrar')
#     todos_usuarios = Usuarios.objects.all().order_by('-id')
#     return render(request, 'cadastro/cadastro.html', {'usuarios': todos_usuarios})
#     # return HttpResponse("Olá mundo! Este é o app notes de DevLife do Insper.")

# def login(request):
#     if request.method =='POST':
#         email = request.POST.get('email')
#         senha = request.POST.get('senha')

def cadastrar(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        first_name = request.POST.get('primeiro nome',None)
        last_name = request.POST.get('ultimo nome', None)
        email = request.POST.get('email',None)
        password = request.POST.get('senha',None)
        if username and first_name and last_name and email and password:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            return redirect('login')
        else:
            return HttpResponse('usuario nao foi cadastrado')
        
    # return render(request,)


def login(request):
    print(request.user, request.user.first_name, request.user.last_name)
    return render(request, 'notes/cadastro.html')



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

