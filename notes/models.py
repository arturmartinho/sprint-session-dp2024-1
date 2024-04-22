from django.db import models
from django.contrib.auth.models import User
# class Usuarios(models.Model):
#     email = models.CharField(max_length=70)
#     senha = models.CharField(max_length=70)
#     def __str__(self) -> str:
#         return f"{self.id} .{self.email}"     
    

class Formulario(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=9999)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Pergunta(models.Model):
    TEXTO = 'TXT'
    INTERVALO = 'INT'
    MULTIPLA_ESCOLHA = 'MUL'
    TIPOS_PERGUNTA = [
        (TEXTO, 'Texto'),
        (INTERVALO, 'Intervalo'),
        (MULTIPLA_ESCOLHA, 'Múltipla Escolha'),
    ]

    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.CharField(max_length=3, choices=TIPOS_PERGUNTA)

class Opcao(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=100)

class Formularios(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=9999)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

# class Relaciona(models.Model):
#     id_perg = models.ForeignKey()
#     id_formulario = models.ForeignKey()
    
