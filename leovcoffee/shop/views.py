from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Produto, Categoria, Feedbacks, Cupons, Ordem, OrdemItens, Endereço, Pedido
from account.models import CustomUser
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
import random





def produtos(request):
    if not request.user.is_authenticated:
        return redirect("userLogin")
    produtos = Produto.objects.all()
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itensCarrinho = ordem.itens_carrinho
    paginacao = Paginator(produtos, 20)
    page_number = request.GET.get("page")
    pagina_obj = paginacao.get_page(page_number)
    categorias = Categoria.objects.all()
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    return render(request, "shop.html", {"pagina_obj": pagina_obj, "categorias": categorias, "ordem": ordem, "itensCarrinho": itensCarrinho})



def verProduto (request, nome_url):
    if not request.user.is_authenticated:
        return redirect("userLogin")
    produto = Produto.objects.get(nome_url=nome_url)
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itensCarrinho = ordem.itens_carrinho
    ver_produto = {
        "produto": produto,
        "ordem": ordem,
        "itensCarrinho": itensCarrinho,
    }
    if request.method == "POST":
        nota = request.POST.get("notas", 3)
        mensagem = request.POST.get("mensagem", " ")
        if mensagem:
            feedbacks = Feedbacks.objects.filter(criado_por=request.user, produto=produto)
            if feedbacks.count() > 0:
                feedback = feedbacks.first()
                feedback.nota = nota
                feedback.mensagem = mensagem
                feedback.save()
            else:
                feedback = Feedbacks.objects.create(
                    produto = produto, 
                    nota = nota,
                    mensagem = mensagem,
                    criado_por = request.user
            )
            return redirect("produtos")

    return render(request, "ver_produto.html", ver_produto)


def buscarProduto(request):
    if not request.user.is_authenticated:
        return redirect("userLogin") 
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itens = ordem.ordemitens_set.all()
    itensCarrinho = ordem.itens_carrinho
    if request.method == "POST":
        q = request.POST.get("q")
        pagina_obj = Produto.objects.filter(nome__icontains=q)
        categorias = Categoria.objects.all()
        return render(request, "shop.html", {'q': q, 'pagina_obj':pagina_obj, "categorias": categorias, 'ordem':ordem, 'itens': itens, 'itensCarrinho': itensCarrinho})
    else:
        return render(request, "shop.html", {})
    
    
def filtraCategorias(request):
    if not request.user.is_authenticated:
        return redirect("userLogin") 
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itens = ordem.ordemitens_set.all()
    itensCarrinho = ordem.itens_carrinho
    if request.method == "POST":
        categoria_selecionada =  request.POST.get('checkbox_categorias')
        if categoria_selecionada == None:
            return redirect ('produtos')
        else:
            pagina_obj = Produto.objects.filter(categoria__nome=categoria_selecionada)
            categorias = Categoria.objects.all()
            return render(request, "shop.html", {'filter': filter, 'pagina_obj':pagina_obj, "categorias": categorias, "categoria_selecionada": categoria_selecionada, 'ordem': ordem, 'itens': itens, 'itensCarrinho': itensCarrinho})
    else:
        return render(request, "shop.html", {})



def atualizarItens(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    usuario = request.user.username
    produto = Produto.objects.get(id=productId)
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    ordemItem, created = OrdemItens.objects.get_or_create(ordem=ordem, produto=produto)
    if action == 'add':
        ordemItem.quantidade = (ordemItem.quantidade + 1)
    elif action == 'remove':
        ordemItem.quantidade = (ordemItem.quantidade - 1)
    elif action == 'trash':
        ordemItem.quantidade = 0
    ordemItem.save()
    if ordemItem.quantidade <= 0:
        ordemItem.delete()

    return JsonResponse('Item adicionado ao carrinho', safe=False)

def atualizarItens_vProduto(request,nome_url ):
    produto = Produto.objects.get(nome_url=nome_url)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    usuario = request.user.username
    produto = Produto.objects.get(id=productId)
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    ordemItem, created = OrdemItens.objects.get_or_create(ordem=ordem, produto=produto)
    if action == 'add':
        ordemItem.quantidade = (ordemItem.quantidade + 1)
    elif action == 'remove':
        ordemItem.quantidade = (ordemItem.quantidade - 1)
    elif action == 'trash':
        ordemItem.quantidade = 0
    ordemItem.save()
    if ordemItem.quantidade <= 0:
        ordemItem.delete()

    return JsonResponse('Item adicionado ao carrinho', safe=False)

def atualizarItens_carrinho(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    usuario = request.user.username
    produto = Produto.objects.get(id=productId)
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    ordemItem, created = OrdemItens.objects.get_or_create(ordem=ordem, produto=produto)
    if action == 'add':
        ordemItem.quantidade = (ordemItem.quantidade + 1)
    elif action == 'remove':
        ordemItem.quantidade = (ordemItem.quantidade - 1)
    elif action == 'trash':
        ordemItem.quantidade = 0
    ordemItem.save()
    if ordemItem.quantidade <= 0:
        ordemItem.delete()

    return JsonResponse('Item adicionado ao carrinho', safe=False)


def carrinho(request): 
    if request.user.is_authenticated:
        usuario = request.user.username
        ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
        itens = ordem.ordemitens_set.all()
        itensCarrinho = ordem.itens_carrinho
    else:
        itens = []
        ordem = {'total_carrinho':0, 'itens_carrinho': 0}
        itensCarrinho = ordem['itens_carrinho']
        return redirect("userLogin")
    context = {'itens': itens, 'ordem': ordem, 'itensCarrinho': itensCarrinho}
    return render(request, 'carrinho.html', context)

def confirmarPedido(request):
    if request.user.is_authenticated:
        usuario = request.user.username
        id_usuario = request.user.id
        endereco_entrega = Endereço.objects.filter(usuario=id_usuario)
        ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
        itens = ordem.ordemitens_set.all()
        itensCarrinho = ordem.itens_carrinho
        cupom = Cupons.objects.filter()
        
    else:
        itens = []
        ordem = {'total_carrinho':0, 'itens_carrinho': 0}
    context = {'itens': itens, 'ordem': ordem, 'itensCarrinho': itensCarrinho, 'endereco_entrega': endereco_entrega}
    return render(request, "confirmar_pedido.html", context)


def verificaCupons(request):
    if request.method == "POST":
        cupom_inserido = request.POST.get('input_buscar_cupom')
        cupom = Cupons.objects.filter(codigo=cupom_inserido)
        id_usuario = request.user.id
        endereco_entrega = Endereço.objects.filter(usuario=id_usuario)
        usuario = request.user.username
        ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
        itens = ordem.ordemitens_set.all()
        itensCarrinho = ordem.itens_carrinho
        if cupom:
            for i in cupom:
                porcentagem_desconto = i.porcentagem_desconto  
                codigo_cupom = i.codigo
            total_carrinho = float(ordem.total_carrinho)
            valor_desconto = (total_carrinho * porcentagem_desconto) / 100
            valor_total_com_desconto = total_carrinho - valor_desconto     
        else:
            (print("cupom nao encontrado"))
        context = {'itens': itens, 'ordem': ordem, 'itensCarrinho': itensCarrinho, 'valor_total_com_desconto': valor_total_com_desconto, 'valor_desconto':valor_desconto, 'codigo_cupom': codigo_cupom, 'endereco_entrega': endereco_entrega}
    return render(request, "verifica_cupons.html", context)

def finalizarPedido(request):
    return JsonResponse("Pagamento realizado", safe=False)


def pagamentoPedido(request):
    if not request.user.is_authenticated:
        return redirect("userLogin") 
    if request.method == "POST":
        global meio_pagamento
        meio_pagamento = request.POST.get('checkbox_meio_pagamento')
        retirar_pedido = request.POST.get('checkbox_retirar_pedido')
        nome_cartao = request.POST.get('input_cc-name')
        numero_cartao = request.POST.get('input_cc-number')
        expiracao_cartao = request.POST.get('input_cc-expiration')
        cvv_cartao = request.POST.get('input_cc-cvv')
        usuario = request.user.username
        ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
        itens = ordem.ordemitens_set.all()
        itensCarrinho = ordem.itens_carrinho
        global endereço
        endereço = request.POST.get('endereco_entrega')
        length_endereço = len(endereço)
        if (retirar_pedido == None) and (length_endereço < 10):
            return HttpResponse("Selecione se você deseja receber o pedido em sua casa ou se deseja retirar o pedido em nossa cafeteria")
        if  (retirar_pedido == "Retirar no local") and (meio_pagamento == "Cartão de Crédito / Débito"):
            length_nome_cartao = len(nome_cartao)
            length_numero_cartao = len(numero_cartao)
            length_expiracao_cartao = len(expiracao_cartao)
            length_cvv_cartao = len(cvv_cartao)
            if (length_nome_cartao <= 10) or (length_numero_cartao < 19) or (length_expiracao_cartao < 5) or (length_cvv_cartao < 3):
                return HttpResponse("Erro. Você precisa inserir todos os dados do seu cartão")
            else:
                return redirect("pedidoFinalizado")
        if meio_pagamento == None:
            return HttpResponse("Meio de Pagamento não disponível. Selecione um meio de pagamento válido e tente novamente")
        if meio_pagamento == "Cartão de Crédito / Débito":
            length_nome_cartao = len(nome_cartao)
            length_numero_cartao = len(numero_cartao)
            length_expiracao_cartao = len(expiracao_cartao)
            length_cvv_cartao = len(cvv_cartao)
            if (length_nome_cartao <= 10) or (length_numero_cartao < 19) or (length_expiracao_cartao < 5) or (length_cvv_cartao < 3):
                return HttpResponse("Erro. Você precisa inserir todos os dados do seu cartão")
            else:
                return redirect("pedidoFinalizado")
        if meio_pagamento == "Pix":
            return redirect("pagamentoPix")
    context = {'itens': itens, 'ordem': ordem, 'itensCarrinho': itensCarrinho}
        
    return render(request, "pedido_finalizado.html")


def gerador_codigo_pedido(codigo):
    caracteres = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    i = 0
    codigo = []
    while i < 4:
        valor = random.randint(0, 9)
        valor_convertido = str(valor)
        codigo.append(valor_convertido)
        i += 1
    return codigo



def pedidoFinalizado (request):
    if not request.user.is_authenticated:
        return redirect("userLogin")
    nome_usuario = request.user.nome 
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itens = ordem.ordemitens_set.all()
    itensCarrinho = ordem.itens_carrinho
    anota_pedido = []
    codigo = []
    codigo = gerador_codigo_pedido(codigo)
    codigo_convertido = "".join(codigo)
    endereço_entrega = endereço
    if len(endereço_entrega) <= 10:
        endereço_entrega = "Retirar no Local"
    for i in itens:
        quantidade = i.quantidade
        anota_pedido.append(["Quantidade:",quantidade])
        produto = i.produto.nome
        anota_pedido.append(["Produto:",produto])
        valor_produto = i.produto.valor
        anota_pedido.append(["Valor Unitário:",valor_produto])
        total_item = i.total_item
        anota_pedido.append(["Valor Total do Produto:",total_item])
        anota_pedido.append(["Valor Total do Pedido:",ordem.total_carrinho])
        anota_pedido.append("                                             ")
        anota_pedido.append("                                                                                              ")
    pedido = Pedido.objects.get_or_create(usuario=nome_usuario, id_pedido=codigo_convertido, endereço=endereço_entrega, meio_pagamento=meio_pagamento, pedido=anota_pedido)
    
    context = {'itens': itens, 'ordem': ordem, 'itensCarrinho': itensCarrinho} #'produto':produto, 'ordemItem': ordemItem,  } 
    return render(request, "pedido_finalizado.html", context)

def pagamentoPix(request):
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    itens = ordem.ordemitens_set.all()
    itensCarrinho = ordem.itens_carrinho
    tel_usuario = request.user.telefone
    remove_caracteres = "-", "(", ")", " "
    for i in remove_caracteres:
        tel_usuario = tel_usuario.replace(i, ' ')
    tel_usuario = tel_usuario.replace(" ", "")
    return render(request, "pagamento_pix.html", {'tel_usuario': tel_usuario, 'itens': itens, 'itensCarrinho': itensCarrinho})








