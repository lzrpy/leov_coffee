from django.contrib import admin
from website.models import FormularioContato


class FormularioContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'mensagem', 'status_contato')
admin.site.register(FormularioContato,FormularioContatoAdmin)
