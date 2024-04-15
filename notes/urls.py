from django.urls import path

from . import views

urlpatterns = [

    path('', views.cadastrar, name='cadastro'),
    path('criar_formulario/', views.criar_formulario, name='criar_formulario'),
    path('formulario/<int:formulario_id>/', views.detalhes_formulario, name='detalhes_formulario'),
    path('formulario/<int:formulario_id>/adicionar-pergunta/', views.adicionar_pergunta, name='adicionar_pergunta'),
]

    

