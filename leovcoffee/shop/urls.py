from django.urls import path
from . import views
from django.conf import settings #new
from django.conf.urls.static import static #new



urlpatterns = [
    path('', views.produtos, name='produtos'),  
    path('produto/<str:nome_url>/', views.verProduto, name='verProduto'),
    path('produto/<str:nome_url>/atualizar_itens/', views.atualizarItens_vProduto, name='atualizarItens_vProduto'),
    path('q', views.buscarProduto, name='buscarProduto'),
    path('filtroCategorias', views.filtraCategorias, name='filtraCategorias'),
    path('atualizar_itens/', views.atualizarItens, name= 'atualizarItens'),
    path('carrinho/', views.carrinho, name= 'carrinho'),
    path('carrinho/atualizar_itens/', views.atualizarItens_carrinho, name= 'atualizarItens_carrinho'),
    path('confirmar_pedido/', views.confirmarPedido, name= 'confirmarPedido'),
    path('verifica_cupons/', views.verificaCupons, name= 'verificaCupons'),
    path('pagamento_pedido/', views.pagamentoPedido, name= 'pagamentoPedido'),
    path('pedido_finalizado/', views.pedidoFinalizado, name= 'pedidoFinalizado'),
    path('pagamento_pix/', views.pagamentoPix, name= 'pagamentoPix'),
    



] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



   