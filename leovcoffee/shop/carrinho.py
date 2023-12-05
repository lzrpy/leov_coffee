from django.conf import settings
from shop.models import Produto

class Carrinho(object): 
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(settings.CART_SESSION_ID)
        if not carrinho:
            carrinho = self.session[settings.CART_SESSION_ID] = {}
        self.carrinho = carrinho

    def __iter__(self):
        for p in self.carrinho.keys():
            self.carrinho[str(p)]['produto'] = Produto.objects.get(pk=p)
        
        for item in self.carrinho.values():
            item['valor_total'] = float(item['produto'].valor * item['quantidade'])
            yield item
    
    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.carrinho
        self.session.modified = True

    def add(self, id_produto, quantidade=1, atualizar_quantidade=False):
        id_produto = str(id_produto)
        if id_produto not in self.carrinho:
            self.carrinho[id_produto] = {'quantidade':1, 'id': id_produto}
        if atualizar_quantidade:
            self.carrinho[id_produto]['quantidade'] += int(quantidade)
            if self.carrinho[id_produto]['quantidade'] == 0:
                self.remove(id_produto)
        self.save()

    
    def remove(self, id_produto):
        if id_produto in self.carrinho:
            del self.carrinho[id_produto]
            self.save()

    def valor_total_carrinho(self):
        for p in self.carrinho.keys():
            self.carrinho[str(p)]['produto'] = Produto.objects.get(pk=p)
        return sum(item['produto'].valor * item['quantidade'] for item in self.carrinho.values())
    
    def get_item(self, id_produto):
        return self.carrinho[str(id_produto)]
        