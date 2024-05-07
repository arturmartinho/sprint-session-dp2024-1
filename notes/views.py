from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.template.loader import get_template
from django.template import Context
from reportlab.pdfgen import canvas


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Formulario, Relaciona

def gerar_pdf(request, formulario_id):
    # Recupere o formulário com o ID fornecido
    formulario = get_object_or_404(Formulario, id=formulario_id)

    # Recupere as perguntas relacionadas ao formulário
    relacionas = Relaciona.objects.filter(id_formulario=formulario_id)

    # Inicialize o objeto de resposta do PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{formulario.nome}.pdf"'

    # Crie um objeto PDF usando o ReportLab
    p = canvas.Canvas(response)

    # Defina o número máximo de perguntas por página e a margem inferior
    max_perguntas_por_pagina = 10
    margem_inferior = 50

    # Inicialize a posição y para desenhar as perguntas
    y_position = 750

    # Adicione as informações do formulário à primeira página do PDF
    p.drawString(100, y_position, f"Nome do Formulário: {formulario.nome}")
    y_position -= 20  # Mova para a próxima linha
    p.drawString(100, y_position, f"Descrição do Formulário: {formulario.descricao}")
    y_position -= 20  # Mova para a próxima linha
    p.drawString(100, y_position, f"Data de Criação: {formulario.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}")
    y_position -= 20  # Mova para a próxima linha

    # Adicione as perguntas relacionadas ao PDF
    count = 0  # Contador para controlar o número de perguntas por página
    for relaciona in relacionas:
        # Mova para a próxima página se o número máximo de perguntas por página for atingido
        if count >= max_perguntas_por_pagina:
            p.showPage()  # Mostra a página atual
            p.drawString(100, margem_inferior, "Continuação...")  # Indica que há mais perguntas na próxima página
            p.drawString(100, margem_inferior - 20, f"Página 2")  # Indica o número da próxima página
            p.drawString(100, margem_inferior - 40, f"Nome do Formulário: {formulario.nome}")  # Repete o nome do formulário na próxima página
            count = 0  # Reseta o contador
            y_position = 750  # Reseta a posição y
            continue

        # Adiciona a pergunta atual ao PDF
        y_position -= 20  # Mova para a próxima linha
        p.drawString(100, y_position, f"Pergunta: {relaciona.id_perg.texto}")
        count += 1  # Incrementa o contador de perguntas

    # Salva o PDF
    p.showPage()
    p.save()

    return response




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
    return render(request, "usuarios/index.html")


def cadastrar(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        first_name = request.POST.get("primeiro_nome", None)
        last_name = request.POST.get("ultimo_nome", None)
        email = request.POST.get("email", None)
        password = request.POST.get("senha", None)
        print(username, first_name, last_name, email, password)
        if username and first_name and last_name and email and password:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            return redirect("login")

        else:
            return HttpResponse("usuario nao foi cadastrado")

    return render(request, "usuarios/cadastro.html")


def er(request):
    print(request.user, request.user.first_name, request.user.last_name)
    # return HttpResponse('usuario foi cadastrado')
    # return render(request, 'notes/cadastro.html')


# ----------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------


@login_required
def criar_formulario(request):
    if request.method == "POST":
        nome = request.POST.get(
            "nome"
        )  # Usar get() para evitar exceção se a chave não existir
        descricao = request.POST.get("descricao")
        usuario = request.user
        formulario = Formulario.objects.create(
            nome=nome, descricao=descricao, usuario=usuario
        )

        return redirect("detalhes_formulario", formulario_id=formulario.id)
    return render(request, "criar_formulario.html")


@login_required
def detalhes_formulario(request, formulario_id):
    formulario = Formulario.objects.get(id=formulario_id)

    perguntas = Pergunta.objects.filter(usuario=request.user)
    relacionas = Relaciona.objects.filter(id_formulario=formulario_id)
    lista_id = []
    for i in relacionas:
        lista_id.append(i.id_perg.id)
    return render(
        request,
        "detalhes_formulario.html",
        {"formulario": formulario, "perguntas": perguntas, "lista_id": lista_id},
    )


@login_required
def meus_formularios(request):
    meus_formularios = Formulario.objects.filter(usuario=request.user)
    return render(
        request, "meus_formularios.html", {"meus_formularios": meus_formularios}
    )


def adicionar_pergunta(request, formulario_id, pergunta_id):

    formulario = Formulario.objects.get(id=formulario_id)
    pergunta = Pergunta.objects.get(id=pergunta_id)
    Relaciona.objects.create(id_perg=pergunta, id_formulario=formulario)

    return redirect("detalhes_formulario", formulario_id=formulario_id)


# def editar_pergunta(request, pergunta_id):
#     pergunta = get_object_or_404(
#         Pergunta, id=pergunta_id
#     )  ## se n achar a pergunta com o id, ele consegue retornar uma pagina 404.
#     if request.method == "POST":
#         texto = request.POST["texto"]  ##pegar os dados do formulario
#         tipo = request.POST["tipo"]
#         pergunta.texto = (
#             texto  # pra atualizar os novos campos de texto e tipo da perguta
#         )
#         pergunta.tipo = tipo
#         pergunta.save()  ##deixar salvo no banco de dados
#         if (
#             tipo == pergunta.MULTIPLA_ESCOLHA
#         ):  ##atualizar as opçoes se for de multipla escolha
#             opcoes = request.POST.getlist("opcao")
#             pergunta.opcao_set.all().delete()  ##apaga as opçoes existentes
#             for opcao_texto in opcoes:
#                 Opcao.objects.create(pergunta=pergunta, texto=opcao_texto)
#         return redirect("detalhes_formulario", formulario_id=formulario_id)
#     return render(request, "adicionar_pergunta.html")


# def editar_pergunta(request, pergunta_id):
#     pergunta = get_object_or_404(
#         Pergunta, id=pergunta_id
#     )  ## se n achar a pergunta com o id, ele consegue retornar uma pagina 404.
#     if request.method == "POST":
#         texto = request.POST["texto"]  ##pegar os dados do formulario
#         tipo = request.POST["tipo"]
#         pergunta.texto = (
#             texto  # pra atualizar os novos campos de texto e tipo da perguta
#         )
#         pergunta.tipo = tipo
#         pergunta.save()  ##deixar salvo no banco de dados
#         if (
#             tipo == pergunta.MULTIPLA_ESCOLHA
#         ):  ##atualizar as opçoes se for de multipla escolha
#             opcoes = request.POST.getlist("opcao")
#             pergunta.opcao_set.all().delete()  ##apaga as opçoes existentes
#             for opcao_texto in opcoes:
#                 Opcao.objects.create(pergunta=pergunta, texto=opcao_texto)
#         return redirect(
#             "detalhes_formulario", formulario_id=pergunta.formulario.id
#         )  ##voltar pra pagina de detalhes do formulario
#     return render(
#         request, "editar_pergunta.html", {"pergunta": pergunta}
#     )  ##renderizar o template de pergunta caso n for POST


@login_required
def excluir_pergunta(request, pergunta_id, formulario_id):
    pergunta = get_object_or_404(
        Pergunta, id=pergunta_id
    )  ##tb serve pra retornar um 404, caso n ache a pergunta
    
    if request.method == "POST":
        pergunta.delete()
        return redirect("detalhes_formulario", formulario_id=formulario_id)
    return render(request, "detalhes_formulario.html", {"pergunta": pergunta})


perguntas = {}  # dicionario para armazenar as perguntas


@login_required
def criar_pergunta(request):

    if request.method == "POST":
        texto = request.POST.get("texto")
        tipo = request.POST.get("tipo")
        usuario = request.user
        pergunta = Pergunta.objects.create(texto=texto, tipo=tipo, usuario=usuario)

        ##voltar pra pagina de sucesso ou da pesquisa de satisfação
        # return HttpResponseRedirect('/sucesso/')
        # redirect('detalhes_formulario')

    return render(request, "criar_pergunta.html")


@login_required
def remover_pergunta(resquest, formulario_id, pergunta_id):
    objeto = Relaciona.objects.filter(id_formulario=formulario_id, id_perg=pergunta_id)
    objeto.delete()
    return redirect("detalhes_formulario", formulario_id=formulario_id)


@login_required
def editar_pergunta(request, pergunta_id):
    objeto = Pergunta.objects.get(id=pergunta_id)
    if request.method == "POST":
        texto = request.POST.get("texto")
        objeto.texto = texto
        tipo = request.POST.get("tipo")
        objeto.tipo = tipo
        objeto.save()
        return redirect("editar_pergunta", pergunta_id=pergunta_id)
    return render(request, "editar_pergunta.html", {"pergunta": objeto})


@login_required
def excluir_formulario(request, formulario_id):
    formulario = Formulario.objects.get(id=formulario_id)
    if request.method == 'POST':
        formulario.delete()
        return redirect('meus_formularios')
    return render(request, 'excluir_formulario.html', {'formulario': formulario})

