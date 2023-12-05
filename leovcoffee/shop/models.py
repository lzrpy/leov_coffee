from django.db import models
from django.utils.safestring import mark_safe
from account.models import *





class Categoria(models.Model):
    nome = models.CharField(max_length=200)
    nome_url = models.SlugField(null=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    imagem = models.ImageField(null=True, upload_to='images_products/')
    nome = models.CharField(max_length=30, null=True)
    id_produto = models.CharField(max_length=10, null=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE,null=True)
    nome_url = models.SlugField(null=True, max_length=50)
    descricao = models.TextField(null=True, max_length=300)


    def image_tag(self):
        if self.imagem:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.imagem.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Produto'

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def pegar_nota(self):
        total_feedbacks = 0
        for feedback in self.feedbacks.all():
            total_feedbacks += feedback.nota
        if total_feedbacks > 0:
            return total_feedbacks / self.feedbacks.count()
        return 0


    def __str__(self):
        return self.nome
    

class Feedbacks(models.Model):
    produto = models.ForeignKey(Produto, related_name='feedbacks', on_delete=models.CASCADE)
    nota = models.IntegerField(default=3)
    mensagem = models.TextField(max_length=100)
    criado_por = models.ForeignKey(CustomUser, related_name='feedbacks', on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)


class Cupons(models.Model):
    nome = models.CharField(null=True, max_length=30)
    codigo = models.CharField(null=True, max_length=10)
    porcentagem_desconto = models.IntegerField(default=0)
    

class Ordem(models.Model):
    usuario = models.CharField(max_length=50, blank=True, null=True)
    data_ordem = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False, null=True, blank=False)
    id_transacao = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def envio_pedido(self):
        envio_pedido = False
        ordemitens = self.ordemitens_set.all()
        return envio_pedido
            


    @property
    def total_carrinho(self):
        ordemitens = self.ordemitens_set.all()
        total = sum([item.total_item for item in ordemitens])
        return total
    
    def itens_carrinho(self):
        ordemitens = self.ordemitens_set.all()
        total = sum([item.quantidade for item in ordemitens])
        return total
    

    
class OrdemItens(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True)
    ordem = models.ForeignKey(Ordem, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.produto.nome

    @property
    def total_item(self):
        total = self.produto.valor * self.quantidade
        return total
    
    

class Endereço(models.Model):
    usuario = models.CharField(max_length=5, blank=True, null=True)
    nome_usuario = models.CharField(max_length=100, blank=True, null=True)
    logradouro = models.CharField(max_length=100, null=True)
    complemento = models.CharField(max_length=100, null=True)
    numero  = models.IntegerField(null=True)
    bairro = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.logradouro)
    
class Pedido(models.Model):
    usuario = models.CharField(max_length=50, blank=True, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    id_pedido = models.CharField(max_length=50, null=True)
    endereço = models.CharField(max_length= 100,blank=True, null=True)
    meio_pagamento = models.CharField(max_length=30, null=True)
    pedido = models.TextField(max_length=800, null=True)






