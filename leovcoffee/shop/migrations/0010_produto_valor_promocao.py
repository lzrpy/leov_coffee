# Generated by Django 4.2.4 on 2023-11-08 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_rename_slug_categoria_nome_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='valor_promocao',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
