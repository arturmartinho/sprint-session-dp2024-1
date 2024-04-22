from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastrar, name='cadastro'),
    path('login', views.er, name='er'),
    path('criar_formulario/', views.criar_formulario, name='criar_formulario'),
    path('formulario/<int:formulario_id>/', views.detalhes_formulario, name='detalhes_formulario'),
    path('formulario/<int:formulario_id>/adicionar-pergunta/', views.adicionar_pergunta, name='adicionar_pergunta'),
    path('meus_formularios/', views.meus_formularios, name='meus_formularios'),
]

    
