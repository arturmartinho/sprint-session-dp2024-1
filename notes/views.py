from django.http import HttpResponse
from .models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def cadastrar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        Usuarios.objects.create(email=email,senha=senha)
        return redirect('cadastrar')
    todos_usuarios = Usuarios.objects.all().order_by('-id')
    return render(request, 'cadastrar/cadastrar.html', {'usuarios': todos_usuarios})
    # return HttpResponse("Olá mundo! Este é o app notes de DevLife do Insper.")


