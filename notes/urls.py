from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastrar, name='cadastro'),
    path('login', views.er, name='er'),
]