from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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




