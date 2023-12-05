from django.db import models


class FormularioContato(models.Model):   
    nome = models.CharField(blank=True, null=True, max_length=150)
    email = models.EmailField(max_length=40)
    telefone = models.CharField(blank=True, null=True, max_length=20)
    mensagem = models.TextField(max_length=300)
    status_contato = models.CharField(null=True, max_length=10)
   

