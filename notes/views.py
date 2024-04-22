from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
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

def index(request):
    return render(request, 'usuarios/index.html')

def cadastrar(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        first_name = request.POST.get('primeiro_nome',None)
        last_name = request.POST.get('ultimo_nome', None)
        email = request.POST.get('email',None)
        password = request.POST.get('senha',None)
        print(username,first_name,last_name,email,password)
        if username and first_name and last_name and email and password:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            return redirect('login')
        
        else:
            return HttpResponse('usuario nao foi cadastrado')
        
    return render(request, 'usuarios/cadastro.html')


def er(request):
    print(request.user, request.user.first_name, request.user.last_name)
    # return HttpResponse('usuario foi cadastrado')
    # return render(request, 'notes/cadastro.html')


#----------------------------------------------------------------------------------------------------------------------------------


@login_required
def criar_formulario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')  # Usar get() para evitar exceção se a chave não existir
        descricao = request.POST.get('descricao')
        formulario = Formulario.objects.create(nome=nome,descricao=descricao)

        return redirect('detalhes_formulario', formulario_id=formulario.id)
    return render(request, 'criar_formulario.html')

@login_required
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


def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id) ## se n achar a pergunta com o id, ele consegue retornar uma pagina 404.
    if request.method == 'POST':
        texto = request.POST['texto'] ##pegar os dados do formulario 
        tipo = request.POST['tipo']
        pergunta.texto = texto #pra atualizar os novos campos de texto e tipo da perguta
        pergunta.tipo = tipo 
        pergunta.save() ##deixar salvo no banco de dados
        if tipo == pergunta.MULTIPLA_ESCOLHA: ##atualizar as opçoes se for de multipla escolha
            opcoes = request.POST.getlist('opcao')
            pergunta.opcao_set.all().delete() ##apaga as opçoes existentes
            for opcao_texto in opcoes:
                Opcao.objects.create(pergunta=pergunta, texto=opcao_texto)
        return redirect('detalhes_formulario', formulario_id=pergunta.formulario.id) ##voltar pra pagina de detalhes do formulario
    return render(request,'editar_pergunta.html' , {'pergunta': pergunta}) ##renderizar o template de pergunta caso n for POST


def excluir_perguntar(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id) ##tb serve pra retornar um 404, caso n ache a pergunta
    formulario_id = pergunta.formulario.id 
    if request.method == 'POST':
        pergunta.delete()
        return redirect('detalhes_formulario', formulario_id=formulario_id)
    return render(request, 'excluir_pergunta.html', {'pergunta': pergunta})




