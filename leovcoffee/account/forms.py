from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import CustomUser

class LoginUser(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))


class RegisterUser(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'nome', 'cpf', 'email', 'telefone', 'password', 'data_nascimento']
    



