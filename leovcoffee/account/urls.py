from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.userRegister, name='userRegister'),
    path('login/', views.userLogin, name='userLogin'),
    path('logout/', views.userLogout, name='userLogout'),
    path('confirmarEmail/', views.confirmarEmail, name='confirmarEmail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('minha_conta', views.minhaConta, name="minhaConta"),
    path('cadastrar_endereco', views.cadastrarEndereço, name="cadastrarEndereço"),

    
]