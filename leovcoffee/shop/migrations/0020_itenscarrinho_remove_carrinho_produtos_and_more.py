# Generated by Django 4.2.4 on 2023-11-20 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0019_carrinho_itemcarrinho_carrinho_produtos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItensCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='carrinho',
            name='produtos',
        ),
        migrations.AddField(
            model_name='carrinho',
            name='esta_pago',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='carrinho',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ItemCarrinho',
        ),
        migrations.AddField(
            model_name='itenscarrinho',
            name='carrinho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_carrinho', to='shop.carrinho'),
        ),
        migrations.AddField(
            model_name='itenscarrinho',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.produto'),
        ),
    ]
