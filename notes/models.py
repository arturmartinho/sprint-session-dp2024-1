from django.db import models

class Usuarios(models.Model):
    email = models.CharField(max_length=70)
    senha = models.CharField(max_length=70)
    def __str__(self) -> str:
        return f"{self.id} .{self.email}"     
    

class Formulario(models.Model):
    nome = models.CharField(max_length=100)
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
