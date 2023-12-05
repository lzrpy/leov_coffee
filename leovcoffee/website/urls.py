from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre.html', views.sobre, name='sobre'),
    path('contato.html', views.contato, name='contato'),
    
]