from django.contrib import admin
from shop.models import Produto, Categoria, Feedbacks, Cupons, Endereço, Pedido


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'nome', 'valor', 'id_produto', 'categoria')

admin.site.register(Produto, ProdutoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nome_url')
admin.site.register(Categoria, CategoriaAdmin)

class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ('produto', 'criado_por', 'data_criacao', 'nota')
admin.site.register(Feedbacks, FeedbacksAdmin)

class CuponsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'porcentagem_desconto' )
admin.site.register(Cupons, CuponsAdmin)

class EndereçoAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'logradouro', 'numero', 'bairro' )
admin.site.register(Endereço, EndereçoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'data_pedido', 'endereço' )
admin.site.register(Pedido, PedidoAdmin)



