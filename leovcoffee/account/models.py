from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user

class CustomUser(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    nome = models.CharField(blank=True, null=True, max_length=150)
    cpf = models.CharField(blank=True, null=True, max_length=14)
    email = models.EmailField(unique=True)
    telefone = models.CharField(blank=True, null=True, max_length=20)
    data_nascimento = models.CharField(blank=True, null=True, max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nome', 'username', 'cpf', 'telefone', 'data_nascimento']

    def __str__(self):
        return self.email
    

    


    

