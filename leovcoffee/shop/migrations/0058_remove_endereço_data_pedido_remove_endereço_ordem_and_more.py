# Generated by Django 4.2.4 on 2023-12-02 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0057_remove_pedido_pedido_teste_alter_pedido_data_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereço',
            name='data_pedido',
        ),
        migrations.RemoveField(
            model_name='endereço',
            name='ordem',
        ),
        migrations.AlterField(
            model_name='endereço',
            name='usuario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
