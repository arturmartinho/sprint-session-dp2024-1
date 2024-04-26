from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastrar, name='cadastro'),
    path('login', views.er, name='er'),
    path('criar_formulario/', views.criar_formulario, name='criar_formulario'),
    path('formulario/<int:formulario_id>/', views.detalhes_formulario, name='detalhes_formulario'),
    path('criar_pergunta', views.criar_pergunta, name='criar_pergunta'),
    path('formulario/<int:formulario_id>/gerar_pdf/', views.gerar_pdf, name='formulario_pdf'),
]

    
