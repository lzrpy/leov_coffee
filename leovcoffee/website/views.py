from django.shortcuts import render
from website.models import FormularioContato
from shop.models import Ordem

# Create your views here.

def home(request):
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    return render(request, 'home.html', {"ordem":ordem})

def sobre(request):
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    return render(request, 'sobre.html', {"ordem": ordem})


def contato(request):
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    if request.method == "POST":
        nome = request.POST.get('input_nome')
        email = request.POST.get('input_email')
        telefone = request.POST.get('input_tel')
        mensagem = request.POST.get('input_mensagem')
        status_contato = "Aguardando"
        envio = FormularioContato.objects.create(nome=nome, email=email, telefone=telefone, mensagem=mensagem, status_contato=status_contato)
    return render(request, 'contato.html', {"ordem":ordem})
    



