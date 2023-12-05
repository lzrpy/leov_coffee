from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime
import re
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
from shop.models import Cupons, Endereço, Ordem, Pedido


User = get_user_model()



def password_check(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    compile_regex = re.compile(regex)
    search_regex = re.search(compile_regex, password)
    global senha_valida
    if search_regex:
        senha_valida = True
    else:
        senha_valida = False

def gerador_codigo(codigo):
    caracteres = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    i = 0
    codigo = []
    while i < 6:
        valor = random.randint(0, 9)
        valor_convertido = str(valor)
        codigo.append(valor_convertido)
        i += 1
    return codigo







def userRegister(request):
    if request.method == "POST":
        global username
        username = request.POST.get('input_username')
        global nome
        nome = request.POST.get('input_nome')
        global cpf
        cpf = request.POST.get('input_cpf')
        global data_nascimento
        data_nascimento = request.POST.get('input_data-nascimento')
        global email
        email = request.POST.get('input_email')
        global telefone
        telefone = request.POST.get('input_tel')
        global password
        password = request.POST.get('input_senha')
        data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
        data_atual = datetime.now()
        diferenca = data_atual - data_nascimento
        idade = diferenca.days // 365
        usuario_existe = User.objects.filter(username=username).exists()
        email_existe = User.objects.filter(email=email).exists()
        cpf_existe = User.objects.filter(cpf=cpf).exists()
        telefone_existe = User.objects.filter(telefone=telefone).exists()
        password_check(password)
        
        if usuario_existe == True:
            messages.error(request, f"O username ({username}) já foi cadastrado")
        elif email_existe == True:
            messages.error(request, f"O e-mail ({email}) já foi cadastrado")
        elif cpf_existe == True:
            messages.error(request, "Este CPF informado já foi cadastrado")
        elif telefone_existe == True:
            messages.error(request, "Este número de telefone já foi cadastrado")
        
        else:
            try:
                if idade >= 18: 
                    if senha_valida == True:
                        codigo = []
                        codigo = gerador_codigo(codigo)
                        global codigo_convertido
                        codigo_convertido = "".join(codigo) 
                        subject = "Bem-vindo a LeoV Coffee"
                        mensagem = f'Olá, {username}. Aqui está o seu código para verificação de seu e-mail: {codigo_convertido}'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [email,]
                        send_mail( subject, mensagem, email_from, recipient_list )
                        return redirect("confirmarEmail")               
                    else:
                        messages.error(request, "A senha não corresponde aos requisitos. Sua senha deve conter letra maiúscula e minúscula, número e caracter especial.")

                else:
                    messages.error(request, "Você precisa ter 18 anos para se cadastrar.")
            except:
                return HttpResponse ("Algo deu errado. Por favor, tente novamente")
    return render(request, "register.html")



def userLogin(request):  
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST.get('input_email')
        password = request.POST.get('input_senha')
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "E-mail e/ou senha inválidos. Por favor, verifique e tente novamente")
            print('teste')
        user= authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')    
        else:
            messages.error(request, "E-mail e/ou senha inválidos. Por favor, verifique e tente novamente")
    return render(request, "login.html")

def userLogout(request):
    logout(request)
    return redirect('home')


def confirmarEmail(request):
    if request.method == "POST":
        codigo_inserido = request.POST.get('input_codigo')
        codigo_inserido = str(codigo_inserido)
        try:
            if codigo_inserido == codigo_convertido:
                user = User.objects.create_user(username=username, email=email, password=password, nome=nome, cpf=cpf, telefone=telefone, data_nascimento=data_nascimento)
                user.is_active = True
                user.save()
                return redirect("userLogin")
            else:
                #messages.error(request, "Código incorreto. Verifique novamente o código inserido e tente novamente")
                print("Erro")
        except:
            return HttpResponse ("Algo deu errado. Por favor, tente novamente")

    return render(request, "confirmar_email.html")



def resetarSenha(request):
    if request.method == "POST":
        print('ok')
    return render(request, "resetar_senha.html")

@login_required
def minhaConta(request):
    if not request.user.is_authenticated:
        return redirect("userLogin") 
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    cupons = Cupons.objects.all()
    id_usuario = request.user.id
    nome_usuario = request.user.nome
    meus_endereços = Endereço.objects.filter(usuario=id_usuario)
    meus_pedidos = Pedido.objects.filter(usuario=nome_usuario)
    return render(request, "minha_conta.html", {'cupons': cupons, 'meus_endereços':meus_endereços, 'meus_pedidos':meus_pedidos, 'ordem': ordem})

def cadastrarEndereço(request):
    usuario = request.user.username
    ordem, created = Ordem.objects.get_or_create(usuario=usuario, completo=False)
    if request.method == "POST":
        usuario = request.user.id
        nome_usuario = request.user.nome
        logradouro = request.POST.get('input_logradouro')
        numero = request.POST.get('input_numero')
        complemento = request.POST.get('input_complemento')
        bairro = request.POST.get('input_bairro')
        cidade = request.POST.get('input_cidade')
        estado = request.POST.get('input_estado')
        cadastrar_endereço = Endereço.objects.get_or_create(usuario=usuario, nome_usuario=nome_usuario, logradouro=logradouro, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado)
        return redirect ("minhaConta")
    return render(request, "cadastrar_endereço.html", {'ordem': ordem})


def deleteEndereço(request):
    return redirect("minhaConta")
















# Create your views here.

